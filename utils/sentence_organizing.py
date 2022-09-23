

import pandas as pd
import srsly
import csv


main_3_per_cluster = "/Users/kameronr/Documents/personal/climate change outreach/new uploads/NLP data/main_3_per_cluster_download.cba617d8-a055-4622-97a3-c194a148cbed.jsonl"

gold_A_D_1 = "/Users/kameronr/Documents/personal/climate change outreach/new uploads/NLP data/gold_A_D_1_download.bdab609a-e22c-4ab3-afc8-75b9fe91f088.jsonl"

main_batchA = "/Users/kameronr/Documents/personal/climate change outreach/new uploads/NLP data/main_batchA_download.e8ae0b47-cfa5-4e9d-9aca-095f67fe4cba.jsonl"

main_batchB = "/Users/kameronr/Documents/personal/climate change outreach/new uploads/NLP data/main_batchB_download.59542f99-02ed-44f0-bb8a-4d8113af40e9.jsonl"

main_batchC = "/Users/kameronr/Documents/personal/climate change outreach/new uploads/NLP data/main_batchC_download.ff5914fd-d179-45fd-82fa-46a8926549ec.jsonl"

main_batchD = "/Users/kameronr/Documents/personal/climate change outreach/new uploads/NLP data/main_batchD_download.d2f88d43-98ec-4fe8-958c-29c05b1fb72e.jsonl"

main_batchE = "/Users/kameronr/Documents/personal/climate change outreach/new uploads/NLP data/main_batchE_download.8d0b4794-631c-4a6b-be6f-e00ffd882957.jsonl"

main_batchF = "/Users/kameronr/Documents/personal/climate change outreach/new uploads/NLP data/main_batchF_download.e5745e3e-4c6b-4edd-bf7d-43a51c1add4b.jsonl"

gold_batches_A_D_1 = "/Users/kameronr/Documents/personal/climate change outreach/new uploads/NLP data/gold_batches_A_D_1.jsonl"


file_name = "main_3_per_cluster"
data = srsly.read_jsonl(main_3_per_cluster)

file_name = "gold_A_D_1"
data = srsly.read_jsonl(gold_A_D_1)

file_name = "main_batchA"
data = srsly.read_jsonl(main_batchA)

file_name = "main_batchB"
data = srsly.read_jsonl(main_batchB)

file_name = "main_batchC"
data = srsly.read_jsonl(main_batchC)

file_name = "main_batchD"
data = srsly.read_jsonl(main_batchD)

file_name = "main_batchE"
data = srsly.read_jsonl(main_batchE)

file_name = "main_batchF"
data = srsly.read_jsonl(main_batchF)

file_name = "gold_batches_A_D_1"
data = srsly.read_jsonl(gold_batches_A_D_1)


empty_dict_entry = {
  "username": [],
	"text": [],
	"original_text": [],
	"source": [],
	"document_id": [],
	"sentence_id": [],
	"answer": []
	}



csv_columns = [
	"combo_id",
	"document_id",
	"sentence_id",
	"username",
	"answer",
	"original_text",
	"text",
	"source"
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

	if "answer" in entry:
		answer = entry["answer"]
	else: 
		answer = "answer missing!"

	if "combo_id" in entry:
		combo_id = entry["combo_id"]
	else: 
		combo_id = "combo_id missing!"

	#csv_line = []
	#for column in csv_columns:
	csv_lines.append([combo_id, document_id, sentence_id, username, answer, original_text, text, source])
	#csv_lines.append(csv_line)



#output the lines in csv_lines
output_file_name = file_name + '_csv_organized.csv'

with open(output_file_name, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(csv_lines)









