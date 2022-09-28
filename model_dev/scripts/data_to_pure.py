import srsly
import json

file_name_answers = "checkin_answers"
file_path_answers = "/Users/ash/Desktop/PURE/PURE/"+file_name_answers+".jsonl"
rel_labels = ["Contributes_To"]

def get_rel(user):
    tmp_index = 0
    final_sent = {}
    data = srsly.read_jsonl(file_path_answers)
    final_sent_arr = []
    for entry in data:
        text = entry["text"]
        if text:
            sentences = []
            if entry['answer'] == "accept":
                if entry['_session_id'] == user:
                    ner = []
                    rel = []
                    token_sent = []
                    for t in entry["tokens"]:
                        token_sent.append(t["text"])
                    sentences.append(token_sent)
                    for relation in entry['relations']:
                        if ("label" in relation) and ("head_span" in relation) and ("child_span" in relation):
                            if relation["label"] in rel_labels:
                            
                                ner.append([relation["head_span"]["token_start"] + 1, relation["head_span"]["token_end"] + 1, "base"])
                                ner.append([relation["child_span"]["token_start"] + 1, relation["child_span"]["token_end"] + 1, "base"])

                                rel.append([relation["head_span"]["token_start"] + 1, relation["head_span"]["token_end"] + 1,
                                        relation["child_span"]["token_start"] + 1, relation["child_span"]["token_end"] + 1,
                                        "Contributes_To"])

                    final_sent['doc_key'] = str(tmp_index)
                    final_sent['sentences'] = sentences
                    final_sent['ner'] = [ner]
                    final_sent['predicted_ner'] = [ner]
                    final_sent['relations'] = [rel]

            if final_sent:
                final_sent_arr.append(final_sent)
                final_sent = {}
                tmp_index += 1
    
    return final_sent_arr

def gen_preds(user):
    kameron_rel = get_rel("main_3_per_cluster-Kameron")
    user_rel = get_rel("main_3_per_cluster-" + user)

    for k in kameron_rel:
        for u in user_rel:
            if k["sentences"] == u["sentences"]:
                u["predicted_relations"] = u["relations"]
                u["relations"] = k["relations"]

    for ur in user_rel:
        if "predicted_relations" not in ur.keys():
            user_rel.remove(ur)

    for ud in user_rel:
        json_object = json.dumps(ud)
        with open("predictions_"+user+".json", "a") as outfile:
            outfile.write(json_object + "\n")


gen_preds("Nikita")
gen_preds("Sampath")