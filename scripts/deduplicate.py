import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument('--file_name')
parser.add_argument('--output')
parser.add_argument('--deleted_path')
parser.add_argument('--convert', action='store_true')
parser.add_argument('--max_units', type=int, default=512)

args = parser.parse_args()

def preprocess(file_name, convert):
    f = open(file_name, 'r')
    if not convert:
        names = []
        lines = []
        deleted = []
        deleted_names = []
        for line in f.readlines():
            line = line.split('\t')
            wav_name, line = line[0], line[1]
            line = line.split(',')
            if '\n' in line[-1]:
                line[-1] = line[-1][:-1]
            new_line = []
            for id in line:
                if len(new_line)==0:
                    new_line.append(id)
                else:
                    if new_line[-1]==id:
                        continue
                    new_line.append(id)
            if len(new_line)<=args.max_units:
                names.append(wav_name)
                lines.append(new_line)
            else:
                deleted_names.append(wav_name)
                deleted.append(new_line)
            
            
        return names, lines, deleted_names, deleted

    else:
        deleted_names = []
        lines = []
        deleted = []

        for line in f.readlines():
            line = line.split('\t')
            wav_name, line = line[0], line[1]
            line = line.split(',')
            
            if '\n' in line[-1]:
                line[-1] = line[-1][:-1]
            new_line = []
            for id in line:
                if len(new_line)==0:
                    new_line.append(id)
                else:
                    if new_line[-1]==id:
                        continue
                    new_line.append(id)
            
            if len(new_line)<=args.max_units:
                lines.append(new_line)
            else:
                deleted_names.append(wav_name)
                deleted.append(new_line)
            
        return None, lines, deleted_names, deleted

def write_output(names, lines, output, convert):
    if not convert:
        with open(output, 'w') as f:
            assert len(names)==len(lines)
            for i in range(len(names)):
                #f.write(names[i]+'\t')
                f.write(names[i]+'\t')
                for j in range(len(lines[i])):
                    f.write(lines[i][j])
                    if j!=len(lines[i])-1:
                        f.write(',')
                    else:
                        f.write('\n')
    else:
        with open(output, 'w') as f:
            for line in lines:
                for j in range(len(line)):
                    f.write(line[j])
                    if j==len(line)-1:
                        f.write('\n')
                    else:
                        f.write(' ')
               

if __name__ == '__main__':
    names, lines, deleted_names, deleted = preprocess(args.file_name, args.convert)
    write_output(names, lines, args.output, args.convert)
    write_output(deleted_names, deleted, args.deleted_path, False)
    