"""Executive summary: run the frozen public FOMC forecasting pilot."""
from pathlib import Path

from looped_forecast.experiment import run


if __name__ == "__main__":
    run(Path("data/fomc-looped-pilot-v1"), Path("outputs/looped-forecast-pilot-v1"))
