# multilingual zero resource challenge

## Environment
All packages are specified in requirements.txt

`pip install -r requirements.txt`

`cd zerospeech2021_baseline`

## Downloading pre-trained XLSR and XLMR model
Please first download the pretrained model.
   
xlsr1B: https://dl.fbaipublicfiles.com/fairseq/wav2vec/xlsr2_960m_1000k.pt
   
xlmr.base: https://dl.fbaipublicfiles.com/fairseq/models/xlmr.base.tar.gz

## Training
* Train the K-means
```  
python scripts/cpc/criterion/clustering/clustering_script.py \
--config cluster_config.yaml
```
* Quantize audio
```
python scripts/quantize_audio.py \
path/to/kmeans/cluster/checkpoint path/to/the/output/dir --config quantize_config.yaml
```
* Deduplicating
  
Note that the audios having more than `max_units` units after deduplicating will be excluded since they exceed the max tokens the model can receive.
```
python scripts/deduplicate.py \
--file_name /path/to/the/quantized/units \
--output /path/to/the/output/deduplicated/units \
--deleted_path /path/to/the/excluded/audios --max_units 512 --convert
```
* Preprocess quantized data for unit-LM training
```
fairseq-preprocess --only-source --trainpref /path/to/quantized/training/set \
--validpref /path/to/quantized/validation/set \
--testpref /path/to/quantized/testing/set --destdir /path/to/the/output --workers 20
```
* Training the unit-LM
  
Please note that for a XLMR-like architecture, the max-positions should be set to 512.
```
fairseq-train --fp16 /path/to/the/binarized/data --task masked_lm \
--criterion masked_lm --save-dir /path/to/the/resulting/checkpoints \
--keep-last-epochs 5 --train-subset train --num-workers 32 --arch roberta_base \
--optimizer adam --adam-betas '(0.9, 0.98)' --adam-eps 1e-06 --clip-norm 0.0 \
--lr-scheduler polynomial_decay --lr 0.0005 --total-num-update 250000 --warmup-updates 10000 \
--dropout 0.1 --attention-dropout 0.1 --weight-decay 0.01 --mask-multiple-length 10 --mask-prob 0.5 --mask-stdev 10 \
--sample-break-mode eos --tokens-per-sample 3072 --max-positions 6144 --max-tokens 4096 \
--update-freq 4 --max-update 250000 \
--seed 5 --log-format simple --log-interval 10 --skip-invalid-size-inputs-valid-test
```
Note: According to the repo of ZeroSpeech, the `update-freq` should be set to `128/n`, where n is the number of GPUs. The `max-tokens` are modified to fit the memory of GPUs.

## Testing
* Compute the pseudo-probability
```
python scripts/compute_proba_BERT.py /path/to/the/quantized/units \
/path/to/the/output/ /path/to/the/LM 
```
* Evalution
```
python scripts/evaluate.py --input /path/to/the/pseudo/probability/file
```
The accuracy will be printed.

