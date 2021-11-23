import srsly
import json

file_name = "checkin_four_all_labels"
file_path = "C://Users//buchh//OneDrive/Desktop//cm_nlp//climatemind-nlp//utils//"+file_name+".jsonl"
user = "answers2"
data = srsly.read_jsonl(file_path)


def get_answers(username):
    checkuser = []
    newfilename = username + "_answers.jsonl"
    f = open(newfilename, "w")
    for entry in data:
        user_file = entry["_session_id"].replace("checkin_four_all_labels-", "")
        if user_file == username:
            if entry['answer'] == "accept":
                checkuser.append("Username found: " + username)
                ans = json.dumps(entry) + '\n'
                f.write(ans)
    f.close()
    if checkuser:
        print(checkuser[0])
    else:
        print("User not found")

if not user:
    print("No username specified")
else:
    get_answers(user)
print("Done!")



