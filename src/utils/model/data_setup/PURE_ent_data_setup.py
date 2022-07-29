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

from nltk.util import pr
import srsly
import json
#from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
from nltk.tokenize import RegexpTokenizer
import os
import shutil
tokenizer = RegexpTokenizer(r"\w+")

file_name_answers = "checkin_answers"
file_path_answers = "/Users/ash/Desktop/PURE/PURE/"+file_name_answers+".jsonl"
data = srsly.read_jsonl(file_path_answers)
final_sent = {}
final_sent_arr = []
tmp_index = 0
ents = ["base"]

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
            for span in entry['spans']:
                if ("label" in span) and ("start" in span) and ("end" in span):
                    child_span_start = span["start"]
                    child_span_end = span["end"]
                    word = text[child_span_start:child_span_end]
                    if span["label"] in ents:
                        tokenized_word = tokenizer.tokenize(word)
                        if len(tokenized_word) == 1:
                            if [int(sentences[0].index(tokenized_word[0])) + 1, int(sentences[0].index(tokenized_word[0])) + 1, span["label"]] not in ner:
                                ner.append([int(sentences[0].index(tokenized_word[0])) + 1, int(sentences[0].index(tokenized_word[0])) + 1, span["label"]])
                        else:
                            if [int(sentences[0].index(tokenized_word[0])) + 1, int(sentences[0].index(tokenized_word[-1])) + 1, "BASE"] not in ner:
                                ner.append([int(sentences[0].index(tokenized_word[0])) + 1, int(sentences[0].index(tokenized_word[-1])) + 1, span["label"]])

            final_sent['doc_key'] = str(tmp_index)
            final_sent['sentences'] = sentences
            final_sent['ner'] = [ner]

        if final_sent:
            final_sent_arr.append(final_sent)
            final_sent = {}
            tmp_index += 1


train, test = train_test_split(final_sent_arr, test_size=0.1)
val, test = train_test_split(test, test_size=0.5)
data_folder = "data_ent"

shutil.rmtree(data_folder)
os.makedirs(data_folder, exist_ok=True)

with open('./{}/dev.json'.format(data_folder), 'w') as file:
    for item in val:
        file.write("%s\n" % json.dumps(item))

with open('./{}/train.json'.format(data_folder), 'w') as file:
    for item in train:
        file.write("%s\n" % json.dumps(item))

with open('./{}/test.json'.format(data_folder), 'w') as file:
    for item in test:
        file.write("%s\n" % json.dumps(item))

print("Done!")

