import fairseq
from fairseq.models.roberta.model_xlmr import XLMRModel
import argparse
import csv
from tqdm import tqdm
from pathlib import Path
import os

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, help='The input senetences that are going to tokenize.')
parser.add_argument('--output', type=str, help='Output tokenized sentences dir.')
parser.add_argument('--model', type=str, default='/work/b08202033/multilingual_zero_resource_challenge/xlmr.base/',
                    help='The pretrained multilingual language model that provides tokenizer.')
parser.add_argument('--only_correct', action='store_true', help='Activated if only tokenizing the correct text.')
parser.add_argument('--mono', action='store_true', help='Activated if only tokenizing the monolingual text.')
args = parser.parse_args()

flag_mono = False
with open(args.input, 'r', encoding='utf-16') as f:
    rows = csv.reader(f)
    rows = [x for x in rows]
    if not ('correct' in rows[0] or 'wrong' in rows[0]):
        assert args.mono, "Activate --mono if you want to tokenize monolingual data."
    else:
        assert not args.mono, "Don' activate --mono if you want to tokenize code-switched data"
    assert len(rows)>=2, 'There is no sentence in this file.'
    rows = rows[1:]

if args.mono:
    sentences = [x[0] for x in rows]

elif args.only_correct:
    sentences = [x[0] for x in rows]
    filenames = [x[2] for x in rows]

else:
    correct_sentence = [x[0] for x in rows]
    correct_filenames = [x[2] for x in rows]
    wrong_sentence = [x[1] for x in rows]
    wrong_filenames = [x[3] for x in rows]

    sentences = correct_sentence + wrong_sentence
    filenames = correct_filenames + wrong_filenames

#sentences = [rows[i][0] for i in range(20)]

tokenized_sentences = []
tokenized_sentences_converted = []
cp_path = args.model
model = XLMRModel.from_pretrained(cp_path)
for _, s in enumerate(tqdm(sentences)):
    s = s.lower()
    #bpe_sentence = '<s> ' + model.bpe.encode(s) + ' </s>'
    bpe_sentence = model.bpe.encode(s)
    sentence_tokens = model.task.source_dictionary.encode_line(bpe_sentence, append_eos=False, add_if_not_exist=False)
    tokenized_sentences_converted.append(" ".join([model.task.source_dictionary.symbols[tok] for tok in sentence_tokens]))
    tokenized_sentences.append(",".join([model.task.source_dictionary.symbols[tok] for tok in sentence_tokens]))

Path(args.output).mkdir(parents=True, exist_ok=True)

if args.mono:
    with open(os.path.join(args.output, 'tokenized_mono.txt'), 'w') as f:
        for s in tokenized_sentences_converted:
            f.write(s + '\n')
else:
    with open(os.path.join(args.output, 'tokenized_not_converted.txt'), 'w') as f:
        for fn, s in zip(filenames, tokenized_sentences):
            f.write(fn +'\t' + s + '\n')

    with open(os.path.join(args.output, 'tokenized_converted.txt'), 'w') as f:
        for s in tokenized_sentences_converted:
            f.write(s + '\n')
