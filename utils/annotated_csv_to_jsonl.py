#making jsonl file from csv of annotated sentences

import json
import pandas as pd
import srsly
import random


#file_path = "sentences_for_NER_from_cause_effect_classifier_climateBERT_predictions_for_sentences_from_effect_tag_articles.csv"
file_path = "15 April 2021 - cm_cause_effect_rel_download.45fa2a75-cc43-4236-a0e8-b922028c9ca1 - 200_sentences_cause_effect_rel_150421.csv"#"pocket_pred.csv"


data = pd.read_csv(file_path, sep = ",")

columns = list(data.columns)


output_file_path = file_path.replace(".csv", ".jsonl",1)


json_data = []

for index, row in data.iterrows():
	line_contents = {} #each dictionary holds all information of a single line
	
	for column in columns:
		line_contents[column] = row[column]
	json_data.append(line_contents)

#if want to randomize the list
json_data_shuffled = random.sample(json_data, len(json_data))


srsly.write_jsonl(output_file_path, json_data)
srsly.write_jsonl('randomized_'+output_file_path, json_data_shuffled)


