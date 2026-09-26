"""Executive summary: run the provenance-audit command as a Python module."""

from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())
