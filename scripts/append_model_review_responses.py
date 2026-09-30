"""Executive summary: attach anonymous saved model answers to the prospective human packet.

This requires the complete original three-model panel. It writes separate keys;
no source label or model name enters a reviewer-facing candidate file.
"""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "outputs/model-grading-v1"
REVIEW = ROOT / "outputs/model-grading-review"
MODELS = ("qwen3-1.7b", "qwen2.5-coder-3b", "deepseek-v3.2")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    selection = [json.loads(s) for s in (STUDY / "selection.jsonl").read_text().splitlines()]
    expected = {r["case_id"] for r in selection}
    assert len(expected) == 200
    lookup, ledger_hashes = {}, {}
    for model in MODELS:
        path = STUDY / f"{model}_responses.jsonl"
        raw = path.read_bytes()
        rows = [json.loads(s) for s in raw.decode().splitlines()]
        assert len(rows) == 200 and {r["case_id"] for r in rows} == expected
        assert all(r["model_key"] == model for r in rows)
        lookup.update({(r["case_id"], model): r for r in rows})
        ledger_hashes[path.name] = sha(raw)
    packet = REVIEW / "response-packet"
    packet.mkdir(exist_ok=True)
    keys = json.loads((REVIEW / "ANSWER_KEY.json").read_text())["items"]
    primary = [r for r in keys if r["role"] == "primary_panel"]
    assert len(primary) == 8
    index = ["## Executive summary (read this first)", "",
             "Eight anonymous questions and twenty-four unchanged candidate answers.",
             "Human review is pending. Read the question and calculate its answer before",
             "opening the candidate files. Do not open RESPONSE_KEY.json or ANSWER_KEY.json.", "",
             "The original financial-question packet includes four further input-ambiguity",
             "questions without model answers. Those are supplementary to this response packet.", ""]
    answer_key = []
    system = json.loads((STUDY / "selection_manifest.json").read_text())["system_prompt"]
    for question in primary:
        rid = question["review_id"]
        entries = [lookup[(question["source_id"], m)] for m in MODELS]
        entries.sort(key=lambda r: sha(("anonymous-candidates-v1:" + rid + r["model_key"]).encode()))
        index.append(f"- [{rid}]({rid}.md)")
        body = ["## Executive summary (read this first)", "", f"Financial question {rid}.", "",
                question["question"], "", "Independent assumptions, formula, value and units: ____________________", "",
                "Common instructions given to every candidate system:", "", system, "", "Anonymous candidates:", ""]
        for label, response in zip("ABC", entries):
            name = f"{rid}_{label}.md"
            body.append(f"- [Candidate {label}]({name})")
            text = response["text"]
            fence = "`" * max(3, 1 + max((len(s) for s in re.findall(r"`+", text)), default=0))
            completion = "complete" if response["finish_reason"] in {"stop", "eos"} else "unfinished or failed"
            candidate = ["## Executive summary (read this first)", "", f"Anonymous candidate {label} for {rid}.", "",
                         "The text below is preserved exactly. An empty or unfinished response does",
                         "not become a completed answer through human review.", "", f"Completion status: {completion}", "",
                         fence + "text", text, fence, "",
                         "Final-value correctness: ____________________", "Unit correctness: ____________________",
                         "Requested-precision compliance: ____________________", "Reasoning support: ____________________",
                         "Uncertainty and comments: ____________________", ""]
            (packet / name).write_text("\n".join(candidate))
            answer_key.append({"review_id": rid, "candidate": label, "source_id": question["source_id"],
                               "model_key": response["model_key"], "finish_reason": response["finish_reason"],
                               "response_text_sha256": sha(text.encode()), "candidate_file": name})
        (packet / f"{rid}.md").write_text("\n".join(body) + "\n")
    (packet / "README.md").write_text("\n".join(index) + "\n")
    (REVIEW / "RESPONSE_KEY.json").write_text(json.dumps({"status": "prepared; no human annotations", "items": answer_key}, indent=2) + "\n")
    manifest = {"status": "prepared; no human review or contact", "questions": 8, "candidate_responses": 24,
                "selection_sha256": sha((STUDY / "selection.jsonl").read_bytes()), "ledger_sha256": ledger_hashes,
                "script_sha256": sha(Path(__file__).read_bytes()),
                "file_sha256": {p.name: sha(p.read_bytes()) for p in sorted(packet.glob("*.md"))},
                "response_key_sha256": sha((REVIEW / "RESPONSE_KEY.json").read_bytes())}
    (REVIEW / "response-packet-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"questions": 8, "anonymous_candidates": 24, "status": manifest["status"]}))


if __name__ == "__main__":
    main()
