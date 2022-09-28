import srsly

file_name_answers = "gold_standard"
file_path_answers = "/Users/ash/Desktop/PURE/PURE/new_data/"+file_name_answers+".jsonl"

def get_all_sessions():
    data = srsly.read_jsonl(file_path_answers)
    sessions = []
    for entry in data:
        if entry["_session_id"] and entry["_session_id"] not in sessions:
            sessions.append(entry["_session_id"])
    return sessions

def get_sentences_per_user(user):
    data = srsly.read_jsonl(file_path_answers)
    sentence_count = 0
    for entry in data:
        text = entry["text"]
        if text:
            if entry['answer'] == "accept":
                if entry['_session_id'] == user:
                    sentence_count += 1
    return sentence_count

if __name__ == "__main__":
    users = get_all_sessions()
    for u in users:
        sentences = get_sentences_per_user(u)
        print("{}: {} sentences".format(u, sentences))


