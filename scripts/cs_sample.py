import os
import yaml
import argparse
import soundfile as sf

from pathlib import Path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="data_config.yaml", help="data configuration")
    args = parser.parse_args()

    with open(args.config, "r") as fp:
        config = yaml.load(fp)
    
    config = config["cs"]
    cs_data_root = config["data_root"]
    lang_list = config["lang"]
    hr_list = config["hr"]
    output_dir = config["output"]

    total_seconds_list = [h*3600 for h in hr_list]
    
    for lang, total_seconds in zip(lang_list, total_seconds_list):
        data_path = os.path.join(os.path.join(cs_data_root, lang), "train/correct/")
        wav_files = list(map(str, list(Path(data_path).rglob("*.wav"))))
        assert len(wav_files) > 0
        len_count = 0
        idx = 0
        while (True):
            wav, sr = sf.read(wav_files[idx])
            idx += 1
            len_count += len(wav) / sr
            output_path = os.path.join(os.path.join(output_dir, lang), "train/correct/")
            if not os.path.exists(output_path):
                Path(output_path).mkdir(parents=True, exist_ok=True)
            sf.write(os.path.join(output_path, os.path.basename(wav_files[idx])), wav, sr)
            if len_count >= total_seconds:
                break
            print(len_count)
    