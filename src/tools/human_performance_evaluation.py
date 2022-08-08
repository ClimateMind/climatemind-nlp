import json
from pathlib import Path

from nervaluate import Evaluator

base_path = Path(__file__).parents[2] / "data"
data_path = base_path / "main_3_per_cluster_download.cba617d8-a055-4622-97a3-c194a148cbed.jsonl"

with open(data_path, "r") as f:
    lines = [json.loads(x) for x in f.readlines()]

gold_standard_session = "main_3_per_cluster-Kameron"
other_sessions = ["main_3_per_cluster-Sampath", "main_3_per_cluster-Nikita"]

all_labels = ['where', 'to_whom', 'base', 'change_direction', 'confidence', 'when', 'type_of', 'aspect_changing',
              'predicate', 'effect_size']

for other_session in other_sessions:
    other_session_subset = [x for x in lines if x["_session_id"] == other_session]
    gold_session_subset = [x for x in lines if x["_session_id"] == gold_standard_session]

    other_session_subset.sort(key=lambda x: x["document_index"])
    gold_session_subset.sort(key=lambda x: x["document_index"])

    assert [x["document_index"] for x in other_session_subset] == [x["document_index"] for x in gold_session_subset]

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
