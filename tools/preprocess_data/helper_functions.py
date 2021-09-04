import spacy
from typing import List

def split_sentences(paragraphs) -> List[str]:
    nlp = spacy.load("en_core_web_sm") 
    # minor text cleaning
    texts = (str(paragraph.replace('\n', ' ').replace('-', ' ')) for paragraph in paragraphs)

    new_data = []
    for doc in nlp.pipe(texts):
        for sent in doc.sents:
            new_data.append(sent.text)
    
    return new_data

