import srsly
import json
from sklearn.model_selection import train_test_split
import os
import shutil

file_name_answers = "checkin_answers"
file_path_answers = "/Users/ash/Desktop/PURE/PURE/"+file_name_answers+".jsonl"
data = srsly.read_jsonl(file_path_answers)
final_sent = {}
final_sent_arr = []
tmp_index = 0
ents = ["base", "aspect_changing", "change_direction", "type_of"]
total_span_count = 0
total_ent_count = 0

def find_token(tokens, index, is_start):
    for t in tokens:
        if is_start:
            if t["start"] == index:
                return tokens.index(t) + 1
        else:
            if t["end"] == index:
                return tokens.index(t) + 1

for entry in data:
    text = entry["text"]
    if text:
        sentences = []
        if entry['answer'] == "accept":
            if entry['_session_id'] == "main_3_per_cluster-Kameron":
                ner = []
                token_sent = []
                for t in entry["tokens"]:
                    token_sent.append(t["text"])
                sentences.append(token_sent)
                for span in entry['spans']:
                    if ("label" in span) and ("start" in span) and ("end" in span):
                        if span["label"] in ents:
                            #word = text[span["start"]:span["end"]]
                            total_span_count += 1
                            start_index = find_token(entry["tokens"], span["start"], True)
                            end_index = find_token(entry["tokens"], span["end"], False)
                            ner.append([start_index, end_index, span["label"]])
                total_ent_count += len(ner)

                final_sent['doc_key'] = str(tmp_index)
                final_sent['sentences'] = sentences
                final_sent['ner'] = [ner]

            assert total_ent_count == total_span_count
            
            if final_sent:
                final_sent_arr.append(final_sent)
                final_sent = {}
                tmp_index += 1


train, test = train_test_split(final_sent_arr, test_size=0.1)
#val, test = train_test_split(test, test_size=0.5)
data_folder = "data_ent"

#shutil.rmtree(data_folder)
#os.makedirs(data_folder, exist_ok=True)

#with open('./{}/dev.json'.format(data_folder), 'w') as file:
#    for item in val:
#        file.write("%s\n" % json.dumps(item))

with open('./{}/train.json'.format(data_folder), 'w') as file:
    for item in train:
        file.write("%s\n" % json.dumps(item))

with open('./{}/dev.json'.format(data_folder), 'w') as file:
    for item in test:
        file.write("%s\n" % json.dumps(item))

print("Done!")

