#analyze jsonl file form cause_effect sentence entity labeling (semantic role labeling) with longform

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


#output as a list each entry's change_direction, base_entity, and measurable_aspect_pr_state_that_changes ...
#try to keep them in the same order they appear in the text? that way can assoicate them into separate nodes?
#also output the whole sentence too for double checking

#"text"
#for each spans take only the ones with "label" that I want
#only take "answer":"accept" ?

keep_lines = {}

data_for_csv = []

#columns = 
 #base,type_of,change_direction,aspect_changing,to_whom,effect_size,confidence,where,when,predicate 
 #text, original_text, source

#spans
#Concept_Member,Contributes_To

empty_dict_entry = {
  "username": [],
  "change_direction": [],
	"type_of": [],
	"base": [],
	"aspect_changing": [],
	"to_whom": [],
	"effect_size": [],
	"confidence": [],  
	"where": [],
	"when": [],
	"predicate": [],
	"text": [],
	"original_text": [],
	"source": [],
	"document_id": [],
	"sentence_id": [],
	"change_direction_id": [],
	"aspect_changing_id": [],
	"base_id": []
	}

csv_columns = [
	"username",
  	"change_direction",
	"type_of",
  	"base",
	"aspect_changing",
	"to_whom",
	"effect_size",
	"confidence",  
	"where",
	"when",
	"predicate",
	"text",
	"original_text",
	"source",
	"document_id",
	"sentence_id",
	"change_direction_id",
	"aspect_changing_id",
	"base_id"
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


	base_entity_dict = {}

	for relation in entry["relations"]:
		if "label" in relation:
			if relation["label"] == "Concept_Member":
				#check if the "child_span" has the "label" of "base_entity" and if does, then check if that child base_entity is in the base_entity_dict and if not then add that child base_entity
				if "child_span" in relation:
					if "label" in relation["child_span"]:
						if relation["child_span"]["label"] == "base":
							#check if this base entity is in the base_entity_dict
							child_span_start = relation["child_span"]["start"] #assumes "start" is present even though doesn't check for it! And assumes just 1 start. This could be improved by checking first for "start"
							child_span_end = relation["child_span"]["end"] #assumes "end" is present even though doesn't check for it! And assumes just 1 end. This could be improved by checking first for "end"
							dict_key = str(child_span_start)+":"+str(child_span_end)
							base_entity = text[child_span_start:child_span_end]
							base_id = document_id+"_"+sentence_id+"_"+str(child_span_start)+"_"+str(child_span_end)

							if dict_key not in base_entity_dict.keys(): #add it
								base_entity_dict[dict_key] = copy.deepcopy(empty_dict_entry)
								base_entity_dict[dict_key]["base"].append(base_entity)
								base_entity_dict[dict_key]["text"].append(text)
								base_entity_dict[dict_key]["original_text"].append(original_text)
								base_entity_dict[dict_key]["source"].append(source)
								base_entity_dict[dict_key]["document_id"].append(document_id)
								base_entity_dict[dict_key]["sentence_id"].append(sentence_id)
								base_entity_dict[dict_key]["username"].append(username)
								base_entity_dict[dict_key]["base_id"].append(base_id)

							
							#now process that Concept_Members relation's "head" information and add it to it's associated base_entity information in the appropriate value of it's appropriate base_entity_dict key.
							head_span = relation["head_span"]
							head_span_start = head_span["start"]
							head_span_end = head_span["end"]
							head_span_label = head_span["label"]
							entity_label = text[head_span_start:head_span_end] 

							if head_span_label:
								if entity_label != base_entity: #ensure base_entity doesn't get added twice
									base_entity_dict[dict_key][head_span_label].append(entity_label)
									
									# if head_span_label == "change_direction": #if the label is for change_direction then add special type_of id (includes doc id, sentence id, span start, span stop)
									# 	change_direction_id = document_id+"_"+sentence_id+"_"+str(head_span_start)+"_"+str(head_span_end)
									# 	base_entity_dict[dict_key]["change_direction_id"].append(change_direction_id)
									# if head_span_label == "aspect_changing":
									# 	aspect_changing_id = document_id+"_"+sentence_id+"_"+str(head_span_start)+"_"+str(head_span_end)
									# 	base_entity_dict[dict_key]["change_direction_id"].append(aspect_changing_id)

                                    #if the label is for change_direction or aspect_changing then add special id (includes doc id, sentence id, span start, span stop)
									if head_span_label in ("change_direction", "aspect_changing"):
										span_id = document_id+"_"+sentence_id+"_"+str(head_span_start)+"_"+str(head_span_end)
										base_entity_dict[dict_key][head_span_label+"_id"].append(span_id)







	#for each base entry, add its dictionary contents to simple list of lists for easy export as csv line later... but make the data longform for the combinations of change_direction and aspect_changing

	for base_entity_entry, base_entity_value in base_entity_dict.items(): #.keys():

		expanded_lines = []

		# change_direction = base_entity_value["change_direction"] or [()]
		# aspect_changing = base_entity_value["aspect_changing"] or [()]
		if base_entity_value["change_direction"]:
			change_direction = zip(base_entity_value["change_direction"], base_entity_value["change_direction_id"])
		else:
			change_direction = [((),())]

		if base_entity_value["aspect_changing"]:
			aspect_changing = zip(base_entity_value["aspect_changing"], base_entity_value["aspect_changing_id"])
		else:
			aspect_changing = [((),())]		

		combinations = itertools.product(change_direction, aspect_changing)
		for combination in combinations:
			new_dictionary = {}
			for csv_column in csv_columns:
				new_dictionary[csv_column] = base_entity_value[csv_column]

			new_dictionary["change_direction"] = [combination[0][0]]
			new_dictionary["change_direction_id"] = [combination[0][1]]
			new_dictionary["aspect_changing"] = [combination[1][0]]
			new_dictionary["aspect_changing_id"] = [combination[1][1]]

			if new_dictionary["change_direction"] == [()]:
				new_dictionary["change_direction"] = []
			if new_dictionary["aspect_changing"] == [()]:
				new_dictionary["aspect_changing"] = []
			if new_dictionary["change_direction_id"] == [()]:
				new_dictionary["change_direction_id"] = []
			if new_dictionary["aspect_changing_id"] == [()]:
				new_dictionary["aspect_changing_id"] = []



			csv_line = []
			for column in csv_columns:
				csv_line.append(new_dictionary[column])
			csv_lines.append(csv_line)


#output the lines in csv_lines
output_file_name = file_name + '_base_entity_export_longform.csv'

with open(output_file_name, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(csv_lines)









