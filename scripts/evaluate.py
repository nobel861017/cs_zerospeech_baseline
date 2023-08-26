from pathlib import Path
import os
import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, help='The input file of pseudo-probability')
parser.add_argument('--units', nargs='*', type=str, default=None, help='The path to the quantized units')
args = parser.parse_args()

valid_table = dict()
valid_table['es_en'] = dict()
df_es_en = pd.read_csv("/work/b08202033/zerospeech2021_baseline/scripts/test_cs_es-en_labeled.csv", encoding="utf-8")
valid_table['es_en']['test'] = list(map(int, list(df_es_en["valid"])))

table = dict()

with open(args.input, 'r') as f:
    for line in f.readlines():
        line = line.strip().split(' ')
        #print(line)
        filename, prob = line[0], float(line[1])
        filename = Path(filename)

        idx = str(os.path.splitext(os.path.basename(filename))[0])
        sets = os.path.basename(os.path.dirname(os.path.dirname(filename)))
        sets_dir = os.path.dirname(os.path.dirname(filename))
        lang = os.path.basename(os.path.dirname(sets_dir))
        correct_or_wrong = os.path.basename(os.path.dirname(filename))
        # print(correct_or_wrong)
        if lang not in table.keys():
            table[lang] = dict()
        if sets not in table[lang].keys():
            table[lang][sets] = dict()
        
        if idx not in table[lang][sets].keys():
            table[lang][sets][idx] = dict()

        table[lang][sets][idx][correct_or_wrong] = prob

for unit_file in args.units:
    with open(unit_file, 'r') as f:
        for line in f.readlines():
            line = line.strip().split('\t')
            filename, units = line[0], line[1].split(',')
            filename = Path(filename)
            idx = str(os.path.splitext(os.path.basename(filename))[0])
            sets = os.path.basename(os.path.dirname(os.path.dirname(filename)))
            sets_dir = os.path.dirname(os.path.dirname(filename))
            lang = os.path.basename(os.path.dirname(sets_dir))
            correct_or_wrong = os.path.basename(os.path.dirname(filename))
            table[lang][sets][idx][f'{correct_or_wrong}_len'] = len(units)


for lang in table.keys():
    for sets in table[lang].keys():
        correct_counter, correct_longer_counter, correct_shorter_counter = 0, 0, 0
        correct_longer_correct_counter = 0 #correct>wrong
        correct_shorter_correct_counter = 0 #correct<=wrong
        total = 0
        valid = None
        if lang in valid_table.keys() and sets in valid_table[lang].keys():
            valid = valid_table[lang][sets]
        for idx in table[lang][sets].keys():
            if ("correct" in table[lang][sets][idx].keys() and "wrong" in table[lang][sets][idx].keys()):
                longer = False
                if table[lang][sets][idx]['correct_len'] > table[lang][sets][idx]['wrong_len']:          
                    longer = True

                if valid is not None:
                    if valid[int(idx)]==1:
                        if table[lang][sets][idx]["correct"] > table[lang][sets][idx]["wrong"]:
                            correct_counter += 1
                            if longer:
                                correct_longer_correct_counter += 1
                            else:
                                correct_shorter_correct_counter += 1
                        total += 1
                        if longer:
                            correct_longer_counter += 1
                        else:
                            correct_shorter_counter += 1
                else:
                    if table[lang][sets][idx]["correct"] > table[lang][sets][idx]["wrong"]:
                        correct_counter += 1
                        if longer:
                            correct_longer_correct_counter += 1
                        else:
                            correct_shorter_correct_counter += 1
                    if longer:
                        correct_longer_counter += 1
                    else:
                        correct_shorter_counter += 1
                    total += 1
        assert (correct_longer_counter + correct_shorter_counter == total)
        assert (correct_longer_correct_counter + correct_shorter_correct_counter == correct_counter)
        print(f'Accuracy of {lang} {sets}: {correct_counter / total}')
        print(f'Number of pair in {lang} {sets} with correct longer: {correct_longer_counter}')
        print(f'Accuracy of {lang} {sets} with correct longer: {correct_longer_correct_counter / correct_longer_counter}')
        print(f'Number of pair in {lang} {sets} with correct shorter: {correct_shorter_counter}')
        print(f'Accuracy of {lang} {sets} with shorter longer: {correct_shorter_correct_counter / correct_shorter_counter}')
        print(f'Total pair: {total}')
print('Finished evaluation.')
