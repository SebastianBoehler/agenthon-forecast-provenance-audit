"""Executive summary: reject failed records and diagnose only declared status repairs."""
import json
import unittest

from finance_document_local.scoring import candidate, score


class LocalParserControls(unittest.TestCase):
    def setUp(self):
        self.answer = {'status': 'answer', 'value': '21', 'unit': 'count', 'scale': 'none'}
        self.reference = {'source': 'finqa', 'joint_status': 'agreed_determinate_numeric',
                          'reference_values': ['21'],
                          'unit_a': {'dimension': 'count', 'factor': '1'}}

    def test_runtime_failure_never_credited(self):
        response = {'model_key': 'control', 'condition': 'compact_baseline',
                    'case_id': 'authored', 'text': json.dumps(self.answer),
                    'error': 'generation_failed', 'runtime_ok': True, 'token_audit_ok': True}
        result = score(response, self.reference, {'exe_ans': 21})
        self.assertIsNone(result['strict_candidate'])
        self.assertIsNone(result['status_only_candidate'])
        self.assertFalse(result['strict_locked']['matches'])
        response['error'] = None
        response['token_audit_ok'] = False
        self.assertIsNone(score(response, self.reference, {'exe_ans': 21})['strict_candidate'])

    def test_nonstandard_constants_and_duplicate_keys(self):
        full = dict(self.answer, calculation='3*7', evidence=[float('nan')])
        self.assertEqual(candidate(json.dumps(full), 'full_baseline')[1], 'invalid_json')
        for constant in ['Infinity', '-Infinity']:
            self.assertEqual(candidate(json.dumps(full).replace('NaN', constant),
                                       'full_baseline')[1], 'invalid_json')
        duplicate = json.dumps(self.answer)[:-1] + ', "value": "22"}'
        self.assertEqual(candidate(duplicate, 'compact_baseline')[1], 'invalid_json')

    def test_status_only_requires_string_and_complete_original_fields(self):
        wrong = dict(self.answer, status='numeric')
        self.assertIsNone(candidate(json.dumps(wrong), 'compact_baseline')[0])
        repaired, error = candidate(json.dumps(wrong), 'compact_baseline', normalize_status=True)
        self.assertIsNone(error)
        self.assertEqual(repaired['value'], '21')
        wrong['status'] = False
        self.assertIsNone(candidate(json.dumps(wrong), 'compact_baseline', normalize_status=True)[0])
        wrong.pop('scale')
        self.assertIsNone(candidate(json.dumps(wrong), 'compact_baseline', normalize_status=True)[0])

    def test_compact_adapter_is_empty_and_full_prose_is_not_execution(self):
        compact, error = candidate(json.dumps(self.answer), 'compact_baseline')
        self.assertIsNone(error)
        self.assertEqual((compact['calculation'], compact['evidence']), ('', []))
        full = dict(self.answer, calculation='Assume groups: 3*7', evidence=[])
        self.assertIsNotNone(candidate(json.dumps(full), 'full_baseline')[0])


if __name__ == '__main__':
    unittest.main()
