"""Executive summary: create a non-overwritable protocol and code freeze without generating instances."""

import json
from independent_finance.protocol import freeze

if __name__ == "__main__":
    record = freeze()
    print(json.dumps({key: record[key] for key in ("frozen_at_utc", "python", "scheduled", "code_revision")}))
