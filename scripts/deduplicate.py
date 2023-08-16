import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--file_name')
parser.add_argument('--output_dir')
parser.add_argument('--convert', action='store_true')
parser.add_argument('--max_units', type=int, default=512)

args = parser.parse_args()

def preprocess(file_name, convert):
    f = open(file_name, 'r')
    names = []
    lines = []
    deleted = []
    deleted_names = []
    for line in f.readlines():
        wav_name, line = line.split('\t')
        line = line.strip('\n').split(',')
        new_line = []
        for id in line:
            if len(new_line) == 0:
                new_line.append(id)
            elif new_line[-1] != id:
                new_line.append(id)
        if len(new_line) <= args.max_units:
            if not convert:
                names.append(wav_name)
            lines.append(new_line)
        else:
            deleted_names.append(wav_name)
            deleted.append(new_line)
    
    if not convert:
        return names, lines, deleted_names, deleted
    
    return None, lines, deleted_names, deleted



def write_output(names, lines, output, convert):
    if not convert:
        with open(output, 'w') as f:
            assert len(names)==len(lines)
            for i in range(len(names)):
                f.write(names[i]+'\t')
                f.write(','.join(lines[i]) + '\n')

    else:
        with open(output, 'w') as f:
            for line in lines:
                f.write(' '.join(line) + '\n')

if __name__ == '__main__':
    names, lines, deleted_names, deleted = preprocess(args.file_name, args.convert)
    dedup_path = os.path.join(args.output_dir, 'dedup.txt')
    deleted_path = os.path.join(args.output_dir, 'deleted.txt')
    write_output(names, lines, dedup_path, args.convert)
    write_output(deleted_names, deleted, deleted_path, False)
    