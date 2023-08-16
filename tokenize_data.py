import torch
import fairseq
from fairseq.models.roberta.model_xlmr import XLMRModel
import argparse
import csv
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, help='The input senetences that are going to tokenize.')
parser.add_argument('--output', type=str, help='Output tokenized sentences path.')
parser.add_argument('--model', type=str, default='/work/b08202033/multilingual_zero_resource_challenge/xlmr.base/',
                    help='The pretrained multilingual language model that provides tokenizer.')

args = parser.parse_args()

with open(args.input, 'r', encoding='utf-16') as f:
    rows = csv.reader(f)
    rows = [x for x in rows]
    assert len(rows)>=2, 'There is no sentence in this file.'
    rows = rows[1:]

#### Here assume the sentence is contained in the second column, and the first row is the column label.
#### Needed to be modified when the data format is confirmed.
sentences = [x[0] for x in rows]

#sentences = [rows[i][0] for i in range(20)]

tokenized_sentences = []
cp_path = args.model
model = XLMRModel.from_pretrained(cp_path)
for _, s in enumerate(tqdm(sentences)):
    #bpe_sentence = '<s> ' + model.bpe.encode(s) + ' </s>'
    bpe_sentence = model.bpe.encode(s)
    sentence_tokens = model.task.source_dictionary.encode_line(bpe_sentence, append_eos=False, add_if_not_exist=False)
    tokenized_sentences.append(" ".join([model.task.source_dictionary.symbols[tok] for tok in sentence_tokens]))

with open(args.output, 'w') as f:
    for s in tokenized_sentences:
        f.write(s + '\n')
