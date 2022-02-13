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
tokenizer = RegexpTokenizer(r"\w+")

file_name_answers = "checkin_answers"
file_path_answers = "C://Users//buchh//OneDrive/Desktop//"+file_name_answers+".jsonl"
data = srsly.read_jsonl(file_path_answers)
final_sent = {}
final_sent_arr = []

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
        for relation in entry['spans']:
            ner = []
            if ("label" in relation) and ("start" in relation) and ("end" in relation):
                child_span_start = relation["start"]
                child_span_end = relation["end"]
                word = text[child_span_start:child_span_end]
                if relation["label"] == "base":
                    tokenized_word = tokenizer.tokenize(word)
                    #ner.append([child_span_start, child_span_end, str(relation["label"])])
                    if len(tokenized_word) == 1:
                        ner.append([sentences[0].index(tokenized_word[0]), sentences[0].index(tokenized_word[0]), "PER"])
                    else:
                        ner.append([sentences[0].index(tokenized_word[0]), sentences[0].index(tokenized_word[-1]), "PER"])

        # this will remove all the sentences with no labels (base)
        if ner:
            final_sent['doc_key'] = str(doc_index)
            final_sent['sentences'] = sentences
            final_sent['ner'] = [ner]
            final_sent['relations'] = [[]]

    if final_sent:
        final_sent_arr.append(final_sent)
        final_sent = {}

train, test = train_test_split(final_sent_arr, test_size=0.3)
val, test = train_test_split(test, test_size=0.5)

with open('dev.json', 'w') as file:
    for item in val:
        file.write("%s\n" % json.dumps(item))

with open('train.json', 'w') as file:
    for item in train:
        file.write("%s\n" % json.dumps(item))

with open('test.json', 'w') as file:
    for item in test:
        file.write("%s\n" % json.dumps(item))


print("Done!")

