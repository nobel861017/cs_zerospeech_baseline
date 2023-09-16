exp_name=mhubert_kmeans_mix_unit_cs_only
num_workers=32

# quantize training set (8 sets: cs_es-en, cs_fr-en, cs_zh-en, mono_es, mono_fr, mono_zh, mono_en)
config_path=scripts/config/config_train.yaml
train_output_dir=$exp_name/train

python scripts/quantize_audio.py $train_output_dir --config $config_path
python scripts/deduplicate.py --output $train_output_dir --max_units 6144 --convert
python scripts/form_convert.py --file_name $train_output_dir/quantized_outputs.txt --output $train_output_dir/converted_not_dedup.txt

# quantize dev set (3 sets)
config_path=scripts/config/config_dev.yaml
dev_output_dir=$exp_name/dev

python scripts/quantize_audio.py $dev_output_dir --config $config_path
python scripts/deduplicate.py --output $dev_output_dir --max_units 512 --convert

config_path=scripts/config/config_test.yaml
test_output_dir=$exp_name/test/

python scripts/quantize_audio.py $test_output_dir --config $config_path
python scripts/deduplicate.py --output $test_output_dir --max_units 512 --convert
python scripts/deduplicate.py --output $test_output_dir --max_units 512

# quantize test correct set (3 sets)
config_path=scripts/config/config_test_correct.yaml
test_output_correct_dir=$exp_name/test_cs/correct

python scripts/quantize_audio.py $test_output_correct_dir --config $config_path
python scripts/deduplicate.py --output $test_output_correct_dir --max_units 512 --convert
python scripts/deduplicate.py --output $test_output_correct_dir --max_units 512

# quantize test wrong set (3 sets)
config_path=scripts/config/config_test_wrong.yaml
test_output_wrong_dir=$exp_name/test_cs/wrong

python scripts/quantize_audio.py $test_output_wrong_dir --config $config_path
python scripts/deduplicate.py --output $test_output_wrong_dir --max_units 512

# preprocess data
fairseq-preprocess --only-source \
    --trainpref $train_output_dir/dedup_converted.txt \
    --validpref $dev_output_dir/dedup_converted.txt \
    --testpref $test_output_dir/dedup_converted.txt \
    --destdir $exp_name/bin \
    --workers $num_workers


