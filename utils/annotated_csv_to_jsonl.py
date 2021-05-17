#making jsonl file from csv of annotated sentences

import argparse
import pandas as pd
import srsly
import random
from os import path

def main():
    data = pd.read_csv(args.input_file_path, sep = ",")

    columns = list(data.columns)

    output_file_path = args.input_file_path.replace(".csv", ".jsonl", 1)
    randomized_output_file_path = path.join(path.dirname(output_file_path),
                                            "reversed_" + path.basename(output_file_path)
                                            )
    json_data = []
    for index, row in data.iterrows():
            line_contents = {} # each dictionary holds all information of a single line

            for column in columns:
                    if column == "text":
                            row[column] = row[column].replace('\n','')
                    line_contents[column] = row[column]
            json_data.append(line_contents)

    #if want to randomize the list
    json_data_shuffled = random.sample(json_data, len(json_data))


    srsly.write_jsonl(output_file_path,            json_data)
    srsly.write_jsonl(randomized_output_file_path, json_data_shuffled)

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Making jsonl file from csv of annotated sentences")
    parser.add_argument('--input_file_path',  help='Path to csv file (Required)', required=True)
    args = parser.parse_args()
    main()
