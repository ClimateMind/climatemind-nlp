#deduplicate edges

import pandas as pd
#import uuid

def string2numeric_hash(text):
    import hashlib
    text = text.encode('utf-8')
    return int(hashlib.md5(text).hexdigest()[:8], 16)


data_file = "/Users/kameronr/Documents/personal/climate change outreach/new uploads/NLP data/main_3_per_cluster_outputs/node initial standardization data.csv"
data = pd.read_csv(data_file, encoding='utf-8')

#add unique identifiers for the unique and complete climate concepts

#filter to just rows with change_direction of 'up' and 'down' and base that are not '?'
standardized_data = data[  ((data['change_direction (to standardize)'] == "up")  |   (data['change_direction (to standardize)'] == "down")) & (data['base (to standardize)'] != "?") ]


#add uuids for the fields combined 'change_direction (standardized v1)', 'type_of (standardized v1)', 'base (standardized v1)', 'aspect_changing (standardized v1)'
cols = ['change_direction (standardized v1)','type_of (standardized v1)','base (standardized v1)','aspect_changing (standardized v1)']
relevant_strings = standardized_data['climate_concept_string_representation'] = standardized_data[cols].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)

standardized_data['climate_concept_id'] = standardized_data.apply(lambda row: string2numeric_hash(row["climate_concept_string_representation"]), axis=1)

standardized_data['base_id'] = standardized_data.apply(lambda row: row["base_id"].strip("[|]|'"), axis=1)

standardized_data.to_csv("/Users/kameronr/Documents/personal/climate change outreach/new uploads/NLP data/main_3_per_cluster_outputs/node standardization data processed v1.csv")


#read in raw data 
#import jsonl file
import srsly
import itertools
import copy
import csv


#file_path = "entity_checkin_one_download.49863984-3905-4e3d-a059-4b2ef0004267.jsonl" 
#file_name = "entity_checkin_one_download.850cb48f-8027-4380-a497-fc0f31e64f48"
file_name = "/Users/kameronr/Documents/personal/climate change outreach/new uploads/NLP data/main_3_per_cluster_outputs/main_3_per_cluster_download.cba617d8-a055-4622-97a3-c194a148cbed"
file_path = file_name + ".jsonl"

data = srsly.read_jsonl(file_path)

keep_lines = {}

data_for_csv = []

csv_columns = [
	"username",
	"text",
	"original_text",
	"source",
	"document_id",
	"sentence_id",
	"relation_type",
	"head_span_start",
	"head_span_end",
	"head_span_label",
	"child_span_start",
	"child_span_end",
	"child_span_label"
]	

csv_lines = []

#append column headers to csv line list
csv_lines.append(csv_columns)


#for each sentence entry
for entry in data:
	if "text" in entry:
		text = entry["text"]
	else: throw("NO 'text' field encountered! This field is necessary for the rest of the script to work! Please fix this and then run this script.")


	if "original_md_text" in entry:
		original_text = entry["original_md_text"]
	else: 
		original_text = "None because no text modifications made. See 'text' field for the original text."


	if "url" in entry:
		source = entry["url"]
	else: 
		source = "url missing!"


	if "document_index" in entry:
		document_id = entry["document_index"]
	else: 
		document_id = "document index missing!"


	if "md_sentence_index" in entry:
		sentence_id = entry["md_sentence_index"]
	else: 
		sentence_id = "md_sentence_index missing!"

	if "_session_id" in entry:
		username = entry["_session_id"]
	else: 
		username = "_session_id missing!"


	# relation_list = []

	for relation in entry["relations"]:
		if "label" in relation:
			if relation["label"]:
				#check if the "child_span" has the "label" of "base_entity" and if does, then check if that child base_entity is in the base_entity_dict and if not then add that child base_entity
				if "child_span" in relation and "head_span" in relation:
					if "label" in relation["child_span"] and "label" in relation["head_span"]:
						relation_type = relation["label"]
						head_span_start = relation["head_span"]["start"] #assumes "start" is present even though doesn't check for it! And assumes just 1 start. This could be improved by checking first for "start"
						head_span_end = relation["head_span"]["end"] #assumes "end" is present even though doesn't check for it! And assumes just 1 end. This could be improved by checking first for "end"
						head_span_label = relation["head_span"]["label"]
						child_span_start = relation["child_span"]["start"] #assumes "start" is present even though doesn't check for it! And assumes just 1 start. This could be improved by checking first for "start"
						child_span_end = relation["child_span"]["end"] #assumes "end" is present even though doesn't check for it! And assumes just 1 end. This could be improved by checking first for "end"
						child_span_label = relation["child_span"]["label"]
						csv_line = [username, text, original_text, source, document_id, sentence_id, relation_type, head_span_start, head_span_end, head_span_label, child_span_start, child_span_end, child_span_label]
						csv_lines.append(csv_line)


#output the lines in csv_lines
output_file_name = file_name + '_relation_export.csv'

with open(output_file_name, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(csv_lines)




relation_export_data = pd.read_csv(output_file_name)



#filter to just username = 'main_3_per_cluster-Kameron' and relation_type = 'Contributes_To'
causal_relation_export_data = relation_export_data[  ( relation_export_data['username'] == "main_3_per_cluster-Kameron" ) & ( relation_export_data['relation_type'] == "Contributes_To" ) ]


head_cols = ['document_id','sentence_id','head_span_start','head_span_end']
child_cols = ['document_id', 'sentence_id', 'child_span_start', 'child_span_end']

causal_relation_export_data['head_id'] = causal_relation_export_data[head_cols].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)

causal_relation_export_data['child_id'] = causal_relation_export_data[child_cols].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)




#left join causal_relation_export_data and standardized_data by document_id sentence_id span_start span_end for head span start and head span end
standardized_causal_relations_head_concepts_only = causal_relation_export_data.merge(standardized_data,
                           left_on=['head_id'],
                           right_on=['base_id'],
                           how = 'left',
                           suffixes = ('','_HEAD_CLIMATE_CONCEPT')
                           )

#left join again on output of previous join and node deduplication table by document_id sentence_id span_start span_end for head span start and head span end
standardized_causal_relations_head_and_child_concepts = standardized_causal_relations_head_concepts_only.merge(standardized_data,
                           left_on=['child_id'],
                           right_on=['base_id'],
                           how = 'left',
                           suffixes = ('','_CHILD_CLIMATE_CONCEPT')
                           )

standardized_causal_relations_head_and_child_concepts.to_csv("/Users/kameronr/Documents/personal/climate change outreach/new uploads/NLP data/main_3_per_cluster_outputs/standardized_causal_relations_v1.csv")


#standardized_causal_relations_concepts_simple
cols = ["climate_concept_id", "climate_concept_string_representation", "change_direction (standardized v1)", "type_of (standardized v1)", "base (standardized v1)", "aspect_changing (standardized v1)", "relation_type", "climate_concept_id_CHILD_CLIMATE_CONCEPT", "climate_concept_string_representation_CHILD_CLIMATE_CONCEPT", "change_direction (standardized v1)_CHILD_CLIMATE_CONCEPT", "type_of (standardized v1)_CHILD_CLIMATE_CONCEPT", "base (standardized v1)_CHILD_CLIMATE_CONCEPT", "aspect_changing (standardized v1)_CHILD_CLIMATE_CONCEPT"]

standardized_causal_relations_concepts_simple = standardized_causal_relations_head_and_child_concepts[cols]


standardized_causal_relations_concepts_simple = standardized_causal_relations_concepts_simple.rename({"climate_concept_id": "climate_concept_id_HEAD_CLIMATE_CONCEPT", "climate_concept_string_representation": "climate_concept_string_representation_HEAD_CLIMATE_CONCEPT", 
	"change_direction (standardized v1)": "change_direction (standardized v1)_HEAD_CLIMATE_CONCEPT",
	"type_of (standardized v1)": "type_of (standardized v1)_HEAD_CLIMATE_CONCEPT",
	"base (standardized v1)": "base (standardized v1)_HEAD_CLIMATE_CONCEPT",
	"aspect_changing (standardized v1)": "aspect_changing (standardized v1)_HEAD_CLIMATE_CONCEPT"}, axis='columns')


#remove rows with missing climate concepts
standardized_causal_relations_concepts_simple = standardized_causal_relations_concepts_simple[ (standardized_causal_relations_concepts_simple.climate_concept_id_HEAD_CLIMATE_CONCEPT.notnull() & standardized_causal_relations_concepts_simple.climate_concept_id_CHILD_CLIMATE_CONCEPT.notnull()) ]

standardized_causal_relations_concepts_simple.to_csv("/Users/kameronr/Documents/personal/climate change outreach/new uploads/NLP data/main_3_per_cluster_outputs/standardized_causal_relations_climate_concepts_simple_v1.csv")


#deduplicate rows
deduplicated_standardized_causal_relations_concepts_simple = standardized_causal_relations_concepts_simple.drop_duplicates()

deduplicated_standardized_causal_relations_concepts_simple.to_csv("/Users/kameronr/Documents/personal/climate change outreach/new uploads/NLP data/main_3_per_cluster_outputs/deduplicated_standardized_causal_relations_climate_concepts_simple_v1.csv")








































