import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--files', nargs='+')
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

def write_output(lines, output):
    with open(output, 'w') as f:
        for line in lines:
            for id in line:
                f.write(id)
                if '\n' not in id:
                    f.write(' ')

if __name__ == '__main__':
    files = args.files
    lines = []
    for file in files:
        lines = lines + preprocess(file)
    
    write_output(lines, args.output)
