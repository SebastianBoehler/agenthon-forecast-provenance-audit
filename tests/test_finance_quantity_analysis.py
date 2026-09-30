"""Executive summary: authored controls expose type, grammar and judge-evidence limits."""

import json
import unittest
from fractions import Fraction

from finance_quantity_analysis.endpoints import arithmetic, candidate, evidence_invalid, judge, raw_evidence, score
from finance_quantity_analysis.provenance import MALFORMED_RULE, budget_audit
from finance_quantity_transfer.runner import judge_payload
from finance_quantity_transfer.scoring import score as frozen_score
from scripts.analyze_finance_quantity_transfer import usage_counts


class IndependentQuantityControls(unittest.TestCase):
    def answer(self, **changes):
        record=dict(status='answer',value='25',unit='percent',scale='none',
                    calculation='(150-120)/120*100',evidence=['table[1][1]','table[2][1]'])
        record.update(changes)
        return json.dumps(record)

    def reference(self, **changes):
        record=dict(eligible=True,value='25',unit='percent',scale='none',calculation='(150-120)/120*100')
        record.update(changes)
        return record

    def verdict(self, **changes):
        record=dict(verdict='supported',requested_quantity='Cost increase',operand_checks=[],
                    unit_check='Percent',reason='150 versus 120',evidence=['table[1][1]'])
        record.update(changes)
        return json.dumps(record)

    def test_fraction_arithmetic_and_unsafe_grammar(self):
        self.assertEqual(arithmetic('(0.3-0.1)/0.1'),Fraction(2))
        for expression in ['sum([1,2])','__import__("os")','1 // 2','2 ** 0.5','2 ** 33','True+1','1;2']:
            with self.assertRaises((ValueError,SyntaxError)): arithmetic(expression)

    def test_per_share_and_total_are_distinct_at_zero(self):
        s=score(self.answer(value='0',unit='currency',calculation='0.36-0.36'),
                self.reference(value='0',unit='currency_per_share'))
        self.assertFalse(s['reported_numeric_typed_match'])
        self.assertFalse(s['expression_numeric_typed_match'])

    def test_duration_and_count_are_distinct(self):
        s=score(self.answer(value='3',unit='count',calculation='1+1+1'),
                self.reference(value='3',unit='duration_years'))
        self.assertTrue(s['schema_valid'])
        self.assertFalse(s['reported_numeric_typed_match'])

    def test_dimensionless_scale_rejected(self):
        self.assertIsNotNone(candidate(self.answer(scale='thousand'))[1])
        self.assertIsNotNone(candidate(self.answer(unit='ratio',scale='million'))[1])

    def test_monetary_scale_is_single_multiplier(self):
        s=score(self.answer(value='1',unit='currency',scale='million',calculation='1'),
                self.reference(value='1000000',unit='currency',scale='none'))
        self.assertTrue(s['reported_numeric_typed_match'])

    def test_native_is_literal_not_scaled_or_tolerant(self):
        s=score(self.answer(value='1',unit='currency',scale='million',calculation='1'),
                self.reference(value='1000000',unit='currency'),{'value':'1000000'})
        self.assertTrue(s['reported_numeric_typed_match'])
        self.assertFalse(s['native_literal_exact'])

    def test_native_scalar_decimal_serialization(self):
        text=self.answer(value='0.1',calculation='1/10')
        for native in ['0.1',0.1]:
            self.assertTrue(score(text,self.reference(value='0.1'),{'value':native})['native_literal_exact'])
        self.assertTrue(score(self.answer(),self.reference(),{'value':25})['native_literal_exact'])
        for native in [True,None,float('nan')]:
            with self.assertRaises((ValueError,ArithmeticError)):
                score(text,self.reference(),{'value':native})
        s=score(self.answer(value='25.00000001'),self.reference(),{'value':'25'})
        self.assertTrue(s['reported_numeric_typed_match'])
        self.assertFalse(s['native_literal_exact'])

    def test_expression_diagnostic_does_not_repair_output(self):
        s=score(self.answer(value='24'),self.reference())
        self.assertFalse(s['reported_numeric_typed_match'])
        self.assertTrue(s['expression_numeric_typed_match'])
        self.assertFalse(s['reported_expression_consistent'])
        self.assertIsNotNone(candidate(self.answer(calculation='assuming costs are comparable: (150-120)/120*100'))[1])

    def test_invalid_candidate_forces_unassessable(self):
        context={'table':[['year','cost'],['1','120']]}
        j,error=judge(self.verdict(),context,'invalid answer')
        self.assertIsNone(error)
        self.assertEqual(j['effective_verdict'],'unassessable')
        self.assertTrue(j['protocol_violation'])

    def test_invalid_judge_pointer_and_duplicate_fields(self):
        context={'table':[['year','cost'],['1','120']]}
        for text in [self.verdict(evidence=['table[99][0]']),self.verdict()[:-1]+',"verdict":"supported"}']:
            j,error=judge(text,context,None)
            self.assertIsNotNone(error)
            self.assertEqual(j['effective_verdict'],'unassessable')
        audit=raw_evidence(self.verdict(evidence=['table[99][0]']),context)
        self.assertEqual(audit['invalid_paths'],['table[99][0]'])

    def test_optional_usage_fields_remain_unknown(self):
        authored=[{'answer_recorded':True,'answer_usage':{'cost':'0.001','completion_tokens':1024,
                    'completion_tokens_details':None}},
                  {'answer_recorded':True,'answer_usage':{'cost':None,'completion_tokens':None,
                    'completion_tokens_details':{'reasoning_tokens':0}}}]
        totals=usage_counts(authored,'answer')
        self.assertEqual(totals['known_cost_usd'],'0.001')
        self.assertEqual(totals['unknown_cost_records'],1)
        self.assertEqual(totals['at_output_cap'],1)
        self.assertEqual(totals['reasoning_tokens_records_known'],1)

    def test_exact_frozen_judge_rule_literal(self):
        authored={'question':'What is the cost increase?', 'original_context':{'table':[['120'],['150']]}}
        payload=judge_payload(authored,{'text':self.answer()})
        self.assertEqual(payload['malformed_candidate_rule'],MALFORMED_RULE)

    def test_unknown_billing_is_not_zero_or_complete(self):
        authored=[dict(event='reserved',call_id='control',study_id='study',utc='1',reserve_usd='0.002',request_sha256='control'),
                  dict(event='settled',call_id='control',study_id='study',utc='2',cost_usd=None,request_sha256='control')]
        audit=budget_audit(authored,[],'study')
        self.assertFalse(audit['observed_cost_complete'])
        self.assertIsNone(audit['full_observed_aggregate_usd'])
        self.assertEqual(audit['aggregate_known_usd'],'0')
        self.assertEqual(audit['unresolved_reserved_usd'],'0.002')
        self.assertEqual(audit['conditional_accounted_aggregate_usd'],'0.002')

    def test_answer_evidence_is_separate_from_frozen_schema(self):
        a,error=candidate(self.answer(evidence=['table[99][0]']))
        self.assertIsNone(error)
        self.assertEqual(evidence_invalid(a['evidence'],{'table':[['x']]}),['table[99][0]'])
        j,error=judge(self.verdict(evidence=['table[1][0][0]']),{'table':[['cost'],['120']]},None)
        self.assertIsNone(error)  # Frozen pointer parser accepts character indexing.
        self.assertEqual(j['effective_verdict'],'supported')
        self.assertEqual(evidence_invalid(j['judgment']['evidence'],{'table':[['cost'],['120']]}),['table[1][0][0]'])

    def test_authored_endpoint_agreement_with_frozen_scoring(self):
        for text,ref,native in [
            (self.answer(),self.reference(),{'value':'25'}),
            (self.answer(value='24'),self.reference(),{'value':'25'}),
            (self.answer(unit='currency_per_share',value='0.2',calculation='1/5'),
             self.reference(unit='currency_per_share',value='0.2'),None),
            (self.answer(scale='million'),self.reference(),None),
            (self.answer(status='ambiguous',value=None,unit='unknown',calculation=''),self.reference(eligible=False),None)]:
            independent=score(text,ref,native); original=frozen_score(text,ref,native)
            for key in ['primary_eligible','schema_valid','reported_numeric_typed_match',
                        'expression_numeric_typed_match','reported_expression_consistent','native_literal_exact']:
                self.assertEqual(independent[key],original[key],key)


if __name__=='__main__': unittest.main()
