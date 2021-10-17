import prodigy
from prodigy.components.loaders import JSONL
from prodigy.components.preprocess import add_tokens
from prodigy.util import split_string
import spacy

import pandas as pd


def build_prelabel_dict(csv_path: str) -> dict:
    """ TODO: Add description """
    pattern_matcher_df = pd.read_csv(csv_path)
    pattern_dict = {}
    for column in pattern_matcher_df:
        for value in pattern_matcher_df[column].values:
            if value != None or value != '' or value != 'NaN':
                pattern_dict[value] = column
    
    return pattern_dict

def label_stream(text: str, pattern_matcher: dict):
    print(f'DEBUG: {text}')

def prelabel_stream(stream):
   pattern_dict = build_prelabel_dict('./root/pattern_matching_rules.csv')
   for eg in stream:
      deps, heads = label_stream(eg["text"], pattern_dict)
      yield eg
      eg["relations"] = []
      for i, (label, head) in enumerate(zip(deps, heads)):
         eg["relations"].append({"child": i, "head": head, "label": label})
      yield eg

@prodigy.recipe("prelabel_rel",
        dataset=("The dataset to use", "positional", None, str),
        spacy_model=("The base model", "positional", None, str),
        source=("The source data as a JSONL file", "positional", None, str),
        label=("One or more comma-separated labels", "option", "l", split_string),
        span_label=("One or more comma-separated labels", "option", "sl", split_string),
)
def prelabel_rel_recipe(dataset, spacy_model, source, label, span_label):
    nlp = spacy.load(spacy_model)
    stream = JSONL(source)                          # load the data
    stream = prelabel_stream(stream)        # add custom relations
    stream = add_tokens(nlp, stream)  # add "tokens" to stream

    return {
        "dataset": dataset,      # dataset to save annotations to
        "stream": stream,        # the incoming stream of examples
        "view_id": "relations",  # annotation interface to use
        "config": {
            "labels": label,  # labels to annotate
            "span_labels": span_label
        }
    }

