#analyze jsonl file form cause_effect sentence entity labeling (semantic role labeling)

import srsly
import csv
import sys
import datetime

file_name = "checkin_three_all_labels"
file_path = "C://Users//buchh//OneDrive/Desktop//cm_nlp//climatemind-nlp//utils//"+file_name+".jsonl"

answer_username = "answers"
username_extra = "checkin_three_all_labels-"

csv_columns_sub = [
    "user",
    "text",
    "entity result",
    "concept rel. result",
    "contrib. rel. result",
    "priority status",
    "entity label",
    "user word/phrase",
    "correct word/phrase",
    "user concept rel. TARGET(S)",
    "correct concept rel. TARGET(S)",
    "user contrib. rel. TARGET(S)",
    "correct contrib. rel. TARGET(S)"
]

tmp_line = []
tmp_line.append(csv_columns_sub)
entities = {"base":"highest", "type_of":"highest", "change_direction":"high", "aspect_changing":"high", "to_whom":"high", "effect_size":"low", "confidence":"low", "where":"low", "when":"low", "predicate":"low", "relation":"low"}

def get_all_users():
    data = srsly.read_jsonl(file_path)
    all_users = []
    for entry in data:
        username = entry["_session_id"].replace(username_extra, "")
        if username not in all_users and username != answer_username:
            all_users.append(username)

    return all_users

def get_answer_dict(username):
    data = srsly.read_jsonl(file_path)
    base_entity_dict_answers = {}
    relation_dict = {}
    base_entity_dict_tmp_reject = {"base": ["No base"], "type_of": ["No type_of"],
    "change_direction": ["No change_direction"], "aspect_changing": ["No aspect_change"], "to_whom": ["No to_whom"], "effect_size": ["No effect_size"], "confidence": ["No confidence"], "where": ["No where"], "when": ["No when"], "predicate": ["No predicate"]}
    base_entity_dict_tmp_answer = {"base": [], "type_of": [], "change_direction": [], "aspect_changing": [], "to_whom": [], "effect_size": [], "confidence": [], "where": [], "when": [], "predicate": [], "relation":[]}

    for entry in data:
        text = entry["text"]
        if entry["_session_id"].replace(username_extra, "") == username:
            if entry['answer'] == "accept":
                for conn in entry['relations']:
                    head_span_start = conn["head_span"]["start"]
                    head_span_end = conn["head_span"]["end"]
                    child_rel_span_start = conn["child_span"]["start"]
                    child_rel_span_end = conn["child_span"]["end"]
                    if text[head_span_start:head_span_end]:
                        head = text[head_span_start:head_span_end]
                    else:
                        head = ""
                    if text[child_rel_span_start:child_rel_span_end]:
                        child = [text[child_rel_span_start:child_rel_span_end]]
                    else:
                        child = []

                    if username in relation_dict:
                        if text in relation_dict[username]:
                            new_res = {'label': conn['label'], head:child}
                            relation_dict[username][text].append(new_res.copy())
                        else:
                            relation_dict[username][text] = [{'label': conn['label'], head: child}]
                    else:
                        relation_dict[username] = {text: [{'label': conn['label'], head: child}]}

                for relation in entry["spans"]:
                    if ("label" in relation) and ("start" in relation) and ("end" in relation):
                        child_span_start = relation["start"]
                        child_span_end = relation["end"]

                        if text in base_entity_dict_answers:
                            base_entity_dict_tmp_answer[relation["label"]] = base_entity_dict_tmp_answer[relation["label"]] + [text[child_span_start:child_span_end]]
                        else:
                            base_entity_dict_answers[text] = base_entity_dict_tmp_answer
                            base_entity_dict_tmp_answer["relation"] = relation_dict[username][text]
                            base_entity_dict_tmp_answer = base_entity_dict_tmp_answer.fromkeys(base_entity_dict_tmp_answer, [])
                            base_entity_dict_answers[text] = [base_entity_dict_tmp_answer]
            else:
                base_entity_dict_answers[text] = [base_entity_dict_tmp_reject]

    return base_entity_dict_answers

def compare_results():
    answers = get_answer_dict(answer_username)
    final_res = []
    for user in get_all_users():
        user_ans = get_answer_dict(user)
        for x in answers:
            for y in user_ans:
                if y == x:
                    for ent in entities.keys():
                        if answers[x][0][ent] == user_ans[y][0][ent]:
                            if ent != "relation":
                                # 1. when both arrays are exactly the same
                                print("true " + ent + " for " + user + " user_ent1: {}, ans_ent: {}".format(user_ans[y][0][ent], answers[x][0][ent]))
                                for ans in user_ans[y][0][ent]:
                                    res = [user, x, "found", [], [], entities[ent], ent, ans, ans, [], [], [], []]
                                    final_res.append(res)
                                    answers[x][0][ent].remove(ans)
                                    user_ans[y][0][ent].remove(ans)
                        else:
                            if ent != "relation":
                                print("false " + ent + " for " + user + " user_ent1: {}, ans_ent: {}".format(user_ans[y][0][ent], answers[x][0][ent]))                                

                                # 2. when some elements are equal in both user and actual ans
                                for ans in user_ans[y][0][ent]:
                                    if ans in answers[x][0][ent]:
                                        res = [user, x, "found", [], [], entities[ent], ent, ans, ans, [], [], [], []]
                                        final_res.append(res)
                                        user_ans[y][0][ent].remove(ans)
                                        answers[x][0][ent].remove(ans)

                                # 3. when user ans is partially correct
                                # - if user ans is contained in actual ans
                                if user_ans[y][0][ent]:
                                    for ans in user_ans[y][0][ent]:
                                        substring_user = [string for string in answers[x][0][ent] if ans in string]
                                        if substring_user:
                                            res = [user, x, "partial", [], [], entities[ent], ent, ans, substring_user[0], [], [], [], []]
                                            final_res.append(res)
                                            answers[x][0][ent].remove(substring_user[0])
                                            user_ans[y][0][ent].remove(ans)

                                # - if actual ans is contained in user ans
                                if answers[y][0][ent]:
                                    for ans in answers[y][0][ent]:
                                        substring_ans = [string for string in user_ans[y][0][ent] if ans in string]
                                        if substring_ans:
                                            res = [user, x, "partial", [], [], entities[ent], ent, substring_ans[0], ans, [], [], [], []]
                                            final_res.append(res)
                                            answers[x][0][ent].remove(ans)
                                            user_ans[y][0][ent].remove(substring_ans[0])

                                # 4. when actual ans is missing from user ans
                                if answers[x][0][ent] and user_ans[y][0][ent]:
                                    set_difference_actual = set(answers[x][0][ent]) - set(user_ans[y][0][ent])
                                    for ans in list(set_difference_actual):
                                        res = [user, x, "missing", [], [], entities[ent], ent, "", ans, [], [], [], []]
                                        final_res.append(res)
                                        answers[x][0][ent].remove(ans)

                                # 5. when user ans is missing from actual ans
                                if answers[x][0][ent] and user_ans[y][0][ent]:
                                    set_difference_user =  set(user_ans[y][0][ent]) - set(answers[x][0][ent])
                                    for ans in list(set_difference_user):
                                        res = [user, x, "missing", [], [], entities[ent], ent, ans, "", [], [], [], []]
                                        final_res.append(res)
                                        user_ans[y][0][ent].remove(ans)

    return final_res

def write_file():
    tmp_line = compare_results()
    now = datetime.datetime.now().strftime("%m-%d-%Y_%H%M%S")
    output_file_name = file_name + '_base_entity_export_' + now + '.csv'
    with open(output_file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(tmp_line)

    print("Created file: " + output_file_name)

if __name__ == "__main__":
    write_file()
