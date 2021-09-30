# Original author: Elton Law

from os import path
import argparse
import datetime
import pandas as pd
import requests
import sys

def url(endpoint):
    return "https://getpocket.com/v3/" + endpoint

def authorize(consumer_key, headers = {"X-Accept": "application/json"}):
    redirect_uri = "https://google.com"
    req = requests.post(url("oauth/request"), data={
        "consumer_key": consumer_key,
        "redirect_uri": redirect_uri
    }, headers=headers)
    request_token = req.json()["code"]
    print("<<< After signing in at link below press ENTER >>>")
    print(f"https://getpocket.com/auth/authorize?request_token={request_token}&redirect_uri={redirect_uri}")
    input() # super hacky way of making it wait
    # After authenticating the request_token ask for an access token
    res = requests.post(url("oauth/authorize"), data={
        "consumer_key": consumer_key,
        "code": request_token,
    }, headers=headers)

    if not res.ok:
        print("ERROR: Authorization failed:", req.text)
        sys.exit(1)

    return res.json()["access_token"]

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
