from pathlib import Path
import os
import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, help='The input file of pseudo-probability')
args = parser.parse_args()

valid_table = dict()
valid_table['es_en'] = dict()
valid_table['fr_en'] = dict()
valid_table['zh_en'] = dict()
df_es_en = pd.read_csv("scripts/test_cs_es-en_labeled.csv", encoding="utf-8")
df_fr_en = pd.read_csv("scripts/test_cs_fr-en_labeled.csv", encoding="utf-8")
df_zh_en = pd.read_csv("scripts/test_cs_zh-en_labeled_v2.csv", encoding="utf-8")
valid_table['es_en']['test'] = list(map(int, list(df_es_en["valid"])))
valid_table['fr_en']['test'] = list(map(int, list(df_fr_en["valid"].fillna(0))))
valid_table['zh_en']['test_new'] = list(map(int, list(df_zh_en["cw_valid"].fillna(1))))
# print("zh_en num:", len(valid_table['zh_en']['test_new']))
# print(df_zh_en["cw_valid"].fillna(1).value_counts())
table = dict()
with open(args.input, 'r') as f:
    lines = []
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

        if lang not in table.keys():
            table[lang] = dict()
        if sets not in table[lang].keys():
            table[lang][sets] = dict()
        
        if idx not in table[lang][sets].keys():
            table[lang][sets][idx] = dict()

        table[lang][sets][idx][correct_or_wrong] = prob

for lang in table.keys():
    for sets in table[lang].keys():
        correct_counter = 0
        total = 0
        valid = None
        if lang in valid_table.keys() and sets in valid_table[lang].keys():
            valid = valid_table[lang][sets]
        for idx in table[lang][sets].keys():
            if ("correct" in table[lang][sets][idx].keys() and "wrong" in table[lang][sets][idx].keys()):
                if valid is not None:
                    if valid[int(idx)] == 1:
                        if table[lang][sets][idx]["correct"] >= table[lang][sets][idx]["wrong"]:
                            correct_counter += 1
                        total += 1
                else:
                    if table[lang][sets][idx]["correct"] >= table[lang][sets][idx]["wrong"]:
                        correct_counter += 1
                    total += 1
        print(f'Accuracy of {lang} {sets}: {round(correct_counter / total, 4)}')

valid = valid_table["zh_en"]["test_new"]
len_valid = list(map(int, list(df_zh_en["len_valid"].fillna(1))))
# print([idx for idx, e in enumerate(list(df_zh_en["set"])) if e not in [0, 1] ])
set_ref = list(map(int, list(df_zh_en["set"].fillna(2))))
total_by_set = {0:0, 1:0}
hit_num_by_set = {0:0, 1:0}

total_by_len = {"correct is shorter":0, "correct is longer":0}
hit_num_by_len = {"correct is shorter":0, "correct is longer":0}

total_by_len_in_range_2_and_set_1 = 0
hit_num_by_len_in_range_2_and_set_1 = 0

for idx in table["zh_en"]["test_new"].keys():
    assert int(idx) < len(valid) and int(idx) < len(set_ref)
    if ("correct" in table[lang][sets][idx].keys() and "wrong" in table[lang][sets][idx].keys()):
        if valid[int(idx)] == 1 and len_valid[int(idx)] == 1:
            assert set_ref[int(idx)] != 2
            total_by_set[set_ref[int(idx)]] += 1
            if len(list(df_zh_en["correct"])[int(idx)]) < len(list(df_zh_en["wrong"])[int(idx)]):
                total_by_len["correct is shorter"] += 1
            else:
                total_by_len["correct is longer"] += 1
            if abs(len(list(df_zh_en["correct"])[int(idx)]) - len(list(df_zh_en["wrong"])[int(idx)])) <= 2 and set_ref[int(idx)] == 1:
                total_by_len_in_range_2_and_set_1 += 1
            if table[lang][sets][idx]["correct"] >= table[lang][sets][idx]["wrong"]:
                # print(list(df_zh_en["correct"])[int(idx)])
                # print(list(df_zh_en["wrong"])[int(idx)])
                # print("-------------------------------------")
                hit_num_by_set[set_ref[int(idx)]] += 1
                if len(list(df_zh_en["correct"])[int(idx)]) < len(list(df_zh_en["wrong"])[int(idx)]):
                    hit_num_by_len["correct is shorter"] += 1
                else:
                    hit_num_by_len["correct is longer"] += 1
                if abs(len(list(df_zh_en["correct"])[int(idx)]) - len(list(df_zh_en["wrong"])[int(idx)])) <= 2 and set_ref[int(idx)] == 1:
                    hit_num_by_len_in_range_2_and_set_1 += 1

print(f"Accuracy of zh_en_0 test_new: {round(hit_num_by_set[0] / total_by_set[0], 4)}")
print(f"Accuracy of zh_en_1 test_new: {round(hit_num_by_set[1] / total_by_set[1], 4)}")
correct_is_shorter_num = hit_num_by_len["correct is shorter"]
correct_is_shorter_total = total_by_len["correct is shorter"]
correct_is_longer_num = hit_num_by_len["correct is longer"]
correct_is_longer_total = total_by_len["correct is longer"]
correct_is_shorter_acc = hit_num_by_len["correct is shorter"] / total_by_len["correct is shorter"]
correct_is_longer_acc = hit_num_by_len["correct is longer"] / total_by_len["correct is longer"]
print(f"Accuracy of zh_en test_new (correct is shorter): {correct_is_shorter_num} / {correct_is_shorter_total} = {round(correct_is_shorter_acc, 4)}")
print(f"Accuracy of zh_en test_new (correct is longer): {correct_is_longer_num} / {correct_is_longer_total} = {round(correct_is_longer_acc, 4)}")

print(f"Accuracy of zh_en_1 test_new (correct wrong len within 2): {hit_num_by_len_in_range_2_and_set_1} / {total_by_len_in_range_2_and_set_1} = {round(hit_num_by_len_in_range_2_and_set_1/total_by_len_in_range_2_and_set_1, 4)}")
print('Finished evaluation.')
        