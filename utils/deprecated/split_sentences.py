import sys
import spacy
import srsly  # to easily read/write JSONL etc.

nlp = spacy.load("en_core_web_sm")  # or whatever you need

input_file_path      = sys.argv[1] # path to all_pocket_for_prodigy_effect_tag_texts_only.jsonl
master_doc_json_path = sys.argv[2] # must be a json file
sentences_jsonl_path = sys.argv[3] # must be a jsonl file

#### Old method
#examples = srsly.read_jsonl(input_file_path)
#texts = (eg["text"] for eg in examples)
#new_examples = []
#for doc in nlp.pipe(texts):
    #for sent in doc.sents:
        #new_examples.append({"text": sent.text})
#srsly.write_jsonl("/home/skhushu/Private/Climate-Mind/data/test.jsonl", new_examples)

examples = srsly.read_jsonl(input_file_path)
texts = (eg["text"] for eg in examples)
# NOTE: Doing this to be able to recreate the list from above
#       Although this is terribly inefficient as we read over the jsonl file twice
all_sents = []
for doc in nlp.pipe(texts):
    sents = []
    for sent in doc.sents:
        sents.append(sent.text)
    all_sents.append(sents)
print("Number of docs: ", len(all_sents))

examples = srsly.read_jsonl(input_file_path)
document_index_list = {}
sentences_list = []
for doc_idx, eg in enumerate(examples):
    new_eg = eg.copy()
    new_eg["sentences"] = {}
    new_eg["document_index"] = doc_idx
    for sent_idx, sent in enumerate(all_sents[doc_idx]):
        new_eg["sentences"][sent_idx] = {"sentence_index": sent_idx, "text": sent}
        new_sent = {"url": new_eg["url"], "document_index": doc_idx,
                    "sentence_index": sent_idx, "text": sent}
        sentences_list.append(new_sent)
    document_index_list[doc_idx] = new_eg
srsly.write_json(master_doc_json_path, document_index_list)
srsly.write_jsonl(sentences_jsonl_path, sentences_list)
