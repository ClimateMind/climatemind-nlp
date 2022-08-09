"""
repo to install and setup PURE: https://github.com/princeton-nlp/PURE

command used to train:
python run_entity.py \
    --do_train --do_eval --eval_test \
    --learning_rate=1e-5 \
    --task_learning_rate=5e-4 \
    --train_batch_size=16 \
    --context_window 100 \
    --task ace05 \
    --data_dir /content/ \
    --model bert-base-uncased \
    --output_dir /content/
"""

import srsly
import json
#from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
from nltk.tokenize import RegexpTokenizer
import os
import random
import numpy as np
tokenizer = RegexpTokenizer(r"\w+")

file_name_answers = "checkin_answers"
file_path_answers = "/Users/ash/Desktop/PURE/PURE/"+file_name_answers+".jsonl"
data = srsly.read_jsonl(file_path_answers)
final_sent = {}
final_sent_arr = []
final_sent_left_to_right = []
final_sent_right_to_left = []
rel_labels = ["Contributes_To"]
tmp_index = 0

# finding the sentence from where no sentences have right_to_left relationship
def get_right_to_left_boundary(sorted_by_direction):
    for s in sorted_by_direction:
        if s['right_to_left'] == 0:
            return sorted_by_direction.index(s)

for entry in data:
    if "text" in entry:
        text = entry["text"]
    else:
        text = ""
        throw("NO 'text' field encountered! This field is necessary for the rest of the script to work! Please fix this and then run this script.")

    if "document_index" in entry:
        doc_index = entry['document_index']
    else:
        doc_index = -1
    sentences = [tokenizer.tokenize(text)]
    if entry['answer'] == "accept":
        if entry['_session_id'] == "main_3_per_cluster-Kameron":
            ner = []
            rel = []
            left_to_right = 0
            right_to_left = 0
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

                        head_word = text[head_span_start:head_span_end]
                        child_word = text[child_span_start:child_span_end]
                        
                        #print(text)
                        #print(relation)
                        #print(head_word)
                        #print(child_word)
                        if head_span_start > child_span_start:
                            #print("right_to_left")
                            right_to_left += 1
                        else:
                            #print("left_to_right")
                            left_to_right += 1
                        #print("=====")
                        
                        tokenized_head_word = tokenizer.tokenize(head_word)
                        if len(tokenized_head_word) == 1:
                            tmp.append(int(sentences[0].index(tokenized_head_word[0])) + 1)
                            tmp.append(int(sentences[0].index(tokenized_head_word[0])) + 1)
                            if [int(sentences[0].index(tokenized_head_word[0])) + 1, int(sentences[0].index(tokenized_head_word[0])) + 1, "BASE"] not in ner:
                                ner.append([int(sentences[0].index(tokenized_head_word[0])) + 1, int(sentences[0].index(tokenized_head_word[0])) + 1, "BASE"])
                        else:
                            tmp.append(int(sentences[0].index(tokenized_head_word[0])) + 1)
                            tmp.append(int(sentences[0].index(tokenized_head_word[-1])) + 1)
                            if [int(sentences[0].index(tokenized_head_word[0])) + 1, int(sentences[0].index(tokenized_head_word[-1])) + 1, "BASE"] not in ner:
                                ner.append([int(sentences[0].index(tokenized_head_word[0])) + 1, int(sentences[0].index(tokenized_head_word[-1])) + 1, "BASE"])

                        tokenized_child_word = tokenizer.tokenize(child_word)
                        if len(tokenized_child_word) == 1:
                            tmp.append(int(sentences[0].index(tokenized_child_word[0])) + 1)
                            tmp.append(int(sentences[0].index(tokenized_child_word[0])) + 1)
                            if [int(sentences[0].index(tokenized_child_word[0])) + 1, int(sentences[0].index(tokenized_child_word[0])) + 1, "BASE"] not in ner:
                                ner.append([int(sentences[0].index(tokenized_child_word[0])) + 1, int(sentences[0].index(tokenized_child_word[0])) + 1, "BASE"])
                        else:
                            tmp.append(int(sentences[0].index(tokenized_child_word[0])) + 1)
                            tmp.append(int(sentences[0].index(tokenized_child_word[-1])) + 1)
                            if [int(sentences[0].index(tokenized_child_word[0])) + 1, int(sentences[0].index(tokenized_child_word[-1])) + 1, "BASE"] not in ner:
                                ner.append([int(sentences[0].index(tokenized_child_word[0])) + 1, int(sentences[0].index(tokenized_child_word[-1])) + 1, "BASE"])
                        tmp.append(relation["label"])
                        rel.append(tmp)

            final_sent['doc_key'] = str(tmp_index)
            final_sent['sentences'] = sentences
            final_sent['ner'] = [ner]
            final_sent['predicted_ner'] = [ner]
            final_sent['relations'] = [rel]
            final_sent['right_to_left'] = right_to_left
            final_sent['left_to_right'] = left_to_right

            #print(final_sent)
            #print("===")

        if final_sent:
            final_sent_arr.append(final_sent)
            final_sent = {}
            tmp_index += 1
    
"""
train, test = train_test_split(final_sent_arr, test_size=0.1)
val, test = train_test_split(test, test_size=0.5)
"""
"""
    Scikit-learn's train_test_split will shuffle the data before creating the tran-test sets, which will result in inconsistent number of right_to_left and left_to_right
    relationships in test, train, and dev sets. To fix that, first the array with all the sentences will be sorted by right_to_left counter
    for the respective sentence, and then an index after which no sentence has right_to_let relationship is found. We have to make sure that majority of right_to_left relationships
    are in train set. In this case 50% sentences containing 
"""

total_sent = len(final_sent_arr)

# sorting the array with right_to_left count
sorted_by_direction = sorted(final_sent_arr, key=lambda d: d['right_to_left'], reverse=True) 

# getting the index after which no sentence will have a right_to_left relationship
right_to_left_boundary = get_right_to_left_boundary(sorted_by_direction)
right_to_left_train_boundary = int(right_to_left_boundary/2)

# 90% of total data will be used in training the model
train_length = int((total_sent*90)/100)
#print("train_length: {}".format(train_length))
#print("right_to_left_boundary: {}".format(right_to_left_boundary))
#print("right_to_left_train_boundary: {}".format(right_to_left_train_boundary))

right_to_left_first_half = sorted_by_direction[:right_to_left_train_boundary]
newarr = sorted_by_direction[right_to_left_train_boundary:]
right_to_left_second_half = random.sample(newarr, len(newarr))
#right_to_left_second_half = np.random.shuffle(newarr)

remaining_train_data = train_length - right_to_left_train_boundary
#print("remaining_train_data: {}".format(remaining_train_data))
#print(right_to_left_second_half)
train = right_to_left_first_half + right_to_left_second_half[:remaining_train_data]

val_length = int(((total_sent-train_length)*50)/100)
val = right_to_left_second_half[remaining_train_data:remaining_train_data+val_length]
test = right_to_left_second_half[remaining_train_data+val_length:]

#print(len(train))
#print(len(test))
#print(len(val))

assert (len(train) + len(test) + len(val)) == total_sent

data_folder = "data"

os.makedirs(data_folder, exist_ok=True)

with open('./{}/dev.json'.format(data_folder), 'w') as file:
    for item in val:
        del item["right_to_left"]
        del item["left_to_right"]
        file.write("%s\n" % json.dumps(item))

with open('./{}/ent_pred_dev.json'.format(data_folder), 'w') as file:
    for item in val:
        #del item["right_to_left"]
        #del item["left_to_right"]
        file.write("%s\n" % json.dumps(item))

with open('./{}/train.json'.format(data_folder), 'w') as file:
    for item in train:
        del item["right_to_left"]
        del item["left_to_right"]
        file.write("%s\n" % json.dumps(item))

with open('./{}/test.json'.format(data_folder), 'w') as file:
    for item in test:
        del item["right_to_left"]
        del item["left_to_right"]
        file.write("%s\n" % json.dumps(item))

with open('./{}/ent_pred_test.json'.format(data_folder), 'w') as file:
    for item in test:
        #del item["right_to_left"]
        #del item["left_to_right"]
        file.write("%s\n" % json.dumps(item))

print("Total sentences: {}".format(total_sent))
print("Done!")

