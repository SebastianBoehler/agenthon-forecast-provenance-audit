"""Executive summary: API-cost replay stays exact across Python versions and rejects changed charges."""

from decimal import Decimal
import unittest
from unittest.mock import patch

import replay_final_extensions as extension


class FinalExtensionReplayTests(unittest.TestCase):
    def test_recorded_cost_is_exact_and_order_independent(self):
        usage = extension.read(extension.BANK / 'api_usage.jsonl')
        expected = Decimal('0.00286891')
        self.assertEqual(extension.api_cost_total(usage), expected)
        self.assertEqual(extension.api_cost_total(list(reversed(usage))), expected)

    def test_changed_charge_is_rejected(self):
        original_read = extension.read

        def changed_usage(path):
            rows = original_read(path)
            if path.name == 'api_usage.jsonl':
                rows[0]['cost_usd'] += 0.00000001
            return rows

        with patch.object(extension, 'read', side_effect=changed_usage):
            with self.assertRaisesRegex(ValueError, 'API usage ledger changed'):
                extension.replay()


if __name__ == '__main__':
    unittest.main()
