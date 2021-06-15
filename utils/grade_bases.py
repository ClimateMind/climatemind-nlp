#analyze jsonl file form cause_effect sentence entity labeling (semantic role labeling)

import srsly
import csv

file_name = "entity_checkin_one_download_6May21"
file_path = "C://Users//buchh//OneDrive/Desktop//"+file_name+".jsonl"
file_name_answers = "ElleGettingAnswers_answers"
file_path_answers = "C://Users//buchh//OneDrive/Desktop//"+file_name_answers+".jsonl"

data = srsly.read_jsonl(file_path)
data_answers = srsly.read_jsonl(file_path_answers)

csv_columns_sub = [
    "username",
    "text",
    "user_base",
    "correct_base",
    "result"
]

base_entity_dict = {}
base_entity_dict_answers = {}
all_users = []


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

        if username not in all_users:
            all_users.append(username)

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
                            old_val.append({"base": base_entity,
                                            "text": text,
                                            "username": username
                                            })
                            dict_name[username] = old_val
                        else:
                            dict_name[username] = [{"base": base_entity,
                                                    "text": text,
                                                    "username": username
                                                    }]
        else:
            if username in dict_name:
                old_val = dict_name[username]
                old_val.append({"base": "No base",
                                "text": text,
                                "username": username
                                })
                dict_name[username] = old_val
            else:
                dict_name[username] = [{"base": "No base",
                                        "text": text,
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


"""
# old implementation with only found, incorrect, and partial as results
def get_res():
    for x in base_entity_dict:
        key_tmp = base_entity_dict[x]
        for u in key_tmp:
            try:
                ans = base_entity_dict_answers[u['text']]
            except KeyError as k:
                ans = []

            if u['base'] in ans:
                u['correct'] = "found"
                u['correct_base'] = u['base']
            elif not ans and u['base'] == "No base":
                u['correct'] = "found"
                u['correct_base'] = u['base']
            elif (not ans and u['base']) or (ans and not u['base']) or (ans and u['base'] == "No base"):
                u['correct'] = "incorrect"
                u['correct_base'] = "No base"
            elif len(u['base'].split(" ")) > 1:
                for r in u['base'].split(" "):
                    for p in ans:
                        if p == r:
                            u['correct'] = "partial"
                            u['correct_base'] = p
                        if ('correct' or 'correct_base') not in u:
                            u['correct'] = "incorrect"
                            u['correct_base'] = "---"
            elif u['base'] not in ans:
                u['correct'] = "incorrect"
                u['correct_base'] = "---"
"""


def get_tmp_dict(user):
    tmp_dict = {}
    for x in base_entity_dict:
        for y in base_entity_dict[x]:
            if y['username'] == user and y['text'] in base_entity_dict_answers:
                if y['text'] in tmp_dict:
                    updated_base = tmp_dict[y['text']] + [y['base']]
                    tmp_dict[y['text']] = updated_base
                else:
                    tmp_dict[y['text']] = [y['base']]

    #print("=====================")
    #print(user)
    #print(len(tmp_dict))
    #print("=====================")
    return tmp_dict


# final implementation with found, incorrect, missing, partial, and not scored as result
def get_res2():
    output_file_name = file_name + '_base_entity_export.csv'
    tmp_line = []
    tmp_line.append(csv_columns_sub)
    for x in all_users:
        #x = "Himesh"
        tmp_dict = get_tmp_dict(x)
        if len(tmp_dict) > 0:
            all_sent = list(base_entity_dict_answers.keys())
            for t in tmp_dict:
                tmp_right_ans = []
                tmp_user_ans = []
                all_sent.remove(t)
                user_ans = tmp_dict[t]
                right_ans = base_entity_dict_answers[t]
                #print(t)
                #print(user_ans)
                #print(right_ans)
                tmp_user_ans = tmp_user_ans + user_ans
                tmp_right_ans = tmp_right_ans + right_ans
                for a in user_ans:
                    if a in tmp_right_ans:
                        #print("found: " + a)
                        line_arr = [x, t, a, a, "found"]
                        tmp_line.append(line_arr)
                        tmp_right_ans.remove(a)
                        tmp_user_ans.remove(a)
                    elif len(a.split(" ")) > 1:
                        strings_with_substring = [string for string in tmp_right_ans if a in string]
                        #print(strings_with_substring)
                        if strings_with_substring:
                            #print("partial: " + a)
                            line_arr = [x, t, a, strings_with_substring[0], "partial"]
                            tmp_line.append(line_arr)
                            tmp_right_ans.remove(strings_with_substring[0])
                            tmp_user_ans.remove(a)
                        else:
                            for a1 in a.split(" "):
                                if a1 in tmp_right_ans:
                                    #print("partial: " + a)
                                    line_arr = [x, t, a, a1, "partial"]
                                    tmp_line.append(line_arr)
                                    tmp_right_ans.remove(a1)
                                    tmp_user_ans.remove(a)
                    else:
                        #print("incorrect: " + a)
                        line_arr = [x, t, a, "---", "incorrect"]
                        tmp_line.append(line_arr)
                        tmp_user_ans.remove(a)

                if tmp_right_ans:
                    for r1 in tmp_right_ans:
                        #print("missing: " + r1)
                        line_arr = [x, t, "---", r1, "missing"]
                        tmp_line.append(line_arr)

                #print()

            if all_sent:
                for s in all_sent:
                    #print("not scored: " + s + ": " + ", ".join(base_entity_dict_answers[s]))
                    line_arr = [x, s, "---", base_entity_dict_answers[s], "not scored"]
                    tmp_line.append(line_arr)

    with open(output_file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(tmp_line)


create_dict(data, base_entity_dict)
get_answer_dict(data_answers, base_entity_dict_answers)
#get_res()
get_res2()
print("Done!")



