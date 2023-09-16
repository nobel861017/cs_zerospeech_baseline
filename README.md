# Zero resource code-switched speech challenge

## Download code-switched zero resource data
Run this python code to download the testing data.
```python3
# pip install datasets
from datasets import load_dataset
dataset = load_dataset("kph68/cs_zerospeech")
```

## Download monolingual data
```
# Spanish
wget https://dl.fbaipublicfiles.com/mls/mls_spanish.tar.gz

# French
wget https://dl.fbaipublicfiles.com/mls/mls_french.tar.gz

# Chinese
wget https://www.openslr.org/resources/68/train_set.tar.gz
wget https://www.openslr.org/resources/68/dev_set.tar.gz

# English
wget https://www.openslr.org/resources/12/train-clean-100.tar.gz
https://www.openslr.org/resources/12/dev-clean.tar.gz

# Extreact
tar zxvf *.tar.gz
```

## Training
* Train the K-means


Please modify the config files first.
```  
python scripts/cpc/criterion/clustering/clustering_script.py \
--config scripts/cpc/criterion/clustering/cluster_config.yaml
```

* Quantize audio & Deduplication & Preprocess (binarize, building dictionary)


Please modify the config files, and modify the paths in `quantize_dedup.sh`.
```
bash quantize_dedup.sh
```

* Training the unit-LM


Please modify the parameters in `train_unit.sh` if needed.
```
bash train_unit.sh
```

## Testing
* Compute the pseudo-probability


Please modify the exp name in `evaluate.sh` first.
```
bash evaluate.sh
```

