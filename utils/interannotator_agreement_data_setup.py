import srsly
import csv
import sys
import datetime
import re
	
class InterannotatorAgreement():

    csv_columns_sub = [
        "annotator",
        "sentence",	
        "document id",
        "sentence id",
        "word",
        "token number",
        "feature",
        "type",
        "feature head span start token number",
        "feature head span end token number",
        "feature tail span start token number",
        "feature tail span end token number"
    ]

    file_name = "checkin_three_all_labels"
    file_path = "C://Users//buchh//OneDrive/Desktop//cm_nlp//climatemind-nlp//utils//"+file_name+".jsonl"
    file_name_answers = "answers_answers"
    file_path_answers = "C://Users//buchh//OneDrive/Desktop//cm_nlp//climatemind-nlp//utils//"+file_name_answers+".jsonl"
    username_extra = "checkin_three_all_labels-"
    all_users = []

    def __init__(self):
        self.sentences = []
        self.data = srsly.read_jsonl(self.file_path)
        self.data_answers = srsly.read_jsonl(self.file_path_answers)
        self.base_dict = {}
        self.relation_dict = {}
        self.result = []

    def create_relationship_dict(self, entry, username):
        text = entry["text"]
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

                child = [conn["head_span"]["token_start"], conn["head_span"]["token_end"], conn["child_span"]["token_start"], conn["child_span"]["token_end"]]

                if username in self.relation_dict:
                    if text in self.relation_dict[username]:
                        new_res = {'label': conn['label'], head:child}
                        self.relation_dict[username][text].append(new_res.copy())
                    else:
                        self.relation_dict[username][text] = [{'label': conn['label'], head: child}]
                else:
                    self.relation_dict[username] = {text: [{'label': conn['label'], head: child}]}
        #print(self.relation_dict['Kameron']['Not all ecomigration is the result of rapid climate change, of course #(e.g., volcanoes, earthquakes), but ecomigration as the direct result of rapid climate change (e.g., #increased frequency and intensity of heat waves, droughts, flooding) is quite common (Piguet, Pécoud, & de #Guchteneire, 2011). IMPLIED_BASE IMPLIED_BASE'])

    def relationship_dict(self):
        for entry in self.data:
            if "text" in entry:
                text = entry["text"]
            else:
                text = ""
                throw("NO 'text' field encountered! This field is necessary for the rest of the script to work! Please fix this and then run this script.")

            if "_session_id" in entry:
                username = entry["_session_id"]
            else:
                username = ""
            username = username.replace(self.username_extra, "")

            self.create_relationship_dict(entry, username)
            relations = self.relation_dict[username][text]

            document_id = entry['document_index']
            sentence_id = entry['md_sentence_index']

            # removing punctuations from the sentence
            text = re.sub(r'[^\w\s]', '', text)
            for word in text.split(" "):
                token_number = text.index(word) + 1
                entity = self.get_extra(entry, word)
                if word in entity:
                    arr = [username, text, document_id, sentence_id, word, token_number, "entity"] + entity[word] + entity[word][1:]
                else:
                    arr = [username, text, document_id, sentence_id, word, token_number, "entity"] + ["None", "None", "None", "None", "None"]
                self.result.append(arr)

                for r in relations:
                    if word in r:
                        arr = [username, text, document_id, sentence_id, word, token_number, "relationship", r['label']] + r[word]
                        self.result.append(arr)

    def get_extra(self, entry, word):
        text = entry["text"]
        label_dict = {}
        if entry['answer'] == "accept":
            for relation in entry['spans']:
                if ("label" in relation) and ("start" in relation) and ("end" in relation):
                    child_span_start = relation["start"]
                    child_span_end = relation["end"]
                    word_temp = text[child_span_start:child_span_end]
                    if word == word_temp:
                        label_dict[word] = [relation["label"], relation["token_start"], relation["token_end"]]
                        break
                    elif len(word_temp.split(" ")) > 1:
                        if word in word_temp.split(" "):
                            label_dict[word] = [relation["label"], relation["token_start"], relation["token_end"]]
                            break
                    else:
                        continue
        return label_dict

    def write_file(self):
        now = datetime.datetime.now().strftime("%m-%d-%Y_%H%M%S")
        output_file_name = self.file_name + '_interannotator_agreement_data_setup_' + now + '.csv'
        self.result.insert(0, self.csv_columns_sub)
        with open(output_file_name, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(self.result)

        print("Created file: " + output_file_name)


if __name__ == "__main__":
    ia = InterannotatorAgreement()
    ia.relationship_dict()
    ia.write_file()
