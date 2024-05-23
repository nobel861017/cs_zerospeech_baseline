# Zero resource code-switched speech challenge

## Download code-switched zero resource data
Run this python code to download only the testing data.
```python3
# pip install datasets
from datasets import load_dataset
dataset = load_dataset("kph68/cs_zerospeech")
```
The full code-switch dataset is available at huggingface
- [es-en](https://huggingface.co/datasets/ky552/cszs_es_en)
- [fr-en](https://huggingface.co/datasets/ky552/cszs_fr_en)
- [zh-en](https://huggingface.co/datasets/ky552/cszs_zh_en)


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

# Extract
tar zxvf *.tar.gz
```

## Data samples
|zh-en|transcript|audio|
|------|-----|------|
|correct|他们自称 artist.|http://sndup.net/kbjv | 
|wrong|他们自称 tasty.|http://sndup.net/gxdk |

|es-en|transcript|audio|
|------|-----|------|
|correct|En el presente, los interactive kiosks often have touch screens.|http://sndup.net/w2tj |
|wrong|En el presente, los interactive pantallas often have touch kiosks.|http://sndup.net/zjxm|

|fr-en|transcript|audio|
|------|-----|------|
|correct|Ce dernier has evolved tout au long de l'histoire romaine.|http://sndup.net/kpms |
|wrong|Ce dernier has evolved tout during la long de l'histoire romaine.|http://sndup.net/x39f| 

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


Please modify the parameters and some paths in `train_unit.sh` if needed.
```
bash train_unit.sh
```

## Testing
* Compute the pseudo-probability


Please modify the exp name and some paths in `evaluate.sh` first.
```
bash evaluate.sh
```

## Citation
If you find this dataset or benchmark useful, please consider citing the following papers:
```
@INPROCEEDINGS{10446737,
  author={Huang, Kuan-Po and Yang, Chih-Kai and Fu, Yu-Kuan and Dunbar, Ewan and Lee, Hung-Yi},
  booktitle={ICASSP 2024 - 2024 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)}, 
  title={Zero Resource Code-Switched Speech Benchmark Using Speech Utterance Pairs for Multiple Spoken Languages}, 
  year={2024},
  volume={},
  number={},
  pages={10006-10010},
  keywords={Speech coding;Benchmark testing;Signal processing;Linguistics;Acoustics;Speech processing;Task analysis;Code-switch;Multilingual;Discrete unit;Zero resource;Self-supervised},
  doi={10.1109/ICASSP48485.2024.10446737}}

@article{yang2023investigating,
  title={Investigating Zero-Shot Generalizability on Mandarin-English Code-Switched ASR and Speech-to-text Translation of Recent Foundation Models with Self-Supervision and Weak Supervision},
  author={Yang, Chih-Kai and Huang, Kuan-Po and Lu, Ke-Han and Kuan, Chun-Yi and Hsiao, Chi-Yuan and Lee, Hung-yi},
  journal={arXiv preprint arXiv:2401.00273},
  year={2023}
}
```

