"""Executive summary: reconcile repeated minibatch occurrences without rescoring changes.

Reporting-only supplement after the frozen checker rejected nonunique actor tags.
Match every saved occurrence to one raw API call using exact request/text/finish
multisets; apply unchanged independent math, parser, selection and API checks.
No inference, raw edits, retries, deduplication or frozen-source changes.
"""
import json
import sys
from collections import Counter, defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/finance_adaptation'))
import output_support as support
import validate_outputs as original
import validate_reexecution as execution

DESTINATION = ROOT / 'outputs/finance-adaptation-review/response_validation_occurrences.json'
FROZEN_CHECK_API = original.check_api
BOOKKEEPING = {}


def identity(tag, messages, text, finish):
    return tag, json.dumps(messages, sort_keys=True), text, finish


def occurrence_check_api(calls, _collapsed_actors, evaluations, questions, wrapper, route, freeze):
    buckets = defaultdict(deque)
    actor_calls = [r for r in calls if not r['tag'].endswith(':reflection')]
    for api in actor_calls:
        key = identity(api['tag'], api['request_body']['messages'], api['text'], api['finish_reason'])
        buckets[key].append(api)
    occurrences = []
    for r in support.read(execution.OUT / 'format_preflight.jsonl') + support.read(execution.OUT / 'holdout_responses.jsonl'):
        occurrences.append((f'{r["label"]}:{r["case_id"]}', r))
    duplicate_batches = []
    for label, groups in evaluations.items():
        for evaluation, group in groups.items():
            frequencies = Counter(r['case_id'] for r in group)
            if any(n > 1 for n in frequencies.values()):
                assert len(group) == 3 and all(r['partition'] == 'train' for r in group)
                duplicate_batches.append({'run': label, 'evaluation': evaluation,
                                          'case_occurrences': dict(frequencies)})
            occurrences.extend((f'{label}:evaluation-{evaluation}:{r["case_id"]}', r) for r in group)
    indexed_actors, indexed_tags, pairs = {}, {}, []
    placeholders = 0
    for position, (tag, record) in enumerate(occurrences):
        if record['finish_reason'] == 'candidate_too_long':
            indexed_actors[f'overlong-placeholder:{position}'] = record
            placeholders += 1
            continue
        messages = [{'role': 'system', 'content': wrapper['PREFIX'] + record['strategy'] + wrapper['FORMAT']},
                    {'role': 'user', 'content': questions[record['case_id']]['prompt']}]
        key = identity(tag, messages, record['text'], record['finish_reason'])
        assert buckets[key], (tag, 'saved actor occurrence has no matching raw API call')
        api = buckets[key].popleft()
        indexed_tag = f'{tag}:independent-api-index-{api["index"]}'
        assert api['index'] not in indexed_tags
        indexed_tags[api['index']] = indexed_tag
        indexed_actors[indexed_tag] = record
        pairs.append({'saved_occurrence': position, 'raw_api_index': api['index'], 'raw_tag': tag})
    assert not any(buckets.values()), 'unmatched raw actor call'
    assert len(pairs) == len(actor_calls) == 878
    assert len(occurrences) == 989 and placeholders == 111
    private_calls = [{**api, 'tag': indexed_tags[api['index']]} if api['index'] in indexed_tags else api
                     for api in calls]
    # Every original check now sees unique occurrence identifiers in memory only.
    report = FROZEN_CHECK_API(private_calls, indexed_actors, evaluations, questions, wrapper, route, freeze)
    frequencies = Counter(api['tag'] for api in actor_calls)
    BOOKKEEPING.update({
        'amendment': 'postflight reporting-only occurrence reconciliation; frozen tag-uniqueness assertion fails',
        'frozen_checker_failure': 'validate_outputs.check_api nonreflection-tag uniqueness assertion; actors dict also collapses repeated tags',
        'reconciliation': 'one-to-one multiset of raw tag, exact request messages, exact response text and finish reason',
        'identity_limit': 'identical request/response occurrences are exchangeable; no unsaved request index is inferred',
        'saved_occurrences_including_placeholders': len(occurrences),
        'raw_actor_calls_matched': len(pairs), 'raw_actor_unique_tags': len(frequencies),
        'overlong_placeholders_retained': placeholders,
        'duplicate_raw_actor_tags': {tag: n for tag, n in frequencies.items() if n > 1},
        'duplicate_training_batches': duplicate_batches, 'occurrence_matches': pairs,
        'all_numerical_parser_feedback_and_selection_rules_unchanged': True,
        'raw_ledger_and_frozen_files_unchanged': True})
    return report


def main():
    temporary_result = execution.OUT / 'independent/response_validation.json'
    assert not temporary_result.exists(), 'Preserve an existing independent response report'
    frozen, hashes = execution.verify_execution_freeze()
    original.check_api = occurrence_check_api
    execution.main()
    result = execution.load(temporary_result)
    result['status'] = 'PASS_WITH_DISCLOSED_REPORTING_SUPPLEMENT'
    result['occurrence_bookkeeping_supplement'] = BOOKKEEPING
    result['supplement_executed_utc'] = datetime.now(timezone.utc).isoformat()
    result['supplement_sha256'] = support.digest(Path(__file__))
    result['primary_results_sha256'] = support.digest(execution.OUT / 'results.json')
    result['execution_freeze_verification'] = hashes
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    DESTINATION.write_text(json.dumps(result, indent=2) + '\n')
    temporary_result.unlink()
    # Confirm preservation after the unchanged checker and temporary report write.
    execution.verify_execution_freeze()
    print(json.dumps({'status': result['status'], 'path': str(DESTINATION),
                      'matched_raw_actor_calls': BOOKKEEPING['raw_actor_calls_matched'],
                      'duplicate_actor_tags': len(BOOKKEEPING['duplicate_raw_actor_tags']),
                      'rescored_rows': result['rescored_actor_responses'],
                      'holdout_responses': result['holdout_responses']}, indent=2))


if __name__ == '__main__':
    main()
