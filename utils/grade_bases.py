#analyze jsonl file form cause_effect sentence entity labeling (semantic role labeling)

import srsly
import csv

file_name = "checkin_two"
file_path = "C://Users//buchh//OneDrive/Desktop//cm_nlp//climatemind-nlp//utils//"+file_name+".jsonl"
file_name_answers = "answers_answers"
file_path_answers = "C://Users//buchh//OneDrive/Desktop//cm_nlp//climatemind-nlp//utils//"+file_name_answers+".jsonl"

data = srsly.read_jsonl(file_path)
data_answers = srsly.read_jsonl(file_path_answers)

csv_columns_sub = [
    "user",
    "text",
    "entity result",
    "priority status",
    "entity label",
    "user word(s)",
    "correct word(s)"
]

base_entity_dict = {}
base_entity_dict_answers = {}
all_users = []
tmp_line = []
tmp_line.append(csv_columns_sub)


def create_dict(datasource, dict_name):
    for entry in datasource:
        if "text" in entry:
            text = entry["text"]
        else:
            text = ""
            throw("NO 'text' field encountered! This field is necessary for the rest of the script to work! Please fix this and then run this script.")

        if "_session_id" in entry:
            username = entry["_session_id"]
        else:
            username = ""
        username = username.replace("checkin_two_blank_bases_typeof-", "")

        if username not in all_users:
            all_users.append(username)

        if entry['answer'] == "accept":
            for relation in entry["spans"]:
                if "label" in relation:
                    child_span_start = relation["start"]
                    child_span_end = relation["end"]
                    dict_key = str(child_span_start) + ":" + str(child_span_end)
                    if relation["label"] == "base":
                        base_entity = text[child_span_start:child_span_end]
                    else:
                        base_entity = ""
                    if relation["label"] == "type_of":
                        type_of = text[child_span_start:child_span_end]
                    else:
                        type_of = ""

                    if username in dict_name:
                        old_val = dict_name[username]
                        old_val.append({"base": base_entity,
                                        "text": text,
                                        "username": username,
                                        "typeOf": type_of
                                        })
                        dict_name[username] = old_val
                    else:
                        dict_name[username] = [{"base": base_entity,
                                                "text": text,
                                                "username": username,
                                                "typeOf": type_of
                                                }]
        else:
            if username in dict_name:
                old_val = dict_name[username]
                old_val.append({"base": "No base",
                                "text": text,
                                "username": username,
                                "typeOf": "No type_of"
                                })
                dict_name[username] = old_val
            else:
                dict_name[username] = [{"base": "No base",
                                        "text": text,
                                        "username": username,
                                        "typeOf": "No type_of"
                                        }]


def get_answer_dict(datasource, dict_name):
    for entry in datasource:
        text = entry["text"]
        for relation in entry["spans"]:
            if "label" in relation:
                child_span_start = relation["start"]
                child_span_end = relation["end"]
                dict_key = str(child_span_start) + ":" + str(child_span_end)

                if relation["label"] == "base":
                    base_entity = [text[child_span_start:child_span_end]]
                else:
                    base_entity = []
                if relation["label"] == "type_of":
                    typeOf_entity = [text[child_span_start:child_span_end]]
                else:
                    typeOf_entity = []
                if text not in dict_name:
                    dict_name[text] = {'base': base_entity, 'typeOf': typeOf_entity}
                else:
                    updated_base = dict_name[text]['base'] + base_entity
                    updated_typeOf = dict_name[text]['typeOf'] + typeOf_entity
                    dict_name[text]['base'] = updated_base
                    dict_name[text]['typeOf'] = updated_typeOf


def get_tmp_dict(user):
    tmp_dict = {}
    for x in base_entity_dict:
        for y in base_entity_dict[x]:
            if y['username'] == user and y['text'] in base_entity_dict_answers:
                if y['text'] in tmp_dict:
                    if y['base']:
                        updated_base = tmp_dict[y['text']]['base'] + [y['base']]
                        tmp_dict[y['text']]['base'] = updated_base
                    if y['typeOf']:
                        updated_typeOf = tmp_dict[y['text']]['typeOf'] + [y['typeOf']]
                        tmp_dict[y['text']]['typeOf'] = updated_typeOf
                else:
                    tmp_dict[y['text']] = {'base': [y['base']], 'typeOf': [y['typeOf']]}

    #print("=====================")
    #print(user)
    #print(len(tmp_dict))
    #print("=====================")
    return tmp_dict


def get_res(entity, user, status):
    #x = "Himesh"
    tmp_dict = get_tmp_dict(user)
    if len(tmp_dict) > 0:
        all_sent = list(base_entity_dict_answers.keys())
        for t in tmp_dict:
            partial = False
            tmp_right_ans = []
            tmp_user_ans = []
            all_sent.remove(t)
            user_ans = [i for i in tmp_dict[t][entity] if i]
            right_ans = base_entity_dict_answers[t][entity]
            if right_ans:
                #print(t)
                #print(user_ans)
                #print(right_ans)
                tmp_user_ans = tmp_user_ans + user_ans
                tmp_right_ans = tmp_right_ans + right_ans
                for a in user_ans:
                    if a in tmp_right_ans:
                        #print("found: " + a)
                        line_arr = [user, t, "found", status, entity, a, a]
                        tmp_line.append(line_arr)
                        tmp_right_ans.remove(a)
                        tmp_user_ans.remove(a)
                    elif len(a.split(" ")) > 1:
                        strings_with_substring = [string for string in tmp_right_ans if a in string]
                        #print(strings_with_substring)
                        if strings_with_substring:
                            #print("partial: " + a)
                            line_arr = [user, t, "partial", status, entity, a, strings_with_substring[0]]
                            tmp_line.append(line_arr)
                            tmp_right_ans.remove(strings_with_substring[0])
                            tmp_user_ans.remove(a)
                        else:
                            for a1 in a.split(" "):
                                if a1 in tmp_right_ans:
                                    #print(a1)
                                    #print("partial: " + a)
                                    line_arr = [user, t, "partial", status, entity, a, a1]
                                    tmp_line.append(line_arr)
                                    if tmp_right_ans:
                                        tmp_right_ans.remove(a1)
                                    if tmp_user_ans:
                                        tmp_user_ans.remove(a)
                                    partial = True
                        if not partial:
                            #print("incorrect: " + a)
                            line_arr = [user, t, "incorrect", status, entity, a, "---"]
                            tmp_line.append(line_arr)
                            tmp_user_ans.remove(a)
                    else:
                        #print("incorrect: " + a)
                        line_arr = [user, t, "incorrect", status, entity, a, "---"]
                        tmp_line.append(line_arr)
                        tmp_user_ans.remove(a)

                if tmp_right_ans:
                    for r1 in tmp_right_ans:
                        #print("missing: " + r1)
                        line_arr = [user, t, "missing", status, entity, "---", r1]
                        tmp_line.append(line_arr)

                #print()

        if all_sent:
            for s in all_sent:
                #print("not scored: " + s + ": " + ", ".join(base_entity_dict_answers[s]))
                line_arr = [user, s, entity, "not scored", status, "---", base_entity_dict_answers[s][entity]]
                tmp_line.append(line_arr)


def write_file():
    output_file_name = file_name + '_base_entity_export.csv'
    with open(output_file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(tmp_line)


if __name__ == '__main__':
    create_dict(data, base_entity_dict)
    get_answer_dict(data_answers, base_entity_dict_answers)

    for x in all_users:
        get_res("base", x, "highest")
        get_res("typeOf", x, "highest")

    write_file()
    print("Done!")



