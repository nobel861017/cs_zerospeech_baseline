import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument('--file_name')
parser.add_argument('--output')
args = parser.parse_args()

def preprocess(file_name):
    f = open(file_name, 'r')
    lines = []
    maxlen = -1
    for line in f.readlines():
        line = line.split('\t')
        line = line[1]
        line = line.strip().split(',')
        if len(line)>maxlen:
            maxlen = len(line)
        #if '\n' in line[-1]:
            #line[-1] = line[-1].split('\n')[0]
        lines.append(line)
    
    print("max units:", maxlen)
    return lines

def write_output(lines, output):
    with open(output, 'w') as f:
        for line in lines:
            f.write(" ".join(line) + '\n')

if __name__ == '__main__':
    lines = preprocess(args.file_name)
    write_output(lines, args.output)
    