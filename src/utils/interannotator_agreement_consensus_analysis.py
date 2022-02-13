import srsly
import csv
import sys
import datetime

class InterannotatorAgreement():
    def __init__(self):
        self.sentences = []
        self.file_name = "checkin_three_all_labels"
        self.file_path = "C://Users//buchh//OneDrive/Desktop//cm_nlp//climatemind-nlp//utils//" + self.file_name + ".jsonl"
        self.file_name_answers = "answers_answers"
        self.file_path_answers = "C://Users//buchh//OneDrive/Desktop//cm_nlp//climatemind-nlp//utils//" + self.file_name_answers + ".jsonl"
        self.data = srsly.read_jsonl(self.file_path)
        self.data_answers = srsly.read_jsonl(self.file_path_answers)
        self.username_extra = "checkin_three_all_labels-"

    def get_sentences(self):
        for entry in self.data_answers:
            text = entry["text"]
            self.sentences.append(text)
        return self.sentences

    def get_interannotator_matrix(self):
        for entry in self.data:
            if entry['text'] == self.sentences[0]:
                print(entry)
                print()
                try:
                    if entry['answer'] == "accept":
                        for conn in entry['relations']:
                            head_span_start = conn["head_span"]["start"]
                            head_span_end = conn["head_span"]["end"]
                            child_rel_span_start = conn["child_span"]["start"]
                            child_rel_span_end = conn["child_span"]["end"]
                            if entry['text'][head_span_start:head_span_end]:
                                head = entry['text'][head_span_start:head_span_end]
                            else:
                                head = ""
                            if entry['text'][child_rel_span_start:child_rel_span_end]:
                                child = [entry['text'][child_rel_span_start:child_rel_span_end]]
                            else:
                                child = []
                except KeyError as k:
                    continue



if __name__ == "__main__":
    ia = InterannotatorAgreement()
    ia.get_sentences()
    ia.get_interannotator_matrix()

