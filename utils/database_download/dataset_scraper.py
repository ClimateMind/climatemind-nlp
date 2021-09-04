# Make sure prodigy is installed (download is in Slack)
from prodigy.components.db import connect
import uuid
import srsly # pip install srsly


dataset_name = "cm-label-eval" # Change this to the name of the dataset you want to use

# Connect to the database using the prodigy.json file (Can also be found in slack)
db = connect()

# The dataset will be returned as an object
dataset = db.get_dataset(dataset_name)

file_ext = "jsonl" # modify this if you want it to be saved as a different file format

# Name of the file being saved, we use uuid.uuid4() to avoid overwriting files 
outfile_name = f"{dataset_name}_download.{uuid.uuid4()}.{file_ext}"

out_path = "./" # location of where the dataset will be saved, default is same directory as script

# if youre writing it as json use .write_json instead, refer to srsly documentation for other formats
# or handle file writing yourself
srsly.write_jsonl(outfile_name, dataset)