#making jsonl file from csv of sentences

import json
import pandas as pd

#file_path = "sentences_for_NER_from_cause_effect_classifier_climateBERT_predictions_for_sentences_from_effect_tag_articles.csv"
file_path = "pocket_pred.csv"

#read in the csv file as a dataframe and convert to list
#sentences = pd.read_csv(file_path, sep = ",", header=None, names=["sentence"])

sentences = pd.read_csv(file_path, sep = ",")

sentence_list = sentences[sentences.Pred == 1].text.tolist() #sentences.sentence.tolist()


#new_examples = []
#for text in sentences:
#	new_examples.append({"text": text})
#srsly.write_jsonl("./NER_team_task_number_1_base_entity_labeling.jsonl", new_examples)

#output_file_path = "./NER_team_task_number_1_base_entity_labeling.jsonl"

output_file_path = "./ClimateBERT_cause_effect_prediction_pos_sentences.jsonl"

text_list = []
for sentence in sentence_list:
	text_list.append({"text": sentence})


with open(output_file_path, 'w') as f:
    for item in text_list:
        f.write(json.dumps(item) + "\n")


