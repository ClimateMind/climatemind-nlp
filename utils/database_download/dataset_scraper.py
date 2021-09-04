# Make sure prodigy is installed (download is in Slack)
import argparse
from prodigy.components.db import connect
import uuid
import srsly # pip install srsly
import os
import json

def main():
	
	dataset_name = args.dataset_name  # the dataset you want to use

	# Connect to the database using the prodigy.json file (Can also be found in slack)
	#db = connect(data["db"],data["db_settings"])
	db = connect() #Prodigy automatically will use the settings in 'prodigy.json' file in this script's directory if running from this directory

	# The dataset will be returned as an object
	dataset = db.get_dataset(dataset_name)

	file_ext = "jsonl" # modify this if you want it to be saved as a different file format

	out_path = args.output_path #"./" # location of where the dataset will be saved, default is same directory as script

	# Name of the file being saved, we use uuid.uuid4() to avoid overwriting files 
	outfile = os.path.join(out_path, f"{dataset_name}_download.{uuid.uuid4()}.{file_ext}")

	# if youre writing it as json use .write_json instead, refer to srsly documentation for other formats
	# or handle file writing yourself
	srsly.write_jsonl(outfile, dataset)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Exporting dataset from Prodigy database. Must run from this files directory!")
    parser.add_argument('--dataset_name',  help='Name of dataset in database (Required)', required=True)
    parser.add_argument('--output_path',  help='Path to save dataset export file (Required)', required=True)
    args = parser.parse_args()
    main()

