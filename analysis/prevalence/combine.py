import argparse
import os
import pathlib
import json

import pandas as pd
from tqdm import tqdm

from .avp import COLUMN_NAMES

parser = argparse.ArgumentParser()
parser.add_argument(
    "-i",
    "--input-dir",
    type=pathlib.Path,
    help="directory containing JSON result files from main.py",
)
parser.add_argument(
    "-o",
    "--out-csv",
    type=pathlib.Path,
    help="output CSV path",
)

args = parser.parse_args()

data_dir = os.path.normpath(args.input_dir)
targets = os.listdir(data_dir)

rows = []

for file in tqdm(targets):
    if not file.lower().endswith(".json"):
        continue
    with open(os.path.join(data_dir, file)) as f:
        data = json.load(f)
        rows.append(data)

df = pd.DataFrame(rows, columns=["name"] + COLUMN_NAMES)
df.to_csv(args.out_csv)
