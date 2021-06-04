import srsly
import json

file_name = "test-team-answers-bases-checkin-one"
file_path = "C://Users//buchh//OneDrive/Desktop//"+file_name+".jsonl"
user = "Alex"
data = srsly.read_jsonl(file_path)


def get_answers(username):
    f = open(username + "_answers.jsonl", "w")
    for entry in data:
        user_file = entry["_session_id"].replace("entity_checkin_one-", "")
        if user_file == username:
            ans = json.dumps(entry) + '\n'
            f.write(ans)
    f.close()


if not user:
    print("No username specified")
else:
    get_answers(user)
print("Done!")



