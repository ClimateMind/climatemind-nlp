import srsly

file_name = "checkin_four_all_labels"
file_path = "C://Users//buchh//OneDrive/Desktop//cm_nlp//climatemind-nlp//utils//"+file_name+".jsonl"
data = srsly.read_jsonl(file_path)

users = []
for entry in data:
    user_name = entry["_session_id"].replace("checkin_four_all_labels-", "")
    if user_name not in users:
        users.append(user_name)

print(users)



