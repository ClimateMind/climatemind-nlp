#analyze jsonl file form cause_effect sentence entity labeling (semantic role labeling)

import srsly
import csv
import sys
import datetime

file_name = "checkin_three_all_labels"
file_path = "C://Users//buchh//OneDrive/Desktop//cm_nlp//climatemind-nlp//utils//"+file_name+".jsonl"
file_name_answers = "answers_answers"
file_path_answers = "C://Users//buchh//OneDrive/Desktop//cm_nlp//climatemind-nlp//utils//"+file_name_answers+".jsonl"

data = srsly.read_jsonl(file_path)
data_answers = srsly.read_jsonl(file_path_answers)

answer_username = ""
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

base_entity_dict = {}
base_entity_dict_answers = {}
all_users = []
tmp_line = []
tmp_line.append(csv_columns_sub)
count_dict = {}
count_dict_user = {}
relation_dict = {}

def create_dict(datasource, dict_name, user=None):
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
        username = username.replace(username_extra, "")

        if username not in all_users:
            all_users.append(username)
        try:
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
                    
                    for relation in entry['spans']:
                        if ("label" in relation) and ("start" in relation) and ("end" in relation):
                            child_span_start = relation["start"]
                            child_span_end = relation["end"]

                            if relation["label"] == "base":
                                base_entity = text[child_span_start:child_span_end]
                            else:
                                base_entity = ""
                            if relation["label"] == "type_of":
                                type_of = text[child_span_start:child_span_end]
                            else:
                                type_of = ""
                            if relation["label"] == "change_direction":
                                change_dir = text[child_span_start:child_span_end]
                            else:
                                change_dir = ""
                            if relation["label"] == "aspect_changing":
                                aspect_change = text[child_span_start:child_span_end]
                            else:
                                aspect_change = ""
                            if relation["label"] == "to_whom":
                                to_whom = text[child_span_start:child_span_end]
                            else:
                                to_whom = ""
                            if relation["label"] == "effect_size":
                                effect_size = text[child_span_start:child_span_end]
                            else:
                                effect_size = ""
                            if relation["label"] == "confidence":
                                confidence = text[child_span_start:child_span_end]
                            else:
                                confidence = ""
                            if relation["label"] == "where":
                                where = text[child_span_start:child_span_end]
                            else:
                                where = ""
                            if relation["label"] == "when":
                                when = text[child_span_start:child_span_end]
                            else:
                                when = ""
                            if relation["label"] == "predicate":
                                predicate = text[child_span_start:child_span_end]
                            else:
                                predicate = ""

                            if username in dict_name:
                                old_val = dict_name[username]
                                old_val.append({"base": base_entity,
                                                "text": text,
                                                "username": username,
                                                "type_of": type_of,
                                                "change_direction": change_dir,
                                                "aspect_changing": aspect_change,
                                                "to_whom": to_whom,
                                                "effect_size": effect_size,
                                                "confidence": confidence,
                                                "where": where,
                                                "when": when,
                                                "predicate": predicate,
                                                "relation": relation_dict[username][text]
                                                })
                                dict_name[username] = old_val
                            else:
                                dict_name[username] = [{"base": base_entity,
                                                    "text": text,
                                                    "username": username,
                                                    "type_of": type_of,
                                                    "change_direction": change_dir,
                                                    "aspect_changing": aspect_change,
                                                    "to_whom": to_whom,
                                                    "effect_size": effect_size,
                                                    "confidence": confidence,
                                                    "where": where,
                                                    "when": when,
                                                    "predicate": predicate,
                                                    "relation": relation_dict[username][text]
                                                    }]
            else:
                if username in dict_name:
                    old_val = dict_name[username]
                    old_val.append({"base": "No base",
                                    "text": text,
                                    "username": username,
                                    "type_of": "No type_of",
                                    "change_direction": "No change_direction",
                                    "aspect_changing": "No aspect_change",
                                    "to_whom": "No to_whom",
                                    "effect_size": "No effect_size",
                                    "confidence": "No confidence",
                                    "where": "No where",
                                    "when": "No when",
                                    "predicate": "No predicate",
                                    })
                    dict_name[username] = old_val
                else:
                    dict_name[username] = [{"base": "No base",
                                            "text": text,
                                            "username": username,
                                            "type_of": "No type_of",
                                            "change_direction": "No change_direction",
                                            "aspect_changing": "No aspect_change",
                                            "to_whom": "No to_whom",
                                            "effect_size": "No effect_size",
                                            "confidence": "No confidence",
                                            "where": "No where",
                                            "when": "No when",
                                            "predicate": "No predicate"
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

def get_answer_username():
    global answer_username
    for entry in data_answers:
        if "_session_id" in entry:
            answer_username = entry["_session_id"]
        else:
            answer_username = ""
        answer_username = answer_username.replace(username_extra, "")
        break

def get_answer_dict(datasource, dict_name):
    for entry in datasource:
        text = entry["text"]
        for relation in entry["spans"]:
            if ("label" in relation) and ("start" in relation) and ("end" in relation):
                child_span_start = relation["start"]
                child_span_end = relation["end"]
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
                if relation["label"] == "change_direction":
                    change_dir_entity = [text[child_span_start:child_span_end]]
                    create_count_dict('change_direction')
                else:
                    change_dir_entity = []
                if relation["label"] == "aspect_changing":
                    aspect_change_entity = [text[child_span_start:child_span_end]]
                    create_count_dict('aspect_changing')
                else:
                    aspect_change_entity = []
                if relation["label"] == "to_whom":
                    to_whom_entity = [text[child_span_start:child_span_end]]
                    create_count_dict('to_whom')
                else:
                    to_whom_entity = []
                if relation["label"] == "effect_size":
                    effect_size_entity = [text[child_span_start:child_span_end]]
                    create_count_dict('effect_size')
                else:
                    effect_size_entity = []
                if relation["label"] == "confidence":
                    confidence_entity = [text[child_span_start:child_span_end]]
                    create_count_dict('confidence')
                else:
                    confidence_entity = []
                if relation["label"] == "where":
                    where_entity = [text[child_span_start:child_span_end]]
                    create_count_dict('where')
                else:
                    where_entity = []
                if relation["label"] == "when":
                    when_entity = [text[child_span_start:child_span_end]]
                    create_count_dict('when')
                else:
                    when_entity = []
                if relation["label"] == "predicate":
                    predicate_entity = [text[child_span_start:child_span_end]]
                    create_count_dict('predicate')
                else:
                    predicate_entity = []

                if text not in dict_name:
                    dict_name[text] = {"base": base_entity, 
                                       "type_of": typeOf_entity,
                                       "change_direction": change_dir_entity,
                                        "aspect_changing": aspect_change_entity,
                                        "to_whom": to_whom_entity,
                                        "effect_size": effect_size_entity,
                                        "confidence": confidence_entity,
                                        "where": where_entity,
                                        "when": when_entity,
                                        "predicate": predicate_entity
                                      }
                else:
                    updated_base = dict_name[text]['base'] + base_entity
                    updated_typeOf = dict_name[text]['type_of'] + typeOf_entity
                    updated_change_dir = dict_name[text]['change_direction'] + change_dir_entity
                    updated_aspect_changing = dict_name[text]['aspect_changing'] + aspect_change_entity
                    updated_to_whom = dict_name[text]['to_whom'] + to_whom_entity
                    updated_effect_size = dict_name[text]['effect_size'] + effect_size_entity
                    updated_confidence = dict_name[text]['confidence'] + confidence_entity
                    updated_where = dict_name[text]['where'] + where_entity
                    updated_when = dict_name[text]['when'] + when_entity
                    updated_predicate = dict_name[text]['predicate'] + predicate_entity
                    dict_name[text]['base'] = updated_base
                    dict_name[text]['type_of'] = updated_typeOf
                    dict_name[text]['change_direction'] = updated_change_dir
                    dict_name[text]['aspect_changing'] = updated_aspect_changing
                    dict_name[text]['to_whom'] = updated_to_whom
                    dict_name[text]['effect_size'] = updated_effect_size
                    dict_name[text]['confidence'] = updated_confidence
                    dict_name[text]['where'] = updated_where
                    dict_name[text]['when'] = updated_when
                    dict_name[text]['predicate'] = updated_predicate

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
                    if y['change_direction']:
                        updated_change_direction = tmp_dict[y['text']]['change_direction'] + [y['change_direction']]
                        tmp_dict[y['text']]['change_direction'] = updated_change_direction
                    if y['aspect_changing']:
                        updated_aspect_changing = tmp_dict[y['text']]['aspect_changing'] + [y['aspect_changing']]
                        tmp_dict[y['text']]['aspect_changing'] = updated_aspect_changing
                    if y['to_whom']:
                        updated_to_whom = tmp_dict[y['text']]['to_whom'] + [y['to_whom']]
                        tmp_dict[y['text']]['to_whom'] = updated_to_whom
                    if y['effect_size']:
                        updated_effect_size = tmp_dict[y['text']]['effect_size'] + [y['effect_size']]
                        tmp_dict[y['text']]['effect_size'] = updated_effect_size
                    if y['confidence']:
                        updated_confidence = tmp_dict[y['text']]['confidence'] + [y['confidence']]
                        tmp_dict[y['text']]['confidence'] = updated_confidence
                    if y['where']:
                        updated_where = tmp_dict[y['text']]['where'] + [y['where']]
                        tmp_dict[y['text']]['where'] = updated_where
                    if y['when']:
                        updated_when = tmp_dict[y['text']]['when'] + [y['when']]
                        tmp_dict[y['text']]['when'] = updated_when
                    if y['predicate']:
                        updated_predicate = tmp_dict[y['text']]['predicate'] + [y['predicate']]
                        tmp_dict[y['text']]['predicate'] = updated_predicate
                else:
                    tmp_dict[y['text']] = {'base': [y['base']], 
                                           'type_of': [y['type_of']],
                                           'change_direction': [y['change_direction']],
                                           'aspect_changing': [y['aspect_changing']],
                                           'to_whom': [y['to_whom']],
                                           'effect_size': [y['effect_size']],
                                           'confidence': [y['confidence']],
                                           'where': [y['where']],
                                           'when': [y['when']],
                                           'predicate': [y['predicate']]
                                          }

    #print("=====================")
    #print(user)
    #print(len(tmp_dict))
    #print("=====================")
    return tmp_dict

def gen_rel_dicts(word, tmp_rel_dict):
    rel_dict = {}
    for y in tmp_rel_dict:
        if word in y.keys():
            if word in rel_dict:
                updated_rel = rel_dict[word] + y[word]
                rel_dict[word] = updated_rel
            else:
                rel_dict[word] = y[word]
                rel_dict['label'] = y['label']
    return rel_dict

def create_arr_res(user_ans, right_ans):
    tmp_right_ans = []
    tmp_user_ans = []
    ans_arr = []
    if right_ans:
        tmp_user_ans = tmp_user_ans + user_ans
        tmp_right_ans = tmp_right_ans + right_ans
        del_right_ans = []
        del_user_ans = []
        for a in user_ans:
            if a in tmp_right_ans:
                ans_arr.append("found")
                #print("found: " + a)
                tmp_right_ans.remove(a)
                tmp_user_ans.remove(a)
            elif len(a.split(" ")) > 1:
                strings_with_substring = [string for string in tmp_right_ans if a in string]
                if strings_with_substring:
                    ans_arr.append("partial")
                    #print("partial: " + a)
                    if strings_with_substring[0] not in del_right_ans:
                        del_right_ans.append(strings_with_substring[0])
                    if a not in del_user_ans:
                        del_user_ans.append(a)
                else:
                    for a1 in a.split(" "):
                        if a1 in tmp_right_ans:
                            #print("partial: " + a)
                            ans_arr.append("partial")
                            if a1 not in del_right_ans:
                                del_right_ans.append(a1)
                            if a not in del_user_ans:
                                del_user_ans.append(a)
                        else:
                            for ra in tmp_right_ans:
                                if len(ra.split(" ")) > 1:
                                    for a2 in a.split(" "):
                                        if a2 in ra.split(" "):
                                            #print("partial: " + a)
                                            ans_arr.append("partial")
                                            if ra not in del_right_ans:
                                                del_right_ans.append(ra)
                                            if a not in del_user_ans:
                                                del_user_ans.append(a)
            else:
                for ra in tmp_right_ans:
                    if len(ra.split(" ")) > 1:
                        for a2 in a.split(" "):
                            if a2 in ra.split(" "):
                                #print("partial: " + a)
                                ans_arr.append("partial")
                                if ra not in del_right_ans:
                                    del_right_ans.append(ra)
                                if a not in del_user_ans:
                                    del_user_ans.append(a)

        if del_user_ans:
            for da in del_user_ans:
                tmp_user_ans.remove(da)
        if del_right_ans:
            for dr in del_right_ans:
                tmp_right_ans.remove(dr)                            

        if tmp_right_ans:
            for r1 in tmp_right_ans:
                #print("missing: " + r1)
                ans_arr.append("missing")
        if tmp_user_ans:
            for ua in tmp_user_ans:
                #print("incorrect: " + ua)
                ans_arr.append("incorrect")
        
        return ans_arr

def check_rel(word, right_word, user_relation, right_relation):
    user_rel_dict = gen_rel_dicts(word, user_relation)
    ans_rel_dict = gen_rel_dicts(right_word, right_relation)
    ans_arr_final = []
    user_label = ""
    ans_label = ""
    if word:
        if word in user_rel_dict:        
            user_rel = user_rel_dict[word]
            #print(user_rel_dict['label'])
            user_label = user_rel_dict['label']
        else:
            user_rel = []
    else:
        user_rel = []
    if right_word:
        if right_word in ans_rel_dict:
            answer_rel = ans_rel_dict[right_word]
            #print(ans_rel_dict['label'])
            ans_label = ans_rel_dict['label']
        else:
            answer_rel = []
    else:
        answer_rel = []
    try:
        if user_rel_dict[word] == ans_rel_dict[word]:
            ans_arr_final = create_arr_res(user_rel_dict[word], ans_rel_dict[right_word])
            del user_rel_dict[word]
            del ans_rel_dict[word]
        else:
            ans_arr_final = create_arr_res(user_rel_dict[word], ans_rel_dict[right_word])
    except KeyError as k:
        if right_word in ans_rel_dict:
            ans_arr_final = ["missing"]*len(ans_rel_dict[right_word])
            del ans_rel_dict[right_word]
        else:
            ans_arr_final = []

    return ans_arr_final, user_rel, answer_rel, user_label

def get_res(entity, user, status):
    tmp_dict = get_tmp_dict(user)
    if len(tmp_dict) > 0:
        all_sent = list(base_entity_dict_answers.keys())
        for t in tmp_dict:
            tmp_right_ans = []
            tmp_user_ans = []
            all_sent.remove(t)
            user_ans = [i for i in tmp_dict[t][entity] if i]
            right_ans = base_entity_dict_answers[t][entity]
            if t in relation_dict[user]:
                user_relation = relation_dict[user][t]
            else:
                user_relation = []
            right_relation = relation_dict[answer_username][t]
            if right_ans:
                #print(t)
                #print(user_ans)
                #print(right_ans)
                #print(user_relation)
                #print("================================")
                #print(right_relation)
                tmp_user_ans = tmp_user_ans + user_ans
                tmp_right_ans = tmp_right_ans + right_ans
                del_right_ans = []
                del_user_ans = []
                for a in user_ans:
                    if a in tmp_right_ans:
                        ans1, ans2, ans3, ans4 = check_rel(a, a, user_relation, right_relation)
                        #print("found: " + a)
                        #print(ans3)
                        #print("///")
                        #print(ans4)
                        #print("///")
                        if ans4 == "Contributes_To":
                            line_arr = [user, t, "found", [], ans1, status, entity, a, a, [], [], ans2, ans3]
                        elif ans4 == "Concept_Member":
                            line_arr = [user, t, "found", ans1, [], status, entity, a, a, ans2, ans3, [], []]
                        else:
                            line_arr = [user, t, "found", ans1, ans1, status, entity, a, a, ans2, ans3, ans2, ans3]
                        create_count_dict_user(entity, user)
                        tmp_line.append(line_arr)
                        tmp_right_ans.remove(a)
                        tmp_user_ans.remove(a)
                    elif len(a.split(" ")) > 1:
                        # 1. if tmp_right_ans contains the user answer
                        strings_with_substring = [string for string in tmp_right_ans if a in string]
                        #print(strings_with_substring)
                        #print("---")
                        if strings_with_substring:
                            #print("partial: " + a)
                            ans1, ans2, ans3, ans4 = check_rel(a, strings_with_substring[0], user_relation, right_relation)
                            if ans4 == "Contributes_To":
                                line_arr = [user, t, "partial", [], ans1, status, entity, a, strings_with_substring[0], [], [], ans2, ans3]
                            elif ans4 == "Concept_Member":
                                line_arr = [user, t, "partial", ans1, [], status, entity, a, strings_with_substring[0], ans2, ans3, [], []]
                            else:
                                line_arr = [user, t, "partial", ans1, ans1, status, entity, a, strings_with_substring[0], ans2, ans3, ans2, ans3]
                            #create_count_dict_user(entity, user)
                            tmp_line.append(line_arr)
                            if strings_with_substring[0] not in del_right_ans:
                                del_right_ans.append(strings_with_substring[0])
                            if a not in del_user_ans:
                                del_user_ans.append(a)
                        else:
                            # 2. check both the answer and user answer
                            for a1 in a.split(" "):
                                if a1 in tmp_right_ans:
                                    #print("partial: " + a)
                                    ans1, ans2, ans3, ans4 = check_rel(a, a1, user_relation, right_relation)
                                    if ans4 == "Contributes_To":
                                        line_arr = [user, t, "partial", [], ans1, status, entity, a, a1, [], [], ans2, ans3]
                                    elif ans4 == "Concept_Member":
                                        line_arr = [user, t, "partial", ans1, [], status, entity, a, a1, ans2, ans3, [], []]
                                    else:
                                        line_arr = [user, t, "partial", ans1, ans1, status, entity, a, a1, ans2, ans3, ans2, ans3]
                                    #create_count_dict_user(entity, user)
                                    tmp_line.append(line_arr)
                                    if a1 not in del_right_ans:
                                        del_right_ans.append(a1)
                                    if a not in del_user_ans:
                                        del_user_ans.append(a)
                                else:
                                    for ra in tmp_right_ans:
                                        if len(ra.split(" ")) > 1:
                                            for a2 in a.split(" "):
                                                if a2 in ra.split(" "):
                                                    #print("partial: " + a)
                                                    ans1, ans2, ans3, ans4 = check_rel(a, ra, user_relation, right_relation)
                                                    if ans4 == "Contributes_To":
                                                        line_arr = [user, t, "partial", [], ans1, status, entity, a, ra, [], [], ans2, ans3]
                                                    elif ans4 == "Concept_Member":
                                                        line_arr = [user, t, "partial", ans1, [], status, entity, a, ra, ans2, ans3, [], []]
                                                    else:
                                                        line_arr = [user, t, "partial", ans1, ans1, status, entity, a, ra, ans2, ans3, ans2, ans3]
                                                    #create_count_dict_user(entity, user)
                                                    tmp_line.append(line_arr)
                                                    if ra not in del_right_ans:
                                                        del_right_ans.append(ra)
                                                    if a not in del_user_ans:
                                                        del_user_ans.append(a)
                    else:
                        for ra in tmp_right_ans:
                            if len(ra.split(" ")) > 1:
                                for a2 in a.split(" "):
                                    if a2 in ra.split(" "):
                                        #print("partial: " + a)
                                        ans1, ans2, ans3, ans4 = check_rel(a, ra, user_relation, right_relation)
                                        if ans4 == "Contributes_To":
                                            line_arr = [user, t, "partial", [], ans1, status, entity, a, ra, [], [], ans2, ans3]
                                        elif ans4 == "Concept_Member":
                                            line_arr = [user, t, "partial", ans1, [], status, entity, a, ra, ans2, ans3, [], []]
                                        else:
                                            line_arr = [user, t, "partial", ans1, ans1, status, entity, a, ra, ans2, ans3, ans2, ans3]
                                        #create_count_dict_user(entity, user)
                                        tmp_line.append(line_arr)
                                        if ra not in del_right_ans:
                                            del_right_ans.append(ra)
                                        if a not in del_user_ans:
                                            del_user_ans.append(a)

                if del_user_ans:
                    for da in del_user_ans:
                        tmp_user_ans.remove(da)
                if del_right_ans:
                    for dr in del_right_ans:
                        tmp_right_ans.remove(dr)                            

                if tmp_right_ans:
                    for r1 in tmp_right_ans:
                        ans1, ans2, ans3, ans4 = check_rel(None, r1, user_relation, right_relation)
                        #print("missing: " + r1)
                        if ans4 == "Contributes_To":
                            line_arr = [user, t, "missing", [], ans1, status, entity, "---", r1, [], [], ans2, ans3]
                        elif ans4 == "Concept_Member":
                            line_arr = [user, t, "missing", ans1, [], status, entity, "---", r1, ans2, ans3, [], []]
                        else:
                            line_arr = [user, t, "missing", ans1, ans1, status, entity, "---", r1, ans2, ans3, ans2, ans3]
                        tmp_line.append(line_arr)
                if tmp_user_ans:
                    for ua in tmp_user_ans:
                        ans1, ans2, ans3, ans4 = check_rel(ua, None, user_relation, right_relation)
                        #print("incorrect: " + ua)
                        if ans4 == "Contributes_To":
                            line_arr = [user, t, "incorrect", ["incorrect"], ans1, status, entity, ua, "---", [], [], ans2, ans3]
                        elif ans4 == "Concept_Member":
                            line_arr = [user, t, "incorrect", ans1, ["incorrect"], status, entity, ua, "---", ans2, ans3, [], []]                
                        else:
                            line_arr = [user, t, "incorrect", ans1, ans1, status, entity, ua, "---", ans2, ans3, ans2, ans3]
                        tmp_line.append(line_arr)
                #print()

        if all_sent:
            for s in all_sent:
                #print("not scored: " + s + ": " + ", ".join(base_entity_dict_answers[s]))
                relation_dict[user][t]
                relation_dict[answer_username][t]
                line_arr = [user, s, "not scored", "---", "---", status, entity, "---", base_entity_dict_answers[s][entity], "---", [], "---", []]
                tmp_line.append(line_arr)

def write_file(user=None):
    now = datetime.datetime.now().strftime("%m-%d-%Y_%H%M%S")
    if user:
        output_file_name = user + "_" + file_name + '_base_entity_export_' + now + '.csv'
    else:
        output_file_name = file_name + '_base_entity_export_' + now + '.csv'
    with open(output_file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(tmp_line)

    print("Created file: " + output_file_name)

def calc_pct(entity, user_count):
    if entity not in user_count:
        return 0
    else:
        return "{}%".format(round(((100*user_count[entity])/count_dict[entity]), 3))

def write_grade_file(user=None):
    now = datetime.datetime.now().strftime("%m-%d-%Y_%H%M%S")
    if user:
        output_file_name_grades = user + "_" + file_name + '_base_entity_export_results_' + now + '.csv'
    else:
        output_file_name_grades = file_name + '_base_entity_export_results_' + now + '.csv'
    lines = []
    lines_headers = ["user", "base", "type_of", "change_direction", "aspect_changing", "to_whom",
                "effect_size", "confidence", "where", "when", "predicate"]
    lines.append(lines_headers)
    for key, val in count_dict_user.items():
        res_lines = [key, calc_pct('base', val), calc_pct('type_of', val), calc_pct('change_direction', val), calc_pct('aspect_changing', val), calc_pct('to_whom', val), calc_pct('effect_size', val), 
        calc_pct('confidence', val), calc_pct('where', val), calc_pct('when', val), calc_pct('predicate', val)]
        lines.append(res_lines)

    with open(output_file_name_grades, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(lines)
    
    print("Created file: " + output_file_name_grades)

if __name__ == '__main__':
    get_answer_username()
    create_dict(data, base_entity_dict)
    get_answer_dict(data_answers, base_entity_dict_answers)

    if len(sys.argv) == 2:
        if str(sys.argv[-1]) not in all_users:
            print("Username " + str(sys.argv[-1]) + " not found. Please enter a different name")
        else:
            user = str(sys.argv[-1])
            print("Username: " + user + " found...")
            get_res("base", user, "highest")
            get_res("type_of", user, "highest")
            get_res("change_direction", user, "high")
            get_res("aspect_changing", user, "high")
            get_res("to_whom", user, "high")
            get_res("effect_size", user, "low")
            get_res("confidence", user, "low")
            get_res("where", user, "low")
            get_res("when", user, "low")
            get_res("predicate", user, "low")
            write_file(user)
            write_grade_file(user)
            print("Done!")
    elif len(sys.argv) == 1:
        for x in all_users:
            get_res("base", x, "highest") 
            get_res("type_of", x, "highest")
            get_res("change_direction", x, "high")
            get_res("aspect_changing", x, "high")
            get_res("to_whom", x, "high")
            get_res("effect_size", x, "low")
            get_res("confidence", x, "low")
            get_res("where", x, "low")
            get_res("when", x, "low")
            get_res("predicate", x, "low")
        write_file()
        write_grade_file()
        print("Done!")
    else:
        print("Invalid input")

    

