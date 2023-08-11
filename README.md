#
Multilingual ZeroSpeech Challenge 2021 Baseline System (Forked)

This repository contains the baseline systems of the ZeroSpeech Challenge 2021.

The baseline system consists of 3 different componants: Unsupervised Acoustic
Modeling (CPC), Clustering (k-means) and Language Modeling (BERT/LSTM) as
described in [The Zero Resource Speech Benchmark 2021: Metrics and baselines for unsupervised spoken language modeling](https://arxiv.org/abs/2011.11588).

## Installation

* First clone this repository:

      git clone https://github.com/bootphon/zerospeech2021_baseline
      cd zerospeech2021_baseline

* Download the checkpoints in the `checkpoints` directory:

      curl http://download.zerospeech.com/models/2021_baseline.checkpoints.tar.gz | tar xz

* Setup a conda environment:

      conda env create -f environment.yml

* Activate the created environment:

      conda activate zerospeech2021_baseline


## Submission generation

The submissions for LSTM and BERT baselines (the ones available on
https://zerospeech.com) can be generated with the `submission/run.sh`
script on a cluster with SLURM available. Have a `./submission/run.sh --help`
for details.


## Evaluations

### Audio quantization

First of all, we need to quantize the audio files with the CPC+clustering
modules.

To quantize a set of audio files, run the `scripts/quantize_audio.py` script.

Example command:

    python ./scripts/quantize_audio.py \
        checkpoints/CPC-big-kmeans50/clustering_kmeans50/clustering_CPC_big_kmeans50.pt \
        ../data/LibriSpeech/dev-clean/ \
        ../quantized/LibriSpeech/dev-clean/ \
        --file_extension wav


The quantized units will be written in the `quantized_outputs.txt` file in the
output directory.

### Build clustering and one-hot features for ABX

We can use the script `scripts/build_CPC_features.py` to extract the CPC features from a
set of audio files.

Example command:

    python scripts/build_CPC_features.py \
        checkpoints/CPC-big-kmeans50/CPC_big_6kh/checkpoint_32.pt \
        ../data/LibriSpeech/dev-clean/ \
        ../features/CPC/layer2/LibriSpeech/dev-clean/ \
        --file_extension flac --gru_level 2


In order to export one-hot features from a `quantized_outputs.txt` file, use the
`scripts/build_1hot_features.py` script:

Example command:

    python scripts/build_1hot_features.py \
        ../quantized/LibriSpeech/dev-clean/quantized_outputs.txt \
        ../features/onehot/LibriSpeech/dev-clean/


The features of each file will be stored in a corresponding file
`file_name.txt`.

### Compute pseudo log-probabilities for sWUGGY, sBLIMP

To compute the pseudo log-probabilities of pseudo-units sequences using
BERT/LSTM models, use the `scripts/compute_proba_BERT.py` or
`scripts/compute_proba_LSTM.py` scripts.

Example command:

    python scripts/compute_proba_BERT.py \
        ../quantized/sWUGGY/dev/quantized_outputs.txt \
        ../scores/sWUGGY/dev/pseudo_log_proba.txt \
        checkpoints/CPC-big-kmeans50/BERT/BERT_CPC_big_kmeans50.pt


### Build LM features for sSIMI

We can export hidden BERT/LSTM features of pseudo-units sequences with the
`scripts/build_BERT_features.py` or `scripts/build_LSTM_features.py` scripts.

Example command:

    python scripts/build_BERT_features.py \
        ../quantized/sSIMI/dev/quantized_outputs.txt \
        ../features/BERT/layer4/sSIMI/dev/ \
        checkpoints/CPC-big-kmeans50-BERT/BERT/BERT_CPC_big_kmeans50.pt \
        --hidden_level 4


The features of each file will be stored in a corresponding file
`file_name.txt`.


## Training the baseline system

If you want to reproduce the baseline system, please follow the instructions
below.

### CPC

To train the CPC model, follow the instructions at
https://github.com/tuanh208/CPC_audio/tree/zerospeech

Example command:

    python /path/to/CPC_audio/cpc/train.py \
        --pathDB path/to/LibriSpeech/train-clean-100 \
        --pathCheckpoint checkpoints/CPC_small_960h \
        --pathTrain path/to/LibriSpeech/LibriSpeech100_labels_split/train_split.txt \
        --pathVal path/to/LibriSpeech/LibriSpeech100_labels_split/test_split.txt \
        --file_extension .flac

where examples of `train_split.txt` and `test_split.txt` can be found
[here](https://drive.google.com/drive/folders/1BhJ2umKH3whguxMwifaKtSra0TgAbtfb).


### k-means

To train the k-means clustering, run the script `clustering_script.py` in the
following
[repository](https://github.com/tuanh208/CPC_audio/tree/zerospeech/cpc/criterion/clustering)
`CPC_audio/cpc/criterion/clustering/`.

Example command:

    python /path/to/CPC_audio/cpc/criterion/clustering/clustering_script.py \
        --pathDB path/to/LibriSpeech/train-clean-100/ --recursionLevel 1 \
        --nClusters 50 --MAX_ITER 150 --level_gru 2 \
        --save --load --batchSizeGPU 500 \
        checkpoints/CPC_big_6kh/checkpoint_32.pt \
        checkpoints/clustering_CPC_big_kmeans50/clustering_CPC_big_kmeans50.pt


**NOTE:** This command was done on a *P100 16GB GPU*, and the `batchSizeGPU`
should be modified according to nClusters, so as to fit the memory. Here are the
recommended numbers:

  nClusters  | 20  | 50  | 100 | 200 | 500 | 2000
-------------|-----|-----|-----|-----|-----|------
batchSizeGPU | 500 | 500 | 300 | 200 | 100 |  50


### Language Model

As long as we have the clustering module, we can quantize the LibriSpeech
datasets and train a LM on the pseudo units.

#### Preprocess the data

To train fairseq's Language models, we have to first preprocess the data with
`fairseq-preprocess`.

Example preprocess command:

    fairseq-preprocess --only-source \
        --trainpref ../quantized/LibriSpeech/fairseq_train.txt \
        --validpref ../quantized/LibriSpeech/fairseq_valid_clean.txt \
        --testpref ../quantized/LibriSpeech/fairseq_test_clean.txt \
        --destdir ../fairseq-bin-data/LibriSpeech \
        --workers 20

**NOTE:** The data files contain only the quantized units seperated by space,
without the name of the audio files. We need to convert to the right form from
the outputs of the `clustering_quantization.py` script, e.g. `5895-34629-0032
31,13,12,12,12,...,13` → `31 13 12 12 12 ... 13`.

#### BERT

We train the fairseq's RoBERTa model as similar to this
[example](https://github.com/pytorch/fairseq/blob/master/examples/roberta/README.pretraining.md),
with the exception that we used spans of masks insead of single masks (with
additional `--mask-multiple-length` and `--mask-stdev` options).

Example train command:

    fairseq-train --fp16 ../fairseq-bin-data/LibriSpeech \
        --task masked_lm --criterion masked_lm \
        --save-dir checkpoints/BERT_CPC_big_kmeans50 \
        --keep-last-epochs 1 \
        --train-subset train \
        --num-workers 4 \
        --arch roberta_base \
        --optimizer adam --adam-betas '(0.9, 0.98)' --adam-eps 1e-06 --clip-norm 0.0 \
        --lr-scheduler polynomial_decay --lr 0.0005 --total-num-update 250000 --warmup-updates 10000 \
        --dropout 0.1 --attention-dropout 0.1 --weight-decay 0.01 \
        --mask-multiple-length 10 --mask-prob 0.5 --mask-stdev 10 \
        --sample-break-mode eos --tokens-per-sample 3072 --max-positions 6144 \
        --max-tokens 4096 --update-freq 4 --max-update 250000 \
        --seed 5 --log-format simple --log-interval 10 --skip-invalid-size-inputs-valid-test

**NOTE:** This command was done on *32 V100 GPUs*. If train on less GPUs (`n`
GPUs), the `--update-freq` should be set equal to `128/n`. Also, `--max-tokens`
could be modified to fit the GPU memory accordingly.

#### LSTM

We can train the fairseq's LSTM Language Model with the following command:


    fairseq-train --fp16 ../fairseq-bin-data/LibriSpeech \
        --task language_modeling \
        --save-dir checkpoints/LSTM_CPC_big_kmeans50 \
        --keep-last-epochs 2 \
        --tensorboard-logdir tensorboard \
        --arch lstm_lm \
        --decoder-embed-dim 200 --decoder-hidden-size 1024 --decoder-layers 3 \
        --decoder-out-embed-dim 200 \
        --optimizer adam --adam-betas '(0.9, 0.98)' --clip-norm 0.0 \
        --lr-scheduler inverse_sqrt --lr 0.0005 --warmup-updates 1000 --warmup-init-lr 1e-07 \
        --dropout 0.1 --weight-decay 0.01 \
        --sample-break-mode none --tokens-per-sample 2048\
        --max-tokens 163840 --update-freq 1 --max-update 100000

## Citation
Please consider citing this paper if it helps your research.
```
@misc{nguyen2020zero,
      title={The Zero Resource Speech Benchmark 2021: Metrics and baselines for unsupervised spoken language modeling}, 
      author={Tu Anh Nguyen and Maureen de Seyssel and Patricia Rozé and Morgane Rivière and Evgeny Kharitonov and Alexei Baevski and Ewan Dunbar and Emmanuel Dupoux},
      year={2020},
      eprint={2011.11588},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```
