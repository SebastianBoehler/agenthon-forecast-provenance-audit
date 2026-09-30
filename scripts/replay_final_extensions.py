"""Executive summary: prepare or replay complete scalar projections of the final two model arms."""

import argparse
from collections import Counter
from decimal import Decimal
import hashlib
import json
from zipfile import ZipFile
from pathlib import Path

from grader_comparison.analysis import financial_scores
from grader_comparison.native import load, normalized_comparison
from grader_comparison.protocol import ROOT, read, digest, write, jsonl
from grader_comparison.scalars import scalar, final_scalar

BANK = ROOT / 'artifacts/final-model-extensions-v1'
COHORT = ROOT / 'artifacts/grader-comparison-v1/cohort_projection.jsonl'


def api_cost_total(usage):
    return sum((Decimal(str(row['cost_usd'])) for row in usage), Decimal(0))


def scores(rows, cases):
    env, _ = load()
    counts = {f'{model}/{domain}': Counter() for model in ('glm', 'llama') for domain in ('finance', 'math')}
    seen = set()
    for r in rows:
        key = (r['model'], r['repetition'], r['case_id'])
        if key in seen or r['model'] not in ('glm', 'llama') or r['repetition'] not in range(3):
            raise ValueError('Duplicate or unexpected extension attempt')
        seen.add(key)
        case = cases[r['case_id']]
        c = counts[r['model']+'/'+case['domain']]
        c['attempted'] += 1
        if r['status'] != 'returned' or r['at_output_cap'] or r['stop_nondecision'] or r['final_scalar'] is None:
            c['nondecision'] += 1
            continue
        c['admitted'] += 1
        value = scalar(r['final_scalar'])
        if case['domain'] == 'finance':
            result = financial_scores(case, value)
            for k in ('released_label_cent', 'complete_contract'):
                c[k] += int(result[k])
            c['valid_denied'] += int(result['complete_contract'] and not result['released_label_cent'])
        else:
            equal = value == scalar(case['reference'])
            native = normalized_comparison(env, case['reference'], r['final_scalar'])[0]
            c['exact'] += int(equal)
            c['native'] += int(native)
            c['unequal_credit'] += int(native and not equal)
            c['equal_denial'] += int(not native and equal)
    expected = {(m, rep, ident) for m in ('glm','llama') for rep in range(3) for ident in cases}
    if seen != expected:
        raise ValueError('Extension schedule incomplete')
    return {k:dict(v) for k,v in counts.items()}


def prepare():
    BANK.mkdir(exist_ok=False)
    glm = ROOT / 'outputs/glm-final-extension-v1'
    llama = ROOT / 'outputs/llama-final-extension-v2'
    cases = {r['id']:r for r in read(COHORT)}
    original = {r['id']:r for r in read(glm/'cohort.jsonl')}
    if original != {r['id']:r for r in read(llama/'cohort.jsonl')}:
        raise ValueError('Extension questions differ')
    projected, usage = [], []
    for row in read(glm/'attempt_projection.jsonl'):
        record = json.loads((glm / f"request-{row['sequence']:03d}.json").read_text())
        if record['request']['messages'][-1]['content'] != original[row['case_id']]['prompt']:
            raise ValueError('API prompt differs from frozen question')
        if hashlib.sha256(record['text'].encode()).hexdigest() != row['response_sha256']:
            raise ValueError('API reply hash changed')
        projected.append({'model':'glm','case_id':row['case_id'],'repetition':row['repetition'],
                          'status':record['status'],'at_output_cap':record['at_output_cap'],
                          'stop_nondecision':record['finish_reason'] != 'stop',
                          'final_scalar':final_scalar(record['text']), 'response_sha256':row['response_sha256']})
    for path in sorted(llama.glob('attempt-*.json')):
        r=json.loads(path.read_text())
        if r['request']['input'] != original[r['case_id']]['prompt']:
            raise ValueError('Local prompt differs from frozen question')
        projected.append({'model':'llama','case_id':r['case_id'],'repetition':r['repetition'],
                          'status':r['status'],'at_output_cap':r.get('at_output_cap',False),
                          'stop_nondecision':False,'final_scalar':final_scalar(r.get('text','')),
                          'response_sha256':hashlib.sha256(r.get('text','').encode()).hexdigest()})
    for path in sorted(glm.glob('request-*.json')):
        r=json.loads(path.read_text());raw=r['raw_response']
        if raw['provider'] != 'Novita' or raw['model'] != 'z-ai/glm-4.7-flash' or r['cost_usd'] is None:
            raise ValueError('Unsettled or changed API route')
        usage.append({'sequence':r['sequence'],'cost_usd':r['cost_usd'],'provider':raw['provider'],
                      'model':raw['model'],'usage':raw['usage'],'elapsed_s':r['elapsed_s']})
    if len(usage) != 51:
        raise ValueError('Missing API requests including preflight')
    jsonl(BANK/'attempt_projection.jsonl',projected)
    write(BANK/'analysis.json',{'scheduled':96,'counts':scores(projected,cases),
          'api_requests_including_probes':51,'observed_api_usd':float(api_cost_total(usage)),
          'scope':'Exploratory paired scoring on the existing panel, not family or capacity effects.'})
    jsonl(BANK/'api_usage.jsonl',usage)
    for source,target in [(glm/'protocol.json','glm_protocol.json'),(llama/'protocol.json','llama_protocol.json'),
                          (ROOT/'outputs/llama-final-extension-v1/protocol.json','llama_failed_protocol.json'),
                          (ROOT/'outputs/llama-final-extension-v1/probes.json','llama_failed_probes.json'),
                          (ROOT/'outputs/llama-final-extension-v1/frozen_collector.py','llama_failed_collector.py')]:
        (BANK/target).write_bytes(source.read_bytes())
    write(BANK/'manifest.json',{'executive_summary':'Complete final-arm scalar evidence and disclosed readiness failure.',
          'cohort_projection_sha256':digest(COHORT),
          'files':{p.name:digest(p) for p in BANK.iterdir() if p.is_file()}})


def replay():
    manifest=json.loads((BANK/'manifest.json').read_text())
    if digest(COHORT) != manifest['cohort_projection_sha256']:
        raise ValueError('Original cohort projection changed')
    for name,expected in manifest['files'].items():
        if Path(name).name != name or digest(BANK/name) != expected:
            raise ValueError('Extension evidence identity changed')
    collectors=json.loads((BANK/'collector_sources_manifest.json').read_text())
    if digest(BANK/'manifest.json') != collectors['parent_manifest_sha256'] or digest(BANK/'collector_sources.zip') != collectors['archive_sha256']:
        raise ValueError('Collector source supplement identity changed')
    with ZipFile(BANK/'collector_sources.zip') as z:
        for name, expected in collectors['files'].items():
            protocol = json.loads((BANK / ('glm_protocol.json' if name.startswith('glm') else 'llama_protocol.json')).read_text())
            if hashlib.sha256(z.read(name)).hexdigest() != expected or expected != protocol['script_sha256']:
                raise ValueError('Frozen collector source changed')
    failed=json.loads((BANK/'llama_failed_protocol.json').read_text())
    if digest(BANK/'llama_failed_collector.py') != failed['script_sha256']:
        raise ValueError('Failed readiness collector changed')
    rows=read(BANK/'attempt_projection.jsonl')
    cases={r['id']:r for r in read(COHORT)}
    report=json.loads((BANK/'analysis.json').read_text())
    if scores(rows,cases) != report['counts']:
        raise ValueError('Extension scores changed')
    usage=read(BANK/'api_usage.jsonl')
    if len(usage) != 51 or api_cost_total(usage) != Decimal(str(report['observed_api_usd'])):
        raise ValueError('API usage ledger changed')
    return {'status':'PASS','attempts':len(rows),'counts':report['counts'],
            'observed_api_usd':report['observed_api_usd'],
            'scope':'Saved scalar scoring and recorded API usage; raw extraction and financial meaning not certified.'}


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare',action='store_true')
    if parser.parse_args().prepare:
        prepare()
    print(json.dumps(replay(),indent=2))
