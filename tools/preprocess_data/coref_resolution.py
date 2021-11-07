import spacy
from typing import List
import neuralcoref


def coref_resolution(sentences: List[str]) -> List[str]:
    nlp = spacy.load('en_core_web_lg')
    coref = neuralcoref.NeuralCoref(nlp.vocab, greedyness=0.56, conv_dict={'Dolphin': ["animal's"]})
    nlp.add_pipe(coref, name='neuralcoref')

    coref_sentences = []
    for sentence in sentences:
        doc = nlp(sentence)
        if doc._.has_coref:
            print(f"Coref_clusters: {doc._.coref_clusters}")
            coref_sentences.append(doc._.coref_resolved)
        else:
            coref_sentences.append(sentence)
    
    return coref_sentences

# A simple test

coref_resolutions = coref_resolution(["Tom is a smart boy. He know a lot of thing.", 
"My sister has a dog. She loves him.", 
"Now a link has been observed between rising levels of atmospheric CO2 — and other greenhouse gases — and weakening vertical wind shear along the East Coast of the US. That will make it less likely that recent violent episodes of extreme weather will start to dissipate after making landfall, and may instead grow in strength.", 
"For example, when an ocean heat wave struck the waters of Western Australia in 2011, scientists noticed there were fewer dolphin births and the animal’s survival rate dropped."])


for coref in coref_resolutions:
    print(f"Example: {coref}\n")