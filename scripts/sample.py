import os
import argparse
import collections
import soundfile as sf

from pathlib import Path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--hr", type=int, default=30, help="hours of speech to sample")
    parser.add_argument("--data", type=str, default="mls_spanish/train/audio/", help="audio dir")
    parser.add_argument("--output", type=str, default="es_sampled/", help="dir to write out cs data")
    parser.add_argument("--ext", type=str, default="flac", help="file extension")
    args = parser.parse_args()
    total_seconds = args.hr * 3600
    len_count = 0
    flac_files = list(map(str, list(Path(args.data).rglob("*." + args.ext))))
    #print(flac_files)
    d = collections.defaultdict(list)
    d_maxidx = collections.defaultdict(int)
    d_idx = collections.defaultdict(int)
    key_idx = 0
    for p in flac_files:
        k = '_'.join(p.split('/')[-1].split('_')[:2])
        d[k].append(p)
        d_maxidx[k] += 1
    
    keys = list(d.keys())
    
    while (True):
        k = keys[key_idx]
        
        if d_idx[k] < d_maxidx[k]:
            p = d[k][d_idx[k]]
            wav, sr = sf.read(p)
            d_idx[k] += 1
            len_count += len(wav) / sr
            sf.write(os.path.join(args.output, p.split('/')[-1].split('.')[0] + ".wav"), wav, sr)
        if len_count >= total_seconds:
            break
        key_idx = (key_idx + 1) % len(keys)
        print(len_count)
    