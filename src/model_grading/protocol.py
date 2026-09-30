"""Executive summary: freeze sample, prompts, model identities, and strict answer extraction."""
import hashlib
import json
import re
from decimal import Decimal, InvalidOperation
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DESTINATION = ROOT / 'outputs/model-grading-v1'
FAMILIES = ('cr_eq_gordon', 'deriv_binomial_call', 'eq_gordon', 'corp_wacc')
SAMPLE_SALT = 'model-grading-v1-20260929'
SYSTEM = (
    'Solve the financial question using the information shown. Briefly show the '
    'calculation in at most five sentences. Respect any rounding instruction in '
    'the question. If no rounding instruction is given, give at least four decimal '
    'places. End with exactly one final line in this format: FINAL: <number> <unit>. '
    'Use currency as the unit for monetary values. Use percent for a rate, expressed '
    'in percentage points (for example, 7.25 percent rather than 0.0725). '
    'Do not put Markdown formatting on the final line.'
)
LOCAL_MODELS = {
    'qwen3-1.7b': {
        'repository': 'Qwen/Qwen3-1.7B',
        'revision': '70d244cc86ccca08cf5af4e1e306ecf908b1ad5e',
        'thinking': False,
    },
    'qwen2.5-coder-3b': {
        'repository': 'Qwen/Qwen2.5-Coder-3B-Instruct',
        'revision': '488639f1ff808d1d3d0ba301aef8c11461451ec5',
    },
}
REMOTE_MODEL = {
    'model': 'deepseek/deepseek-v3.2',
    'canonical_slug': 'deepseek/deepseek-v3.2-20251201',
    'provider_tag': 'siliconflow/fp8',
    'provider_name': 'SiliconFlow',
    'prompt_price_per_token': '0.000000259',
    'completion_price_per_token': '0.00000042',
}
MAX_TOKENS = 1024
FINAL = re.compile(
    r'FINAL: ([+-]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?'
    r'(?:[eE][+-]?\d+)?) (currency|percent)', re.IGNORECASE)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def question_hash(prompt: str) -> str:
    return hashlib.sha256(prompt.encode()).hexdigest()


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines()]


def frozen_selection() -> list[dict]:
    manifest = json.loads((DESTINATION / 'selection_manifest.json').read_text())
    for name, checksum in manifest['frozen_sha256'].items():
        if digest(ROOT / name) != checksum:
            raise ValueError(f'Frozen study file changed: {name}')
    rows = read_jsonl(DESTINATION / 'selection.jsonl')
    if len(rows) != 200 or len({r['question_hash'] for r in rows}) != 200:
        raise ValueError('Frozen question denominator changed')
    return rows


def parse_final(text: str, family: str) -> tuple[Decimal | None, str | None]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    markers = re.findall(r'FINAL:', text, re.IGNORECASE)
    if len(markers) != 1 or not lines:
        return None, 'missing_or_nonfinal_marker'
    match = FINAL.fullmatch(lines[-1])
    if match is None:
        return None, 'invalid_final_format'
    unit = 'percent' if family == 'corp_wacc' else 'currency'
    if match[2].lower() != unit:
        return None, 'wrong_unit'
    try:
        value = Decimal(match[1].replace(',', ''))
    except InvalidOperation:
        return None, 'invalid_decimal'
    if not value.is_finite():
        return None, 'nonfinite_answer'
    return value, None


def append_record(path: Path, record: dict) -> None:
    with path.open('a') as stream:
        stream.write(json.dumps(record, ensure_ascii=False) + '\n')
        stream.flush()
