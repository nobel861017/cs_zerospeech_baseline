from pathlib import Path
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, help='The input file of pseudo-probability')
args = parser.parse_args()

table = dict()
with open(args.input, 'r') as f:
    lines = []
    for line in f.readlines():
        line = line.strip().split(' ')
        #print(line)
        filename, prob = line[0], float(line[1])
        filename = Path(filename)

        idx = str(os.path.splitext(os.path.basename(filename))[0])
        top_dir = os.path.dirname(os.path.dirname(filename))
        correct_or_wrong = os.path.basename(os.path.dirname(filename))

        if top_dir not in table.keys():
            table[top_dir] = dict()
        
        if idx not in table[top_dir].keys():
            table[top_dir][idx] = dict()

        table[top_dir][idx][correct_or_wrong] = prob

correct_counter = 0
total = 0
for top_dir in table.keys():
    for idx in table[top_dir].keys():
        if table[top_dir][idx]["correct"] >= table[top_dir][idx]["wrong"]:
            correct_counter += 1
        total += 1

print(correct_counter / total)
        