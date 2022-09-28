import srsly
import json
from sklearn.model_selection import train_test_split
import os

file_name_answers = "gold_standard"
file_path_answers = "/Users/ash/Desktop/PURE/PURE/new_data/"+file_name_answers+".jsonl"
data = srsly.read_jsonl(file_path_answers)
final_sent = {}
final_sent_arr = []
final_sent_left_to_right = []
final_sent_right_to_left = []
rel_labels = ["Contributes_To"]
ents = ["base", "aspect_changing", "change_direction", "type_of"]
tmp_index = 0
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
            if entry['_session_id'] in ["main_3_per_cluster-Kameron", "main_batchF-KameronRodrigues"]:
                ner = []
                rel = []
                token_sent = []
                for t in entry["tokens"]:
                    token_sent.append(t["text"])
                sentences.append(token_sent)
                left_to_right = 0
                right_to_left = 0

                for span in entry['spans']:
                    if ("label" in span) and ("start" in span) and ("end" in span):
                        if span["label"] in ents:
                            # word = text[span["start"]:span["end"]]
                            total_span_count += 1
                            start_index = find_token(entry["tokens"], span["start"], True)
                            end_index = find_token(entry["tokens"], span["end"], False)
                            ner.append([start_index, end_index, span["label"]])
                
                for relation in entry['relations']:
                    if ("label" in relation) and ("head_span" in relation) and ("child_span" in relation):
                        if relation["label"] in rel_labels:
                            tmp = []
                            head_span_start = relation["head_span"]["start"]
                            head_span_end = relation["head_span"]["end"]
                            child_span_start = relation["child_span"]["start"]
                            child_span_end = relation["child_span"]["end"]
                            head_word = text[head_span_start:head_span_end]
                            child_word = text[child_span_start:child_span_end]
                            
                            if head_span_start > child_span_start:
                                right_to_left += 1
                            else:
                                left_to_right += 1
                            
                            # ner.append([relation["head_span"]["token_start"] + 1, relation["head_span"]["token_end"] + 1, "base"])
                            # ner.append([relation["child_span"]["token_start"] + 1, relation["child_span"]["token_end"] + 1, "base"])

                            rel.append([relation["head_span"]["token_start"] + 1, relation["head_span"]["token_end"] + 1,
                                       relation["child_span"]["token_start"] + 1, relation["child_span"]["token_end"] + 1,
                                       "Contributes_To"])

                final_sent['doc_key'] = str(tmp_index)
                final_sent['sentences'] = sentences
                final_sent['ner'] = [ner]
                # final_sent['predicted_ner'] = [ner]
                final_sent['relations'] = [rel]
                total_ent_count += len(ner)
                # final_sent['right_to_left'] = right_to_left
                # final_sent['left_to_right'] = left_to_right

        assert total_ent_count == total_span_count

        if final_sent:
            final_sent_arr.append(final_sent)
            final_sent = {}
            tmp_index += 1

train, test = train_test_split(final_sent_arr, test_size=0.1)
total_sent = len(final_sent_arr)

data_folder = "data"
os.makedirs(data_folder, exist_ok=True)

with open('./{}/train.json'.format(data_folder), 'w') as file:
    for item in train:
        # del item["right_to_left"]
        # del item["left_to_right"]
        file.write("%s\n" % json.dumps(item))

with open('./{}/dev.json'.format(data_folder), 'w') as file:
    for item in test:
        # del item["right_to_left"]
        # del item["left_to_right"]
        file.write("%s\n" % json.dumps(item))

print("Total sentences: {}".format(total_sent))
print("Done!")
