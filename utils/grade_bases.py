#analyze jsonl file form cause_effect sentence entity labeling (semantic role labeling)

#import jsonl file
import srsly
#import itertools
import copy
import csv
from collections import defaultdict

#file_path = "entity_checkin_one_download.49863984-3905-4e3d-a059-4b2ef0004267.jsonl"
file_name = "entity_checkin_one_download_6May21"
file_path = "C://Users//buchh//OneDrive/Desktop//"+file_name+".jsonl"
#file_name_answers = "model-answers-bases-entity-one-checkin"
file_name_answers = "ElleGettingAnswers_answers"
#file_path_answers = "C://Users//buchh//OneDrive/Desktop//"+file_name_answers+".jsonl"
file_path_answers = "C://Users//buchh//OneDrive/Desktop//"+file_name_answers+".jsonl"
#file_name = "entity_checkin_one_download.850cb48f-8027-4380-a497-fc0f31e64f48"
#file_path = file_name + ".jsonl"

data = srsly.read_jsonl(file_path)
data_answers = srsly.read_jsonl(file_path_answers)

keep_lines = {}
data_for_csv = []

empty_dict_entry = {
    "username": [],
    "change_direction": [],
    "type_of": [],
    "base": [],
    "correct_base": [],
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
    "correct": []
}

csv_columns = [
    "username",
    "change_direction",
    "type_of",
    "base",
    "correct_base",
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
    "correct"
]

csv_columns_sub = [
    "username",
    "text",
    "base",
    "correct_base",
    "correct"
]

csv_lines = []
base_entity_dict = {}
base_entity_dict_answers = {}
#csv_lines.append(csv_columns)

def create_dict(datasource, dict_name):
    for entry in datasource:
        if "text" in entry:
            text = entry["text"]
        else:
            text = ""
            throw("NO 'text' field encountered! This field is necessary for the rest of the script to work! Please fix this and then run this script.")

        if "original_text" in entry:
            original_text = entry["orig_text"]
        else:
            original_text = ""
        if "source" in entry:
            source = entry["source"]
        else:
            source = ""
        if "document_id" in entry:
            document_id = entry["document_id"]
        else:
            document_id = ""
        if "sentence_id" in entry:
            sentence_id = entry["sentence_id"]
        else:
            sentence_id = ""
        if "_session_id" in entry:
            username = entry["_session_id"]
        else:
            username = ""
        username = username.replace("entity_checkin_one-", "")

        if entry['answer'] == "accept":
            for relation in entry["spans"]:
                if "label" in relation:
                    if relation["label"] == "base":
                        child_span_start = relation["start"]
                        child_span_end = relation["end"]
                        dict_key = str(child_span_start) + ":" + str(child_span_end)
                        base_entity = text[child_span_start:child_span_end]

                        if username in dict_name:
                            old_val = dict_name[username]
                            old_val.append({"dict_key": dict_key,
                                            "base": base_entity,
                                            "text": text,
                                            "original_text": original_text,
                                            "source": source,
                                            "document_id": document_id,
                                            "sentence_id": sentence_id,
                                            "username": username
                                            })
                            dict_name[username] = old_val
                        else:
                            dict_name[username] = [{"dict_key": dict_key,
                                                    "base": base_entity,
                                                    "text": text,
                                                    "original_text": original_text,
                                                    "source": source,
                                                    "document_id": document_id,
                                                    "sentence_id": sentence_id,
                                                    "username": username
                                                  }]
        else:
            if username in dict_name:
                old_val = dict_name[username]
                old_val.append({"dict_key": "",
                                "base": "No base",
                                "text": text,
                                "original_text": original_text,
                                "source": source,
                                "document_id": document_id,
                                "sentence_id": sentence_id,
                                "username": username
                                })
                dict_name[username] = old_val
            else:
                dict_name[username] = [{"dict_key": "",
                                        "base": "No base",
                                        "text": text,
                                        "original_text": original_text,
                                        "source": source,
                                        "document_id": document_id,
                                        "sentence_id": sentence_id,
                                        "username": username
                                        }]


def get_answer_dict(datasource, dict_name):
    for entry in datasource:
        text = entry["text"]
        for relation in entry["spans"]:
            if "label" in relation:
                if relation["label"] == "base":
                    child_span_start = relation["start"]
                    child_span_end = relation["end"]
                    dict_key = str(child_span_start) + ":" + str(child_span_end)
                    base_entity = [text[child_span_start:child_span_end]]
                    if text not in dict_name:
                        dict_name[text] = base_entity
                    else:
                        dict_name[text] = dict_name[text] + base_entity


def get_res():
    for x in base_entity_dict:
        key_tmp = base_entity_dict[x]
        for u in key_tmp:
            try:
                ans = base_entity_dict_answers[u['text']]
            except KeyError as k:
                ans = []
            if not ans and u['base'] == "No base":
                u['correct'] = True
                u['correct_base'] = u['base']
            elif not ans and u['base']:
                u['correct'] = False
                u['correct_base'] = "No base"
            elif u['base'] in ans:
                u['correct'] = True
                u['correct_base'] = u['base']
            else:
                u['correct'] = False
                u['correct_base'] = "---"


def write_file():
    csv_lines = []
    output_file_name = file_name + '_base_entity_export.csv'
    csv_line = []
    user_check = []
    csv_line.append(csv_columns_sub)
    for x in base_entity_dict:
        for u in base_entity_dict[x]:
            #line = "{}, {}, {}, {}, {}".format(u['username'], u['text'], u['base'], u['correct_base'], u['correct'])
            tmp_line = []
            tmp_line.append(u['username'])
            tmp_line.append(u['text'])
            tmp_line.append(u['base'])
            tmp_line.append(u['correct_base'])
            tmp_line.append(u['correct'])
            csv_line.append(tmp_line)
    csv_lines = csv_line + csv_lines
    with open(output_file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(csv_lines)


create_dict(data, base_entity_dict)
get_answer_dict(data_answers, base_entity_dict_answers)
get_res()
write_file()
print("Done!")



