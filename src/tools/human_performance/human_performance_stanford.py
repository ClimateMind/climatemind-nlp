import json
from pathlib import Path

from nervaluate import Evaluator

base_path = Path(__file__).parents[3] / "data"
base_path.mkdir(exist_ok=True)

gold_path = base_path / "main_3_per_cluster_download.cba617d8-a055-4622-97a3-c194a148cbed.jsonl"
silver_paths = list(base_path.glob("main_batch*.jsonl"))
print(silver_paths)
all_labels = ['base', 'change_direction', 'type_of', 'aspect_changing']

with open(gold_path, "r") as f:
    gold_lines = [json.loads(x) for x in f.readlines()]

silver_lines = []

for silver_path in silver_paths:
    with open(silver_path, "r") as f:
        silver_lines += [json.loads(x) for x in f.readlines()]

gold_standard_session = "main_3_per_cluster-Kameron"
gold_samples = [x for x in gold_lines if x["_session_id"] == gold_standard_session]
silver_sessions = ["SummerRoyal", "JuneChoi", "LauraAnderson", "MayaNoesen", "HeidiHirsh", "MayaNoesen",
                  "AnnaKasperovich", "HeidiHirsh"]

print(silver_lines)
print(set([x["_session_id"] for x in silver_lines]))

for session in silver_sessions:
    print(session)
    print(len(set([x["original_md_text"] for x in silver_lines if session in x["_session_id"]])
              .intersection([x["original_md_text"] for x in gold_lines])))
    # print(sorted([x["original_md_text"] for x in silver_lines if session in x["_session_id"]]))
    # print(sorted([x["original_md_text"] for x in gold_lines]))

    # There is no overlap between the gold annotations from ain_3_per_cluster-Kameron and the silver annotations from
    # batchX
