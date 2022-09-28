#analyze jsonl file form cause_effect sentence entity labeling (semantic role labeling)

import datetime
import srsly
import csv

file_name = "checkin_four_all_labels"
file_path = "C://Users//buchh//OneDrive/Desktop//cm//cm_jsonl//"+file_name+".jsonl"
file_name_answers = "answers_answers"
file_path_answers = "C://Users//buchh//OneDrive/Desktop//cm//cm_jsonl//"+file_name+".jsonl"

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
count_dict_user = {}
count_dict = {}
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
        username = username.replace("checkin_four_all_labels-", "")

        if username not in all_users:
            all_users.append(username)
        if username == "Mukut":
            try:
                if entry['answer'] == "accept":
                    for relation in entry["spans"]:
                        if "label" in relation:
                            try:
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
                                                    "type_of": type_of
                                                    })
                                    dict_name[username] = old_val
                                else:
                                    dict_name[username] = [{"base": base_entity,
                                                            "text": text,
                                                            "username": username,
                                                            "type_of": type_of
                                                            }]
                            except KeyError as k:
                                continue
                    else:
                        if username in dict_name:
                            old_val = dict_name[username]
                            old_val.append({"base": "No base",
                                            "text": text,
                                            "username": username,
                                            "type_of": "No type_of"
                                            })
                            dict_name[username] = old_val
                        else:
                            dict_name[username] = [{"base": "No base",
                                                    "text": text,
                                                    "username": username,
                                                "type_of": "No type_of"
                                                    }]
                
            except KeyError as k:
                continue


def create_count_dict(entity):
    if entity in count_dict:
        count_dict[entity] += 1
    else:
        count_dict[entity] = 1

def create_count_dict_user(entity, user):
    if user not in count_dict_user:
        count_dict_user[user] = {}

    if entity in count_dict_user[user]:
        count_dict_user[user][entity] += 1
    else:
        count_dict_user[user][entity] = 1

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
                    create_count_dict('base')
                else:
                    base_entity = []
                if relation["label"] == "type_of":
                    typeOf_entity = [text[child_span_start:child_span_end]]
                    create_count_dict('type_of')
                else:
                    typeOf_entity = []
                if text not in dict_name:
                    dict_name[text] = {'base': base_entity, 'type_of': typeOf_entity}
                else:
                    updated_base = dict_name[text]['base'] + base_entity
                    updated_typeOf = dict_name[text]['type_of'] + typeOf_entity
                    dict_name[text]['base'] = updated_base
                    dict_name[text]['type_of'] = updated_typeOf


def get_tmp_dict(user):
    tmp_dict = {}
    for x in base_entity_dict:
        for y in base_entity_dict[x]:
            if y['username'] == user and y['text'] in base_entity_dict_answers:
                if y['text'] in tmp_dict:
                    if y['base']:
                        updated_base = tmp_dict[y['text']]['base'] + [y['base']]
                        tmp_dict[y['text']]['base'] = updated_base
                    if y['type_of']:
                        updated_typeOf = tmp_dict[y['text']]['type_of'] + [y['type_of']]
                        tmp_dict[y['text']]['type_of'] = updated_typeOf
                else:
                    tmp_dict[y['text']] = {'base': [y['base']], 'type_of': [y['type_of']]}

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
                        create_count_dict_user(entity, user)
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

def calc_pct(entity, user_count):
    if entity not in user_count:
        return 0
    else:
        return "{}%".format(round(((100*user_count[entity])/count_dict[entity]), 3))

def write_grade_file():
    now = datetime.datetime.now().strftime("%m-%d-%Y_%H%M%S")
    output_file_name_grades = file_name + '_base_entity_export_results_' + now + '.csv'
    lines = []
    lines_headers = ["user", "base", "type_of"]
    lines.append(lines_headers)
    for key, val in count_dict_user.items():
        res_lines = [key, calc_pct('base', val), calc_pct('type_of', val)]
        lines.append(res_lines)

    with open(output_file_name_grades, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(lines)
    
    print("Created file: " + output_file_name_grades)

if __name__ == '__main__':
    create_dict(data, base_entity_dict)
    get_answer_dict(data_answers, base_entity_dict_answers)

    for x in all_users:
        get_res("base", x, "highest")
        get_res("type_of", x, "highest")

    write_file()
    write_grade_file()
    print("Done!")



