import spacy
import srsly  # to easily read/write JSONL etc.

#nlp = spacy.load("en_core_web_sm")  # or whatever you need

nlp = spacy.load("en_core_web_md")

examples = srsly.read_jsonl("./all_pocket_for_prodigy_effect_tag_texts_only.jsonl")

texts = (eg["text"] for eg in examples)

new_examples = []
for doc in nlp.pipe(texts):
    for sent in doc.sents:
        new_examples.append({"text": sent.text})
srsly.write_jsonl("./all_pocket_for_prodigy_effect_tag_texts_only_split_on_sentences.jsonl", new_examples)


examples2 = srsly.read_jsonl("./all_pocket_for_prodigy5.jsonl")

texts = (eg["text"] for eg in examples2)

new_examples = []
for doc in nlp.pipe(texts):
    for sent in doc.sents:
        new_examples.append({"text": sent.text})
srsly.write_jsonl("./all_pocket_for_prodigy5_split_on_sentences.jsonl", new_examples)



