# Adapted from Mukut Mukherjee's ipynb

import argparse
from os import path
import pandas as pd
import pickle
import time
from tqdm import tqdm

def main():

    # 'cm_pocket_export_23-11-2020.csv'
    data=pd.read_csv(args.pocket_csv_input, index_col=0)
    print("Input data Info: \n", data.info())

    #when scraping all articles
    solution = data

    if args.causes_only:
        solution_index=[]
        for index,row in data.iterrows():
            tags=row['tags']
            if 'cause'in tags:
                solution_index.append(index)
            elif 'causes' in tags:
                solution_index.append(index)
            elif 'Cause' in tags:
                solution_index.append(index)
            elif 'Causes' in tags:
                solution_index.append(index)
            elif 'caused' in tags:
                solution_index.append(index)
            elif 'causing' in tags:
                solution_index.append(index)

        solution=data.loc[solution_index]

    fb_string='https://www.facebook.com/'
    fb_solution_index=[]
    for index,row in solution.iterrows():
        if fb_string in row['given_url']:
            fb_solution_index.append(index)

    solution_wo_fb=solution.drop(index=fb_solution_index)

    # XXX: Need better naming
    solution_wo_fb.to_csv(path.join(args.output_dir, 'all_pocket.csv'))

    articles=solution_wo_fb['resolved_url'].values.tolist()

    token = args.diffbot_token
    URL   = args.diffbot_url

    #data_to_store=[]
    #articles=solution_wo_fb['resolved_url'].values.tolist()
    #arricles_processed=[]

    for x in tqdm(range(2206, 3084)):
        PARAMS = {'token':token,'url':articles[x]}
        r = requests.get(url = URL, params = PARAMS)
        data = r.json()
        data_to_store.append(data)
        arricles_processed.append(articles[x])

    pickle.dump( data_to_store, open( path.join(args.output_dir, "all_pocket.p"), "wb" ) )

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Process data extracted from pocket")
    parser.add_argument('--pocket_csv_input', help='Path to pocket export csv file (Required)',\
                                              required=True)
    parser.add_argument('--diffbot_token',    help='Diffbot token (Required)',\
                                              required=True)
    parser.add_argument('--diffbot_url',      help='Diffbot URL (Optional)',\
                                              default='https://api.diffbot.com/v3/article')
    parser.add_argument('--output_dir',       help='output dir to store results in (Optional)',\
                                              default=".")
    parser.add_argument('--causes_only',      help='Path to output jsonl file (Optional)',\
                                              action='store_true')
    args = parser.parse_args()
    main()
