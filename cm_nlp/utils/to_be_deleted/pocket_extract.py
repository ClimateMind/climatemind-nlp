# Original author: Elton Law

from os import path
import argparse
import datetime
import pandas as pd
import requests
import sys




def main():
    # Get consumer_token from website
    consumer_key = args.consumer_key
    access_token = authorize(consumer_key)
    print("Request token authenticated, received access_token. Sending GET...")
    res = requests.post(url("get"), data={
        "consumer_key": consumer_key,
        "access_token": access_token,
        "detailType": "complete",
        "sort": "oldest",
        "state": "all",
    })

    if not res.ok:
        print("ERROR: GET failed", res.text)
        sys.exit(1)

    data = res.json()

    if len(data["list"].values()) == 0:
        print("ERROR: Empty response list")
        sys.exit(1)

    print("Rows found", len(data["list"].values()))
    df = pd.DataFrame(data["list"].values())

    now = datetime.datetime.now().strftime("%d-%m-%Y")

    # Cleans up tags column (nested maps)
    df["tags"] = df["tags"].apply(lambda x: list(x.keys()) if isinstance(x, dict) else [])

    filename_out = f"cm_pocket_export_{now}.csv"
    df.to_csv(path.join(args.output_dir, filename_out))
    print(f"Saved to {filename_out}. DONE")

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Extract data from pocket")
    parser.add_argument('--consumer_key', help='Consumer key from pocket (Required)', required=True)
    parser.add_argument('--output_dir',   help='output dir to store results in (Optional)', default=".")
    args = parser.parse_args()
    main()
