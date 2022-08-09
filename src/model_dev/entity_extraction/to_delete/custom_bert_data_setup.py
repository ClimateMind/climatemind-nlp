import srsly
import pandas as pd
import os

file_name_answers = "main_3_per_cluster_download.66081fcf-3ef5-48ea-97e0-49298d29b477"
file_path_answers = "/Users/ash/Desktop/"+file_name_answers+".jsonl"
data = srsly.read_jsonl(file_path_answers)
data1 = srsly.read_jsonl(file_path_answers)
sent_dict_train = []
sent_dict_test = []
count = 1
tot_len = 0

for n in data1:
    if n['answer'] == "accept":
        tot_len += 1

print(tot_len)

# 70% training, 30% testing
training_data_index = int(tot_len*0.7)
print()
for entry in data:
    #print(count)
    #print(training_data_index)
    #print("-----")

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
            if training_data_index != 0:
                sent_dict_train.append(sent_dict_tmp)
            else:
                sent_dict_test.append(sent_dict_tmp)
    count += 1
    if training_data_index > 0:
        training_data_index -= 1

df_train = pd.DataFrame.from_dict(sent_dict_train)
print(df_train.iloc[-1])
df_train.to_csv(r'custom_ent_bert_train_data.csv', index = False, header=True)

df_test = pd.DataFrame.from_dict(sent_dict_test) 
df_test.to_csv(r'custom_ent_bert_test_data.csv', index = False, header=True)

