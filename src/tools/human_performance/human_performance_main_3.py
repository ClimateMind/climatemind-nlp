import json
from pathlib import Path

from nervaluate import Evaluator

base_path = Path(__file__).parents[3] / "data"
data_path = base_path / "main_3_per_cluster_download.cba617d8-a055-4622-97a3-c194a148cbed.jsonl"
data_path.mkdir(exist_ok=True)

with open(data_path, "r") as f:
    lines = [json.loads(x) for x in f.readlines()]

gold_standard_session = "main_3_per_cluster-Kameron"
other_sessions = ["main_3_per_cluster-Sampath", "main_3_per_cluster-Nikita"]

all_labels = ['base', 'change_direction', 'type_of', 'aspect_changing']

for other_session in other_sessions:
    other_session_subset = [x for x in lines if x["_session_id"] == other_session]
    gold_session_subset = [x for x in lines if x["_session_id"] == gold_standard_session]

    other_session_subset.sort(key=lambda x: x["original_md_text"])
    gold_session_subset.sort(key=lambda x: x["original_md_text"])

    assert [x["original_md_text"] for x in other_session_subset] == [x["original_md_text"] for x in gold_session_subset]

    other_spans = [[a for a in x["spans"] if all(k in a for k in ["start", "end", "label"])] for x in
                   other_session_subset]
    gold_spans = [[a for a in x["spans"] if all(k in a for k in ["start", "end", "label"])] for x in
                  gold_session_subset]

    evaluator = Evaluator(gold_spans, other_spans, tags=all_labels)

    results, results_per_tag = evaluator.evaluate()

    with open(base_path / f"results_{other_session}.json", "w") as f:
        json.dump(results, f, indent=4)
    with open(base_path / f"results_per_tag_{other_session}.json", "w") as f:
        json.dump(results_per_tag, f, indent=4)
