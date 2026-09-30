"""Executive summary: independently replay the retained FinChain source bank.

This standard-library verifier was authored after collection. It imports no
production oracle, evaluates no corpus programs and changes no artifact. It
replays only the frozen 300 family/seed pairs in memory; no models or network run.
Python must match the recorded 3.13.2 runtime. Numerical compatibility is
conditional on exact inputs versus declared source rounding, not expert truth.
"""

from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal, localcontext
from itertools import product
from collections import Counter, defaultdict
import ast, hashlib, json, re, random, platform

def require(condition, message):
    if not condition:
        raise ValueError(message)

def main():
    ROOT = Path(__file__).resolve().parents[1]
    BASE = ROOT / 'artifacts/finchain-source-v1'
    OUT = ROOT / 'artifacts/independent-financial-source-v1'
    sha = lambda x: hashlib.sha256(x).hexdigest()
    artifact = json.loads((OUT / 'manifest.json').read_text())
    require(artifact['historical_corpus_recovered'] is False, 'Unexpected historical-corpus claim')
    for name, expected in artifact['files'].items():
        require(sha((OUT / name).read_bytes()) == expected, name)
    require(sha((OUT / 'freeze.json').read_bytes()) ==
            '3b177b808f63e5a344cb19694847a6b137ca14f39753c1e18a6ea2786333f911',
            'Retained bank differs from reviewed scientific freeze')
    freeze = json.loads((OUT / 'freeze.json').read_text())
    receipt = json.loads((OUT / 'collection_receipt.json').read_text())
    require(platform.python_version() == freeze['python'] == '3.13.2', "Independent validation failed: platform.python_version() == freeze['python'] == '3.13.2'")
    require(freeze['code_revision'] == '9bd2942b85d992844b77094a8b822aa16832703c', "Independent validation failed: freeze['code_revision'] == '9bd2942b85d992844b77094a8b822aa16832703c'")
    require(freeze['seeds'] == list(range(100)) and freeze['scheduled'] == 300, "Independent validation failed: freeze['seeds'] == list(range(100)) and freeze['scheduled'] == 300")
    for p, h in freeze['files'].items():
        require(sha((ROOT / p).read_bytes()) == h, p)
    for stem, suffix in [('freeze', '.json'), ('analysis', '.json'), ('attempts', '.jsonl')]:
        require(sha((OUT / (stem + suffix)).read_bytes()) == receipt[stem + '_sha256'], "Independent validation failed: sha((OUT / (stem + suffix)).read_bytes()) == receipt[stem + '_sha256']")
    manifest = json.loads((BASE / 'source_manifest.json').read_text())
    code = {}
    for s in manifest['sources']:
        parts = []
        nextline = 1
        for part in s['fragments']:
            b = (BASE / part['file']).read_bytes()
            require(sha(b) == part['sha256'], "Independent validation failed: sha(b) == part['sha256']")
            require(part['first_line'] == nextline and len(b.splitlines()) == part['last_line'] - part['first_line'] + 1, "Independent validation failed: part['first_line'] == nextline and len(b.splitlines()) == part['last_line'] - part['first_line'] + 1")
            nextline = part['last_line'] + 1
            parts.append(b)
        full = b''.join(parts)
        require(sha(full) == s['sha256'], "Independent validation failed: sha(full) == s['sha256']")
        code[s['upstream_path']] = full.decode()

    class TraceRNG:

        def __init__(self, seed):
            self.rng = random.Random(seed)
            self.calls = []

        def choice(self, seq):
            v = self.rng.choice(seq)
            self.calls.append(('choice', len(seq), v))
            return v

        def uniform(self, a, b):
            v = self.rng.uniform(a, b)
            self.calls.append(('uniform', a, b, v))
            return v

        def randint(self, a, b):
            v = self.rng.randint(a, b)
            self.calls.append(('randint', a, b, v))
            return v

    def generate(family, seed):
        path, name = freeze['functions'][family]
        nodes = ast.parse(code[path]).body
        fn = next((n for n in nodes if isinstance(n, ast.FunctionDef) and n.name == name))
        require(not any((isinstance(n, (ast.Import, ast.ImportFrom)) for n in ast.walk(fn))), 'Independent validation failed: not any((isinstance(n, (ast.Import, ast.ImportFrom)) for n in ast.walk(fn)))')
        rng = TraceRNG(seed)
        env = {'random': rng}
        for n in nodes + ast.parse(code['data/templates/corporate_finance/misc.py']).body:
            if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and (n.targets[0].id in {'companies', 'currencies', 'investor_names', 'underlying_assets', 'project_names'}):
                env[n.targets[0].id] = ast.literal_eval(n.value)
        exec(compile(ast.Module(body=[fn], type_ignores=[]), '<inspected-pinned-function>', 'exec'), env)
        q, s = env[name]()
        return (q, s, rng.calls)
    num = '([0-9]+(?:\\.[0-9]+)?)'

    def get(pattern, q):
        m = re.search(pattern, q)
        require(m, q)
        return [F(Decimal(v)) for v in m.groups()]

    def nearest(v, digits):
        m = 10 ** digits
        x = v * m
        n = x.numerator // x.denominator
        if x - n == F(1, 2):
            return (F(n, m), F(n + 1, m))
        return (F(n + int(x - n > F(1, 2)), m),)

    def fmt(v):
        with localcontext() as c:
            c.prec = 50
            return format(Decimal(v.numerator) / Decimal(v.denominator), '.12f')
    rows = [json.loads(x) for x in (OUT / 'attempts.jsonl').read_text().splitlines()]
    require(len(rows) == 300 and len({(r['family'], r['seed']) for r in rows}) == 300, "Independent validation failed: len(rows) == 300 and len({(r['family'], r['seed']) for r in rows}) == 300")
    require({(r['family'], r['seed']) for r in rows} == {(f, s) for f in freeze['functions'] for s in range(100)}, "Independent validation failed: {(r['family'], r['seed']) for r in rows} == {(f, s) for f in freeze['functions'] for s in range(100)}")
    counts = defaultdict(Counter)
    differences = []
    collisions = []
    bounds = []
    traces = Counter()
    ties = Counter()
    errors = []
    for row in rows:
        f, seed = (row['family'], row['seed'])
        q, s, calls = generate(f, seed)
        require(q == row['question'] and s == row['solution'], row['id'])
        require(sha(q.encode()) == row['question_sha256'] and sha(s.encode()) == row['solution_sha256'], "Independent validation failed: sha(q.encode()) == row['question_sha256'] and sha(s.encode()) == row['solution_sha256']")
        traces[f, tuple((c[0] for c in calls))] += 1
        last = next((x.strip() for x in reversed(s.splitlines()) if x.strip()))
        m = re.search('=\\s*' + ('\\$\\s*' if f != 'wacc' else '') + num + ('%' if f == 'wacc' else '') + '\\s*$', last)
        require(m, last)
        native = F(Decimal(m[1]))
        require(native == F(row['native_value']), "Independent validation failed: native == F(row['native_value'])")
        if f == 'binomial_call':
            spot, k, u, d, rate = get(f'S0=\\${num}, K=\\${num}, u={num}, d={num}, r={num} %', q)
            R = 1 + rate / 100
            p = (R - d) / (u - d)
            require(0 < p < 1, 'Independent validation failed: 0 < p < 1')
            su, sd = (spot * u, spot * d)
            cu, cd = (max(su - k, F(0)), max(sd - k, F(0)))
            v = (p * cu + (1 - p) * cd) / R
            delta = (cu - cd) / (su - sd)
            bond = (cu - delta * su) / R
            debt = -bond
            require(delta * spot + bond == v and delta * sd + bond * R == cd, 'Independent validation failed: delta * spot + bond == v and delta * sd + bond * R == cd')
            lower = max(spot - k / R, F(0))
            upper = spot
            require(lower <= v <= upper, 'Independent validation failed: lower <= v <= upper')
            alternatives = [(p * max(a - k, F(0)) + (1 - p) * max(b - k, F(0))) / R for a, b in product(nearest(su, 2), nearest(sd, 2))]
            ties[f] += int(len(alternatives) > 1)
            mutation = debt
            bound = lower - F(1, 200) <= native <= upper + F(1, 200)
            require(bound == row['native_bounds_compatible'], "Independent validation failed: bound == row['native_bounds_compatible']")
            require(list(map(F, row['evidence']['bounds'])) == [lower, upper], "Independent validation failed: list(map(F, row['evidence']['bounds'])) == [lower, upper]")
            if not bound:
                details = []
                for a, b in product(nearest(su, 2), nearest(sd, 2)):
                    p2 = (R * spot - b) / (a - b)
                    selfconsistent = (p2 * max(a - k, F(0)) + (1 - p2) * max(b - k, F(0))) / R
                    details.append({'rounded_up': fmt(a), 'rounded_down': fmt(b), 'selfconsistent_value': fmt(selfconsistent), 'source_rule_value': fmt((p * max(a - k, F(0)) + (1 - p) * max(b - k, F(0))) / R)})
                bounds.append({'id': row['id'], 'native': fmt(native), 'exact': fmt(v), 'lower': fmt(lower), 'below_lower': fmt(lower - native), 'details': details})
        elif f == 'wacc':
            e, d, re_, rd, t = get(f'Equity value = \\${num} (?:million|billion).*?Debt value\\s*= \\${num} (?:million|billion).*?Cost of equity = {num}%.*?Cost of debt\\s*= {num}%.*?Tax rate\\s*= {num}%', q.replace('\n', ' '))
            total = e + d
            v = (e * re_ + d * rd * (1 - t / 100)) / total
            require(v == re_ + d / total * (rd * (1 - t / 100) - re_), 'Independent validation failed: v == re_ + d / total * (rd * (1 - t / 100) - re_)')
            alternatives = [a * re_ + b * rd * (1 - t / 100) for a, b in product(nearest(e / total, 4), nearest(d / total, 4))]
            mutation = (e * re_ + d * rd) / total
            ties[f] += int(len(alternatives) > 1)
        else:
            principal, rate, years = get(f'invested \\${num}.*?annual interest rate of {num}% compounded annually over {num} years', q)
            amount = principal
            for _ in range(int(years)):
                amount *= 1 + rate / 100
            require(amount == principal * (1 + rate / 100) ** int(years), 'Independent validation failed: amount == principal * (1 + rate / 100) ** int(years)')
            v = amount - principal
            alternatives = [a - principal for a in nearest(amount, 2)]
            mutation = amount
            ties[f] += int(len(alternatives) > 1)
        equal = abs(native - v) <= F(1, 200)
        sourceok = any((abs(native - a) <= F(1, 200) for a in alternatives))
        mutok = abs(mutation - v) <= F(1, 200)
        require(v == F(row['exact_reference']) and abs(native - v) == F(row['distance_from_exact']), "Independent validation failed: v == F(row['exact_reference']) and abs(native - v) == F(row['distance_from_exact'])")
        require(sorted(map(str, set(alternatives))) == row['source_convention_references'], "Independent validation failed: sorted(map(str, set(alternatives))) == row['source_convention_references']")
        require((equal, sourceok, mutok) == (row['exact_compatible'], row['source_convention_compatible'], row['mutation_compatible']), "Independent validation failed: (equal, sourceok, mutok) == (row['exact_compatible'], row['source_convention_compatible'], row['mutation_compatible'])")
        c = counts[f]
        c['attempted'] += 1
        c['assessed'] += 1
        c['exact_compatible'] += equal
        c['source_convention_compatible'] += sourceok
        c['mutation_compatible'] += mutok
        c['outside_exact_inside_source_convention'] += not equal and sourceok
        c['outside_both_conventions'] += not equal and (not sourceok)
        if f == 'binomial_call':
            c['native_bounds_compatible'] += bound
        if not equal:
            differences.append({'id': row['id'], 'native': fmt(native), 'exact': fmt(v), 'source_rule_values': [fmt(a) for a in alternatives], 'gap': fmt(native - v), 'within_source': sourceok, 'nearest_ties': len(alternatives), 'native_bounds': bound})
        if mutok:
            collisions.append({'id': row['id'], 'exact': fmt(v), 'mutation': fmt(mutation), 'exact_equal': mutation == v, 'both_state_payoffs_zero': f == 'binomial_call' and cu == cd == 0})
    for f in counts:
        counts[f]['scheduled'] = 100
        counts[f]['unique_questions'] = len({r['question_sha256'] for r in rows if r['family'] == f})
    require({f: dict(c) for f, c in counts.items()} == json.loads((OUT / 'analysis.json').read_text())['counts'], "Independent validation failed: {f: dict(c) for f, c in counts.items()} == json.loads((OUT / 'analysis.json').read_text())['counts']")
    summary = {'validation_scope': 'Postcollection source and scalar replay only; no new seed membership or model calls', 'verifier_sha256': sha(Path(__file__).read_bytes()), 'status': 'PASS', 'python': platform.python_version(), 'frozen_at': freeze['frozen_at_utc'], 'attempts': len(rows), 'counts': {f: dict(c) for f, c in counts.items()}, 'source_files_reconstructed': len(code), 'random_call_sequences': {str(k): v for k, v in traces.items()}, 'intermediate_ties': dict(ties), 'exact_mismatches': differences, 'bounds_violations': bounds, 'quantity_collisions': collisions, 'errors': errors, 'freeze_sha256': sha((OUT / 'freeze.json').read_bytes()), 'attempts_sha256': sha((OUT / 'attempts.jsonl').read_bytes()), 'analysis_sha256': sha((OUT / 'analysis.json').read_bytes())}
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
