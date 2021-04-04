import spacy
from typing import List
import neuralcoref


def coref_resolution(sentences: List[str]) -> List[str]:
    nlp = spacy.load('en_core_web_sm')
    coref = neuralcoref.NeuralCoref(nlp.vocab)
    nlp.add_pipe(coref, name='neuralcoref')

    coref_sentences = []
    for sentence in sentences:
        doc = nlp(sentence)
        if doc._.has_coref:
            coref_sentences.append(doc._.coref_resolved)
        else:
            coref_sentences.append(sentence)
    
    return coref_sentences

# A simple test
# print(coref_resolution(["Tom is a smart boy. He know a lot of thing.", "My sister has a dog. She loves him. "]))