"""Executive summary: build date-safe FOMC forecast cases and train-only features."""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler


def load_cases(root: Path):
    statements = json.loads((root / "statements.json").read_text())
    yields = pd.read_csv(root / "dgs10.csv")
    yields.columns = ["date", "yield"]
    yields["date"] = pd.to_datetime(yields["date"])
    yields["yield"] = pd.to_numeric(yields["yield"], errors="coerce")
    yields = yields.dropna().sort_values("date").reset_index(drop=True)
    index = {date.strftime("%Y-%m-%d"): i for i, date in enumerate(yields.date)}
    counts = {"duplicate_statement_dates": 0, "no_same_day_yield": 0, "insufficient_history": 0, "no_next_yield": 0}
    cases = []
    seen = set()
    for record in sorted(statements, key=lambda item: (item["date"], item["url"])):
        day = record["date"]
        if day in seen:
            counts["duplicate_statement_dates"] += 1
            continue
        seen.add(day)
        if day not in index:
            counts["no_same_day_yield"] += 1
            continue
        i = index[day]
        if i < 20:
            counts["insufficient_history"] += 1
            continue
        if i + 1 == len(yields):
            counts["no_next_yield"] += 1
            continue
        values = yields["yield"].iloc[i - 20:i + 2].to_numpy(dtype=float)
        # The outcome is never included in the input vector.
        numeric = np.r_[values[20], np.diff(values[:21]) * 100]
        cases.append({"date": day, "url": record["url"], "text_sha256": record["text_sha256"],
                      "text": record["text"], "numeric": numeric.tolist(),
                      "target_bp": float((values[21] - values[20]) * 100)})
    return cases, counts


def make_features(cases):
    dates = np.array([case["date"] for case in cases])
    split = np.where(dates <= "2018-12-31", "train", np.where(dates <= "2022-12-31", "val", "test"))
    train = split == "train"
    if sum(train) <= 100 or sum(split == "val") <= 20 or sum(split == "test") <= 20:
        raise ValueError(f"Too few cases: {dict(zip(*np.unique(split, return_counts=True)))}")
    raw_x = np.array([case["numeric"] for case in cases], dtype=np.float32)
    raw_y = np.array([case["target_bp"] for case in cases], dtype=np.float32)
    xscale = StandardScaler().fit(raw_x[train])
    yscale = StandardScaler().fit(raw_y[train, None])
    tfidf = TfidfVectorizer(max_features=2500, min_df=2, stop_words="english", ngram_range=(1, 2))
    matrix = tfidf.fit_transform([case["text"] for case in cases if case["date"] <= "2018-12-31"])
    dim = min(16, matrix.shape[0] - 1, matrix.shape[1] - 1)
    if dim < 2:
        raise ValueError("Too few text features for SVD")
    svd = TruncatedSVD(n_components=dim, random_state=13).fit(matrix)
    text = svd.transform(tfidf.transform([case["text"] for case in cases])).astype(np.float32)
    tscale = StandardScaler().fit(text[train])
    return {"x": xscale.transform(raw_x).astype(np.float32), "text": tscale.transform(text).astype(np.float32),
            "y": yscale.transform(raw_y[:, None]).ravel().astype(np.float32), "raw_y": raw_y,
            "split": split, "target_center": float(yscale.mean_[0]), "target_scale": float(yscale.scale_[0]),
            "vocab_size": len(tfidf.vocabulary_), "text_dimensions": dim}
