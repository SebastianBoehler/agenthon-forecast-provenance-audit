"""Executive summary: bundle only this public-source study's draft and reproduction artifacts."""
import hashlib
import json
import shutil
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT/'outputs/answer-contract-research-20260930-document-extension'
DOCS = ['ANSWER_CONTRACT_PROTOCOL_V1.md', 'ANSWER_CONTRACT_PROTOCOL_AMENDMENTS.md',
        'ANSWER_CONTRACT_RESULTS_V1.md', 'ANSWER_CONTRACT_INDEPENDENT_VALIDATION.md',
        'INDEPENDENT_NOVELTY_REASSESSMENT_2026-09-29.md', 'ANSWER_CONTRACT_MANUSCRIPT_REVIEW.md',
        'ANSWER_CONTRACT_REVIEW_RESPONSE.md', 'ANSWER_CONTRACT_EVOLUTION.md',
        'ANSWER_CONTRACT_REPRODUCE.md', 'LOOPED_FORECAST_PILOT_RESULT_V1.md',
        'MARS_CYCLE_RESULTS_V3.md', 'MODEL_GRADING_PROTOCOL_V1.md',
        'MODEL_GRADING_AMENDMENT_NUMERIC.md', 'MODEL_GRADING_CORRECTION_UNITS.md',
        'MODEL_GRADING_PROTOCOL_REVIEW.md', 'MODEL_GRADING_PAPER_REVIEW.md',
        'MODEL_GRADING_MANUSCRIPT_FRAMING.md', 'MODEL_GRADING_FIRST_PAGE_REVIEW.md', 'MODEL_GRADING_REPRODUCE.md',
        'MODEL_GRADING_RESULTS_V1.md', 'MODEL_GRADING_SIZE_EXTENSION.md',
        'PAPER_PRESENTATION_REVIEW.md', 'MODEL_GRADING_SIZE_AND_ABLATION_REVIEW.md',
        'MODEL_GRADING_CONVENTION_SENSITIVITY.md', 'MODEL_GRADING_CONVENTION_REVIEW.md',
        'MODEL_GRADING_CONVENTION_TIMING_CORRECTION.md', 'MODEL_GRADING_INDEPENDENT_RESULTS.md',
        'MODEL_GRADING_REVIEW_RESPONSE.md', 'FINAL_SCIENTIFIC_REVIEW_2026-09-29.md',
        'MAIN_TRACK_RESEARCH_ROADMAP_2026-09-29.md', 'MAIN_TRACK_RESEARCH_REVIEW_2026-09-29.md',
        'MAIN_TRACK_PLAN_FINAL_REVIEW.md',
        'MAIN_TRACK_SOURCE_LEDGER_2026-09-29.md', 'RESEARCH_EXPANSION_TRIAGE_2026-09-29.md',
        'POSTER_CONTENT_2026-09-29.md', 'FINANCE_ADAPTATION_PROTOCOL_V1.md',
        'FINANCE_ADAPTATION_INDEPENDENT_REVIEW.md', 'FINANCE_ADAPTATION_REPRODUCE.md',
        'FINANCE_ADAPTATION_RESULTS_V1.md', 'FINANCE_ADAPTATION_INDEPENDENT_RESULTS.md',
        'FINANCE_ADAPTATION_EXECUTION_AMENDMENT.md', 'FINANCE_ADAPTATION_EXECUTION_REVIEW.md',
        'FINANCE_DOCUMENT_AUDIT_PROTOCOL_V1.md', 'FINANCE_DOCUMENT_AUDIT_READINESS_V1.md',
        'FINANCE_DOCUMENT_AUDIT_REPRODUCTION_REVIEW.md',
        'EXTENDED_LITERATURE_REVIEW_2026-09-30.md', 'EBSCO_DISCOVERY_TRIAGE_2026-09-30.md',
        'EBSCO_SEARCH_LEDGER_2026-09-30.md', 'RESEARCH_ARTIFACT_DESIGN_2026-09-30.md',
        'PAPER_FIGURE_AND_ARTIFACT_REVIEW_2026-09-30.md',
        'FINAL_ARTIFACT_REPLAY_2026-09-30.md',
        'POSTER_VENUE_REVIEW_2026-09-30.md', 'POSTER_EVIDENCE_REVIEW_2026-09-30.md',
        'POSTER_NOVELTY_REVIEW_2026-09-30.md', 'POSTER_ACCEPTANCE_REVIEW_2026-09-30.md',
        'POSTER_REVISION_CHECK_2026-09-30.md', 'PLOTTING.md',
        'FINANCE_DOCUMENT_TECHNICAL_REVIEW_PROTOCOL_V1.md',
        'FINANCE_DOCUMENT_MODEL_PROTOCOL_V1.md', 'FINANCE_DOCUMENT_COMPARISON_PROTOCOL_V1.md',
        'FINANCE_DOCUMENT_NATIVE_METRICS_V1.md', 'FINANCE_DOCUMENT_REPORTING_DIAGNOSTIC_V1.md',
        'FINANCE_DOCUMENT_COLLECTION_CLOSURE_V1.md',
        'FINANCE_DOCUMENT_COMPARISON_INDEPENDENT_REVIEW_V1.md',
        'FINANCE_DOCUMENT_POST_UNBLINDING_SEMANTIC_AUDIT_B.md',
        'FINANCE_DOCUMENT_FINAL_INDEPENDENT_VALIDATION_V1.md',
        'FINANCE_DOCUMENT_DIAGNOSTIC_INDEPENDENT_VALIDATION_V1.md',
        'FINANCE_DOCUMENT_DERIVATIVE_OVERLAP_REVIEW_2026-09-30.md',
        'FINANCE_DOCUMENT_RESULTS_V1.md', 'FINANCE_DOCUMENT_REPRODUCE_V1.md',
        'MAIN_TRACK_DOCUMENT_EXTENSION_REVIEW_2026-09-30.md',
        'MAIN_TRACK_ITERATION_2026-09-30.md']


def copy(path: Path, target: Path | None = None):
    relative = path.relative_to(ROOT) if target is None else target
    destination = DESTINATION/relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, destination)


def main():
    if DESTINATION.exists():
        shutil.rmtree(DESTINATION)
    DESTINATION.mkdir(parents=True, exist_ok=True)
    for directory in ['src/answer_contract', 'src/model_grading', 'src/finance_adaptation',
                      'scripts/finance_adaptation', 'scripts/finance_document_audit',
                      'src/finance_document_review']:
        for path in sorted((ROOT/directory).glob('*.py')):
            copy(path)
    for name in ['run_answer_contract.py','stage_answer_contract.py',
                 'independent_contract_validation.py','package_answer_contract.py',
                 'prepare_model_grading.py', 'run_model_grading_local.py',
                 'run_model_grading_remote.py', 'evaluate_model_grading.py',
                 'evaluate_model_grading_sensitivity.py', 'build_model_grading_review.py',
                 'validate_model_grading_outputs.py', 'validate_model_grading_selection.py',
                 'validate_model_grading_extension.py',
                 'census_model_grading_conventions.py',
                 'analyze_model_grading_conventions.py', 'validate_model_grading_conventions.py',
                 'report_model_grading.py',
                 'append_model_review_responses.py',
                 'render_answer_contract_tables.py', 'run_model_grading_extension.py',
                 'evaluate_model_grading_extension.py', 'prepare_finance_adaptation.py',
                 'freeze_finance_adaptation.py', 'run_finance_adaptation.py',
                 'report_finance_adaptation.py', 'freeze_finance_adaptation_v2.py',
                 'run_finance_adaptation_v2.py', 'report_finance_adaptation_v2.py',
                 'validate_finance_adaptation_occurrences.py',
                 'render_answer_contract_figures.py', 'validate_research_artifact.py',
                 'validate_finance_document_packets.py', 'validate_finance_document_review.py',
                 'lock_finance_document_reviews.py', 'run_finance_document_models.py',
                 'analyze_finance_document_models.py', 'replay_finance_document_artifact.py',
                 'close_finance_document_collection.py',
                 'replay_finance_document_diagnostics.py',
                 'finance_document_review_independent_controls.py',
                 'validate_finance_document_final.py',
                 'validate_finance_document_diagnostics.py',
                 'render_finance_document_evidence.py', 'validate_finance_document_extension.py']:
        copy(ROOT/'scripts'/name)
    for name in DOCS:
        copy(ROOT/'docs'/name)
    for path in [ROOT/'PAPER.md', ROOT/'figures/paper_evidence.py',
                 ROOT/'experiments/research_exploration_graph_v1.json',
                 ROOT/'experiments/research_claim_evidence_v1.json',
                 ROOT/'outputs/literature-search-20260930/ebsco_query_metadata.json',
                 ROOT/'outputs/final-artifact-replay-results.json',
                 ROOT/'tests/test_answer_contract.py', ROOT/'figures/answer_contract.py',
                 ROOT/'tests/test_document_review_arithmetic.py',
                 ROOT/'tests/test_document_model_parser.py', ROOT/'tests/test_document_comparison.py',
                 ROOT/'figures/document_evidence.py',
                 ROOT/'experiments/finance_document_extension_manifest_v1.json',
                 ROOT/'figures/style.py', ROOT/'paper/answer_contract_audit.tex',
                 ROOT/'tests/test_model_grading.py', ROOT/'tests/test_model_grading_sensitivity.py',
                 ROOT/'tests/test_finance_adaptation.py',
                 ROOT/'tests/test_finance_adaptation_logging.py',
                 ROOT/'figures/model_grading.py', ROOT/'experiments/model_grading_requirements.txt',
                 ROOT/'experiments/finance_adaptation_requirements.txt',
                 ROOT/'experiments/finance_document_audit_sources_v1.json',
                 ROOT/'experiments/review_requirements.txt',
                 ROOT/'experiments/finance_document_review_requirements.txt',
                 ROOT/'experiments/answer_contract_requirements.txt',
                 ROOT/'experiments/cosimo_source_manifest.json']:
        copy(path)
    for directory in ['outputs/answer-contract-v1','outputs/answer-contract-independent',
                      'outputs/model-grading-v1', 'outputs/model-grading-review',
                      'outputs/finance-adaptation-v1', 'outputs/finance-adaptation-v2',
                      'outputs/finance-adaptation-review']:
        for path in sorted((ROOT/directory).rglob('*')):
            if path.is_file() and path.suffix in ['.json', '.jsonl', '.md', '.csv', '.py']:
                copy(path)
    for directory in ['outputs/finance-document-review-v1', 'outputs/finance-document-models-v1',
                      'outputs/finance-document-native-v1', 'outputs/finance-document-replay-v1',
                      'outputs/finance-document-diagnostics-v1',
                      'outputs/finance-document-diagnostics-independent-v1']:
        for path in sorted((ROOT/directory).rglob('*')):
            if (path.is_file() and path.name != 'analysis_stdout.json'
                    and (path.suffix in ['.json', '.jsonl', '.md', '.py'] or path.name == 'LICENSE')):
                copy(path)
    for path in (ROOT / 'outputs/finance-document-derivative-overlap-v1').iterdir():
        if path.is_file() and path.suffix in ['.json', '.py', '.md']:
            copy(path)
    document_preparation = ROOT / 'outputs/finance-document-audit-v1'
    for path in sorted(document_preparation.rglob('*')):
        if (path.is_file() and path.suffix in ['.json', '.jsonl', '.md', '.py']
                and 'raw' not in path.relative_to(document_preparation).parts
                and path.name not in ['source_targets.jsonl', 'reviewer_a.jsonl', 'reviewer_b.jsonl']):
            copy(path)
    document_replay = ROOT / 'outputs/finance-document-reproduction'
    for path in sorted(document_replay.iterdir()):
        if path.is_file() and path.suffix in ['.json', '.py']:
            copy(path)
    graph = json.loads((ROOT/'experiments/research_exploration_graph_v1.json').read_text())
    for evidence in graph['evidence']:
        relative = Path(evidence['path'])
        assert not relative.is_absolute() and '..' not in relative.parts
        path = ROOT/relative
        assert path.resolve().is_relative_to(ROOT.resolve())
        assert path.suffix in ['.json', '.jsonl', '.md', '.py', '.txt', '.toml'] or path.name == 'LICENSE'
        assert hashlib.sha256(path.read_bytes()).hexdigest() == evidence['sha256']
        copy(path)
    for path in (ROOT/'outputs/research-artifact-v1').glob('*.json'):
        copy(path)
    for directory in ['answer-contract-v1', 'model-grading-v1', 'paper-evidence-v1', 'document-evidence-v1']:
        for path in sorted((ROOT/'figures/generated'/directory).glob('*')):
            if path.suffix in ['.png','.pdf','.svg','.json','.tikz']:
                copy(path)
    readme = ('## Executive summary (read this first)\n\n'
              'Local manuscript source and reproducibility package for *When Verified Financial Labels Fail*.\n'
              'The draft names Sebastian Boehler. Confirm coauthors/affiliation and Atlanta attendance\n'
              'before submission. No external submission or public release has occurred.\n\n'
              'Start with paper/answer_contract_audit.tex in the current native editor and docs/ANSWER_CONTRACT_REPRODUCE.md.\n'
              'The current draft compiles in that editor; no separate paper PDF is exported in this bundle.\n'
              'Data are pinned public releases downloaded by scripts/stage_answer_contract.py.\n'
              'Numerical patches are not certified reasoning traces or a ready DPO corpus.\n'
              'The original study grades 800 saved answers from four checkpoints.\n'
              'A separate frozen GEPA pilot measures prompt adaptation; no model weights change.\n'
              'Its first collection failed with a disclosed GEPA logging error. V2 completed 432 heldouts with isolated logs.\n'
              'All optimizer arms retained the seed; both gates failed. The pilot is inconclusive about adaptation effects.\n'
              'Replay that pilot without API calls using docs/FINANCE_ADAPTATION_REPRODUCE.md.\n'
              'Use PAPER.md for the claim/evidence index and recorded unsuccessful research branches.\n'
              'Historical metric checks are distinct from fresh training/inference; weights and full training corpora are external.\n'
              'New measured figures use tueplots/figures4papers guidance and embed generated TikZ in the standalone source.\n'
              'The future main-track plan and its evidence gates are in docs/MAIN_TRACK_RESEARCH_ROADMAP_2026-09-29.md.\n'
              'The later extension retains two blind AI technical reviews and384 attempts:383 API records plus1 censored event.\n'
              'Its numerical/unit proxy, rounding diagnostic and native/adapted grades are separate measurements.\n'
              'Known FinanceReasoning repairs are not claimed as first discoveries; semantic review is AI-assisted.\n'
              'Replay saved document scores without APIs using scripts/replay_finance_document_artifact.py.\n'
              'A later compact diagnostic replay checks all384 posthoc recovery/expression rows.\n'
              'Use docs/FINANCE_DOCUMENT_REPRODUCE_V1.md for the external-runtime commands and boundaries.\n'
              'Full corpora, original annotation dictionaries and original question/context packets remain excluded.\n'
              'Compact numeric native fields, derived reviews and responses are retained for saved-score replay.\n'
              'Replay model grading without inference using docs/MODEL_GRADING_REPRODUCE.md.\n'
              'Strict format compliance and posthoc numerical extraction are distinct endpoints.\n')
    (DESTINATION/'README.md').write_text(readme)
    manifest = {'executive_summary': 'Hashed local draft and audit artifact; no sealed competition data.',
                'status': 'draft_author_metadata_and_attendance_pending',
                'files': {str(p.relative_to(DESTINATION)): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sorted(DESTINATION.rglob('*')) if p.is_file() and p.name!='bundle_manifest.json'}}
    (DESTINATION/'bundle_manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    archive = DESTINATION.with_suffix('.zip')
    with ZipFile(archive, 'w', compression=ZIP_DEFLATED) as output:
        for path in sorted(DESTINATION.rglob('*')):
            if path.is_file():
                output.write(path, str(path.relative_to(DESTINATION)))
    print(json.dumps({'archive': str(archive), 'files':len(manifest['files']),
                      'sha256':hashlib.sha256(archive.read_bytes()).hexdigest()}, indent=2))


if __name__=='__main__':
    main()
