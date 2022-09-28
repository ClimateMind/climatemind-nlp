import srsly
import json

base_path = "/Users/ash/Desktop/PURE/PURE/"
actual_answers_file = "main_3_per_cluster_download.cba617d8-a055-4622-97a3-c194a148cbed"
#actual_file_path = base_path+actual_answers_file+".json"
#actual_file_path = "/Users/ash/Desktop/PURE/PURE/main_3_per_cluster_download.cba617d8-a055-4622-97a3-c194a148cbed.jsonl"
actual_file_path = "/Users/ash/Desktop/PURE/PURE/data1/predictions (1).json"
rel_labels = ["Contributes_To"]

def generate_spans(user=None):
    session = srsly.read_jsonl(actual_file_path)
    rel = {}
    for entry in session:
        text = entry["text"]
        if entry["_session_id"]:
            if text:
                if entry['answer'] == "accept":
                    if entry['_session_id'] == user:
                        for relation in entry['relations']:
                            tmp = []
                            if ("label" in relation) and ("head_span" in relation) and ("child_span" in relation):
                                if relation["label"] in rel_labels:
                                    tmp.append([relation["head_span"]["token_start"], relation["head_span"]["token_end"],
                                                relation["child_span"]["token_start"], relation["child_span"]["token_end"]])
                                    if text not in rel:
                                        rel[text] = tmp
                                    else:
                                        old_rel = rel[text]
                                        rel[text] = old_rel + tmp
    return rel

#Precision P = Number of correctly extracted entity relations / Total number of extracted entity relations
def calc_precision(other_rel, gold_rel):
    precision = 0
    fp = 0
    tp = 0

    for r in other_rel:
        if r in gold_rel:
            o = other_rel[r]
            g = gold_rel[r]

            for x in o:
                if x in g:
                    tp += 1
                else:
                    fp += 1

    precision = (tp / (tp + fp))

    return precision

#Recall R = Number of correctly extracted entity relations / Actual number of extracted entity relations
def calc_recall(other_rel, gold_rel):
    recall = 0
    fn = 0
    tp = 0
    count  = 0

    for r in other_rel:
        if r in gold_rel:
            count += 1
            o = other_rel[r]
            g = gold_rel[r]

            for x in o:
                if x in g:
                    tp += 1
            
            for x in g:
                if x not in o:
                    fn += 1

    recall = (tp / (tp + fn))
    print(count)
    return recall

def calc_f1(precison, recall):

    f1 = 2 * ((precison * recall) / (precison + recall))

    return f1

if __name__ == "__main__":
    other_rel_Sampath = generate_spans("main_3_per_cluster-Sampath")
    other_rel_Nikita = generate_spans("main_3_per_cluster-Nikita")
    gold_rel = generate_spans("main_3_per_cluster-Kameron")

    p_sampath = calc_precision(other_rel_Sampath, gold_rel)
    r_sampath = calc_recall(other_rel_Sampath, gold_rel)
    f1_sampath = calc_f1(p_sampath, r_sampath)
    print(f1_sampath)

    p_nikita = calc_precision(other_rel_Nikita, gold_rel)
    r_nikita = calc_recall(other_rel_Nikita, gold_rel)
    f1_nikita = calc_f1(p_nikita, r_nikita)
    print(f1_nikita)   

