import srsly
import json

file_name_answers = "checkin_answers"
file_path_answers = "C://Users//buchh//OneDrive/Desktop//"+file_name_answers+".jsonl"
data = srsly.read_jsonl(file_path_answers)
final_sent = []

for entry in data:
    if "text" in entry:
        text = entry["text"]
    else:
        text = ""
        throw("NO 'text' field encountered! This field is necessary for the rest of the script to work! Please fix this and then run this script.")

    label_arr = []
    label_dict = {}
    if entry['answer'] == "accept":
        for relation in entry['spans']:
            if ("label" in relation) and ("start" in relation) and ("end" in relation):
                child_span_start = relation["start"]
                child_span_end = relation["end"]
                word = text[child_span_start:child_span_end]
                if relation["label"] == "base":
                    #tmp_tuple = (child_span_start, child_span_end, relation["label"])
                    if 'tokens' in label_dict:
                        prev_tokens = label_dict['tokens']
                        prev_labels = label_dict['labels']
                        label_dict['tokens'] = prev_tokens + [word]
                        label_dict['labels'] = prev_labels + ['base']
                    else:
                        label_dict['tokens'] = [word]
                        label_dict['labels'] = ['base']
                else:
                    if 'tokens' in label_dict:
                        prev_tokens = label_dict['tokens']
                        prev_labels = label_dict['labels']
                        label_dict['tokens'] = prev_tokens + [word]
                        label_dict['labels'] = prev_labels + ['no_base']
                    else:
                        label_dict['tokens'] = [word]
                        label_dict['labels'] = ["no_base"]
        print(label_dict)
        print("---")
        final_sent.append(label_dict)

for tokens in final_sent:
    with open('convert.txt', 'a') as convert_file:
        convert_file.write(json.dumps(tokens) + "\n")