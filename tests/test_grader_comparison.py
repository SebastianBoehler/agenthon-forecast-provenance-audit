"""Executive summary: guard unsupported syntax, exact equivalence and grader ablations."""

from fractions import Fraction
import unittest
from grader_comparison.scalars import scalar, controls, decimal, final_scalar
from grader_comparison.native import load, normalized_comparison


class ComparisonTests(unittest.TestCase):
    def test_exact_value_and_unsupported_syntax(self):
        for text in ("-1/2", "-.5", r"-\frac{1}{2}", r"\boxed{-0.5}"):
            self.assertEqual(scalar(text), Fraction(-1, 2))
        for text in ("1/0", "1 dollar", "{1, 2}", "sqrt(2)", "1.2e3", "NaN"):
            self.assertIsNone(scalar(text))
        self.assertNotEqual(scalar("1/3"), scalar("0.3333"))
        self.assertIsNone(decimal(Fraction(1, 3)))

    def test_final_line_cannot_recover_earlier_answer(self):
        self.assertEqual(final_scalar("Step: 42\nFinal Answer: -1/2"), "-1/2")
        self.assertIsNone(final_scalar("Final Answer: 42\nActually unsure."))

    def test_controls_are_value_checked(self):
        for gold in ("0", "-1.5", "1/3", r"\frac{2}{7}"):
            for name, candidate, equal in controls(gold):
                self.assertEqual(equal, name in {"identity", "canonical", "unreduced", "terminating_decimal"})
                self.assertEqual(equal, Fraction(candidate.replace(r"\frac{2}{7}", "2/7")) == scalar(gold))

    def test_pinned_collisions_and_meaningful_ablation(self):
        env, dataset = load()
        for left, right in (("1.2", "1.8"), ("-1", "+1")):
            self.assertTrue(env["compare_answers"](left, "Final Answer: " + right, dataset)[2])
            self.assertTrue(normalized_comparison(env, left, right)[0])
            self.assertFalse(normalized_comparison(env, left, right, ("intpart", "digits"))[0])
            self.assertNotEqual(scalar(left), scalar(right))


if __name__ == "__main__":
    unittest.main()
