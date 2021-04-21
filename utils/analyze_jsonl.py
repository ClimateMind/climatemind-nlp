#analyze jsonl file form cause_effect sentence entity labeling (semantic role labeling)

#import jsonl file
import srsly
#import itertools
import copy
import csv

#file_path = "KR_updated_annotations_team_task1.jsonl" 
file_name = "rel_data_KR"
file_path = file_name + ".jsonl"

data = srsly.read_jsonl(file_path)


#output as a list each entry's change_direction, base_entity, and measurable_aspect_pr_state_that_changes ...
#try to keep them in the same order they appear in the text? that way can assoicate them into separate nodes?
#also output the whole sentence too for double checking

#"text"
#for each spans take only the ones with "label" that I want
#only take "answer":"accept" ?

keep_lines = {}

data_for_csv = []

#columns = 
 #change_direction, type_for_entity, base_entity, measureable_aspect_or_state_that_changes, 
 #group_affected, location_associated, confidence_indicator, temporal_association, effect_size, 
 #text, original_text, source


empty_dict_entry = {
	"change_direction": [],
	"type": [],
	"base_entity": [],
	"measurable_aspect_or_state_that_changes": [],
	"group_affected": [],
	"location_associated": [],
	"confidence_indicator": [],
	"temporal_association": [],
	"effect_size": [],
	"cause_effect_relation_predicate": [],
	"text": [],
	"original_text": [],
	"source": [],
	"document_id": [],
	"sentence_id": []
	}

csv_columns = [
"change_direction", 
"type", 
"base_entity", 
"measurable_aspect_or_state_that_changes", 
"group_affected", 
"location_associated", 
"confidence_indicator", 
"temporal_association",
 "effect_size",
 "cause_effect_relation_predicate",
 "text",
 "original_text",
 "source",
 "document_id",
 "sentence_id"
]	

csv_lines = []

#append column headers to csv line list
csv_lines.append(csv_columns)


#for each sentence entry
for entry in data:

	if "text" in entry:
		text = entry["text"]
	else: throw("NO 'text' field encountered! This field is necessary for the rest of the script to work! Please fix this and then run this script.")


	if "original_text" in entry:
		original_text = entry["orig_text"]
	else: 
		original_text = "None because no text modifications made. See 'text' field for the original text."


	if "source" in entry:
		source = entry["source"]
	else: 
		source = "source missing!"


	if "document_id" in entry:
		document_id = entry["document_id"]
	else: 
		document_id = "document id missing!"


	if "sentence_id" in entry:
		sentence_id = entry["sentence_id"]
	else: 
		sentence_id = "sentence id missing!"


	base_entity_dict = {}

	for relation in entry["relations"]:
		if "label" in relation:
			if relation["label"] == "Concept_Member":
				#check if the "child_span" has the "label" of "base_entity" and if does, then check if that child base_entity is in the base_entity_dict and if not then add that child base_entity
				if "child_span" in relation:
					if "label" in relation["child_span"]:
						if relation["child_span"]["label"] == "base_entity":
							#check if this base entity is in the base_entity_dict
							child_span_start = relation["child_span"]["start"] #assumes "start" is present even though doesn't check for it! And assumes just 1 start. This could be improved by checking first for "start"
							child_span_end = relation["child_span"]["end"] #assumes "end" is present even though doesn't check for it! And assumes just 1 end. This could be improved by checking first for "end"
							dict_key = str(child_span_start)+":"+str(child_span_end)
							base_entity = text[child_span_start:child_span_end]

							if dict_key not in base_entity_dict.keys(): #add it
								base_entity_dict[dict_key] = copy.deepcopy(empty_dict_entry)
								base_entity_dict[dict_key]["base_entity"].append(base_entity)
								base_entity_dict[dict_key]["text"].append(text)
								base_entity_dict[dict_key]["original_text"].append(original_text)
								base_entity_dict[dict_key]["source"].append(source)
								base_entity_dict[dict_key]["document_id"].append(document_id)
								base_entity_dict[dict_key]["sentence_id"].append(sentence_id)

							
							#now process that Concept_Members relation's "head" information and add it to it's associated base_entity information in the appropriate value of it's appropriate base_entity_dict key.
							head_span = relation["head_span"]
							head_span_start = head_span["start"]
							head_span_end = head_span["end"]
							head_span_label = head_span["label"]
							entity_label = text[head_span_start:head_span_end] 

							if head_span_label:
								if entity_label != base_entity: #ensure base_entity doesn't get added twice
									base_entity_dict[dict_key][head_span_label].append(entity_label)

	#for each base entry, add its dictionary contents to simple list of lists for easy export as csv line later

	for base_entity_entry in base_entity_dict: #.keys():
		csv_line = []
		for column in csv_columns:
			csv_line.append(base_entity_dict[base_entity_entry][column])
		csv_lines.append(csv_line)


#output the lines in csv_lines
output_file_name = file_name + '_base_entity_export.csv'

with open(output_file_name, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(csv_lines)











