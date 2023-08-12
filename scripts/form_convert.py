import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument('--file_name')
parser.add_argument('--output')
args = parser.parse_args()

def preprocess(file_name):
    f = open(file_name, 'r')
    lines = []
    for line in f.readlines():
        line = line.split('\t')
        line = line[1]
        line = line.split(',')
        #if '\n' in line[-1]:
            #line[-1] = line[-1].split('\n')[0]
        lines.append(line)
    return lines

def split(lines):
    total = len(lines)
    train, val = int(total*0.7), int(total*0.2)
    random.shuffle(lines)
    train_lines, val_lines, test_lines = lines[:train], lines[train:val+train], lines[val+train::]
    assert len(train_lines) + len(val_lines) + len(test_lines) == total

    return train_lines, val_lines, test_lines

def write_output(lines, output):
    with open(output, 'w') as f:
        for line in lines:
            for id in line:
                f.write(id)
                if '\n' not in id:
                    f.write(' ')


if __name__ == '__main__':
    lines = preprocess(args.file_name)
    write_output(lines, args.output)
    