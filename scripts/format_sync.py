import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument('--file_name')
parser.add_argument('--output')
args = parser.parse_args()

if __name__ == '__main__':
    input_file = open(args.file_name, 'r')
    lines = []
    names = []
    units = []
    max_length = -1
    ls = input_file.readlines()
    for idx in range(len(ls)):
        line = ls[idx]
        assert len(line.split("\t"))==2
        name, unit = line.split("\t")[0], line.split("\t")[1]
        if len(name)>=max_length:
            max_length = len(name)
        names.append(name)
        units.append(unit)
    
    with open(args.output, 'w') as f:
        assert len(names)==len(units)
        for i in range(len(names)):
            f.write(names[i] + ' '*(max_length-len(names[i])) + "\t" + units[i])