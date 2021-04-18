# Original Author: Kameron Rodrigues

# Usage: split_sentences.py <path/to/output/of/process/extracted/text/script> (input)
#                           <path/to/master/json> (output)
#                           <path/to/split/sentences/jsonl> (output)

import sys
import spacy
import srsly  # to easily read/write JSONL etc.

nlp = spacy.load("en_core_web_md") # "en_core_web_sm"

input_file_path      = sys.argv[1] # path to all_pocket_for_prodigy_effect_tag_texts_only.jsonl
master_doc_json_path = sys.argv[2] # must be a json file
sentences_jsonl_path = sys.argv[3] # must be a jsonl file

examples = srsly.read_jsonl(input_file_path)
document_index_list = {}
sentences_list = []
for doc_idx, eg in enumerate(examples):
    print(f"title {eg['title']}")
    new_eg = eg.copy()
    new_eg["sentences"] = {}
    new_eg["document_index"] = doc_idx
    for sent_idx, sent in enumerate(nlp(eg["text"]).sents):
        new_eg["sentences"][sent_idx] = {"sentence_index": sent_idx, "text": sent.text}
        new_sent = {"url": new_eg["url"], "document_index": doc_idx,
                    "sentence_index": sent_idx, "text": sent.text}
        sentences_list.append(new_sent)
    document_index_list[doc_idx] = new_eg
    print()
srsly.write_json(master_doc_json_path, document_index_list)
srsly.write_jsonl(sentences_jsonl_path, sentences_list)
