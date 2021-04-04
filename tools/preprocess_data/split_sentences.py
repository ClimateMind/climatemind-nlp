import spacy
import srsly

nlp = spacy.load("en_core_web_md") 

examples = srsly.read_jsonl("./data.jsonl")

texts = (str(eg["text"].replace('\n', ' ').replace('-', ' ')) for eg in examples)

new_examples = []
for doc in nlp.pipe(texts):
    for sent in doc.sents:
        new_examples.append({"text": sent.text})
srsly.write_jsonl("./data_split_on_sentences.jsonl", new_examples)


