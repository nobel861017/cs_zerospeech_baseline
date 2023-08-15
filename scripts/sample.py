import os
import yaml
import argparse
import collections
import soundfile as sf

from pathlib import Path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="config/data_config.yaml", help="data configuration")
    args = parser.parse_args()
    with open(args.config, "r") as fp:
        config = yaml.load(fp, Loader=yaml.FullLoader)
    
    config = config["mono"]
    mono_data_root = config["data_root"]
    lang_list = config["lang"]
    ext_list = config["ext"]
    hr_list = config["hr"]
    output_dir = config["output"]

    total_seconds_list = [h*3600 for h in hr_list]

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    for lang, total_seconds, ext in zip(lang_list, total_seconds_list, ext_list):
        data_path = os.path.join(mono_data_root, lang)
        audio_files = list(map(str, list(Path(data_path).rglob("*." + ext))))
        assert len(audio_files) > 0
        d = collections.defaultdict(list)
        d_maxidx = collections.defaultdict(int)
        d_idx = collections.defaultdict(int)
        key_idx = 0
        
        for p in audio_files:
            k = '_'.join(p.split('/')[-1].split('_')[:2])
            d[k].append(p)
            d_maxidx[k] += 1
        
        keys = list(d.keys())
        len_count = 0
        
        while (True):
            k = keys[key_idx]
        
            if d_idx[k] < d_maxidx[k]:
                p = d[k][d_idx[k]]
                wav, sr = sf.read(p)
                d_idx[k] += 1
                len_count += len(wav) / sr
                output_path = os.path.join(output_dir, lang)
                if not os.path.exists(output_path):
                    Path(output_path).mkdir(parents=True, exist_ok=True)
                sf.write(os.path.join(output_path, os.path.splitext(os.path.basename(p))[0] + '.wav'), wav, sr)
            if len_count >= total_seconds:
                break
            key_idx = (key_idx + 1) % len(keys)
            print(len_count)
    