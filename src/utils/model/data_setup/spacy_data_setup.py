import srsly

file_name_answers = "main_3_per_cluster_download.cba617d8-a055-4622-97a3-c194a148cbed"
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
    label_tup = ()
    if entry['answer'] == "accept":
        for relation in entry['spans']:
            if ("label" in relation) and ("start" in relation) and ("end" in relation):
                child_span_start = relation["start"]
                child_span_end = relation["end"]
                word = text[child_span_start:child_span_end]
                if relation["label"] == "base":
                    tmp_tuple = (child_span_start, child_span_end, relation["label"])
                    label_arr.append(tmp_tuple)

    label_tup = (str(text), {"entities": label_arr})
    final_sent.append(label_tup)

print(final_sent)
