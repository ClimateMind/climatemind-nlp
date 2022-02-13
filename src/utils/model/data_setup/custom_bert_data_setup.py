import srsly
import pandas as pd

file_name_answers = "checkin_answers"
file_path_answers = "C://Users//buchh//OneDrive/Desktop//"+file_name_answers+".jsonl"
data = srsly.read_jsonl(file_path_answers)
sent_dict = []
count = 1

for entry in data:
    if "text" in entry:
        text = entry["text"]

    label_arr = []
    label_tup = ()
    if entry['answer'] == "accept":
        for relation in entry['spans']:
            sent_dict_tmp = {}
            sent_dict_tmp["Sentence #"] = "Sentence " + str(count)
            if ("label" in relation) and ("start" in relation) and ("end" in relation):
                sent_dict_tmp["text"] = text
                child_span_start = relation["start"]
                child_span_end = relation["end"]
                word = text[child_span_start:child_span_end]
                if relation["label"] == "base":
                    sent_dict_tmp["word"] = text[child_span_start: child_span_end]
                    sent_dict_tmp["tag"] = relation["label"]
                else:
                    sent_dict_tmp["word"] = text[child_span_start: child_span_end]
                    sent_dict_tmp["tag"] = "O"
            else:
                sent_dict_tmp["word"] = text[child_span_start: child_span_end]
                sent_dict_tmp["tag"] = "O"
            sent_dict.append(sent_dict_tmp)
    count += 1

print(sent_dict)

df = pd.DataFrame.from_dict(sent_dict) 
df.to_csv (r'custom_ent_bert_data.csv', index = False, header=True)