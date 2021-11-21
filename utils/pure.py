json_string = '{"clusters": [[[6, 17], [32, 32]], [[4, 4], [55, 55], [91, 91]], [[58, 62], [64, 64], [79, 79]]], "sentences": [["This", "paper", "presents", "an", "algorithm", "for", "computing", "optical", "flow", ",", "shape", ",", "motion", ",", "lighting", ",", "and", "albedo", "from", "an", "image", "sequence", "of", "a", "rigidly-moving", "Lambertian", "object", "under", "distant", "illumination", "."], ["The", "problem", "is", "formulated", "in", "a", "manner", "that", "subsumes", "structure", "from", "motion", ",", "multi-view", "stereo", ",", "and", "photo-metric", "stereo", "as", "special", "cases", "."], ["The", "algorithm", "utilizes", "both", "spatial", "and", "temporal", "intensity", "variation", "as", "cues", ":", "the", "former", "constrains", "flow", "and", "the", "latter", "constrains", "surface", "orientation", ";", "combining", "both", "cues", "enables", "dense", "reconstruction", "of", "both", "textured", "and", "texture-less", "surfaces", "."], ["The", "algorithm", "works", "by", "iteratively", "estimating", "affine", "camera", "parameters", ",", "illumination", ",", "shape", ",", "and", "albedo", "in", "an", "alternating", "fashion", "."], ["Results", "are", "demonstrated", "on", "videos", "of", "hand-held", "objects", "moving", "in", "front", "of", "a", "fixed", "light", "and", "camera", "."]], "ner": [[[4, 4, "Generic"], [6, 17, "Task"], [20, 21, "Material"], [24, 26, "Material"], [28, 29, "OtherScientificTerm"]], [[32, 32, "Generic"], [42, 42, "Material"], [44, 45, "Material"], [48, 49, "Material"]], [[55, 55, "Generic"], [58, 62, "OtherScientificTerm"], [64, 64, "Generic"], [67, 67, "Generic"], [69, 69, "OtherScientificTerm"], [72, 72, "Generic"], [74, 75, "OtherScientificTerm"], [79, 79, "Generic"], [81, 88, "Task"]], [[91, 91, "Generic"], [95, 105, "Method"]], [[115, 118, "Material"]]], "relations": [[[4, 4, 6, 17, "USED-FOR"], [20, 21, 4, 4, "USED-FOR"], [24, 26, 20, 21, "FEATURE-OF"], [28, 29, 24, 26, "FEATURE-OF"]], [[42, 42, 44, 45, "CONJUNCTION"], [44, 45, 48, 49, "CONJUNCTION"]], [[58, 62, 55, 55, "USED-FOR"], [67, 67, 64, 64, "HYPONYM-OF"], [67, 67, 69, 69, "USED-FOR"], [67, 67, 72, 72, "CONJUNCTION"], [72, 72, 64, 64, "HYPONYM-OF"], [72, 72, 74, 75, "USED-FOR"], [79, 79, 81, 88, "USED-FOR"]], [[95, 105, 91, 91, "USED-FOR"]], []], "doc_key": "ICCV_2003_158_abs"}'


import itertools
import json

obj = json.loads(json_string)
doc = list(itertools.chain(*obj['sentences']))

for sent in obj['ner']:
    for e in sent:
        e_start = e[0]
        e_end = e[1] + 1
        e_tag = e[2]
        e_name = ' '.join(doc[e_start: e_end])
        print("{}\t{}".format(e_name, e_tag))