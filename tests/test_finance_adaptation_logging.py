"""Executive summary: closing concurrent optimizer logs must preserve process streams."""
import json
import sys
from concurrent.futures import ThreadPoolExecutor

from run_finance_adaptation_v2 import FileLogger


def test_parallel_optimizer_logs_do_not_redirect_or_close_stdout(tmp_path):
    before = sys.stdout, sys.stderr

    def write(index):
        logger = FileLogger(tmp_path / f'{index}.log')
        logger.log(f'optimizer {index}')
        logger.close()

    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(write, range(4)))
    assert (sys.stdout, sys.stderr) == before
    assert not sys.stdout.closed and not sys.stderr.closed
    for index in range(4):
        assert json.loads((tmp_path / f'{index}.log').read_text()) == f'optimizer {index}'
