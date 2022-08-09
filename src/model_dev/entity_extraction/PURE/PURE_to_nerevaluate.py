import srsly
from nervaluate import Evaluator

actual_answers_file = "test"
actual_file_path = "/Users/ash/Desktop/PURE/PURE/data_ent/"+actual_answers_file+".json"
actual_data = srsly.read_jsonl(actual_file_path)

predicted_answers_file = "ent_pred_dev1"
predicted_file_path = "/Users/ash/Desktop/PURE/PURE/data_ent/"+predicted_answers_file+".json"
predicted_data = srsly.read_jsonl(predicted_file_path)

def create_nerevaluate_file(ans_file, ner_ent):
    ans = []
   
    for entry in ans_file:
        for n in entry[ner_ent]:
            tmp = []
            for x in n:
                ans_dict = {}
                ans_dict["start"] = x[0]
                ans_dict["end"] = x[1]
                ans_dict["label"] = x[2]
                tmp.append(ans_dict)
            ans.append(tmp)
           
    return ans

actual_answers = create_nerevaluate_file(actual_data, "ner")
predicted_answers = create_nerevaluate_file(predicted_data, "predicted_ner")

#print(predicted_answers)
#print(len(predicted_answers))
#print()
#print(actual_answers)
#print(len(actual_answers))
#print()

assert len(predicted_answers) == len(actual_answers)

entities = ["base", "aspect_changing", "change_direction", "type_of"]
evaluator = Evaluator(actual_answers, predicted_answers, tags=entities)

results, results_per_tag = evaluator.evaluate()
print(results)
print()
print(results_per_tag)

