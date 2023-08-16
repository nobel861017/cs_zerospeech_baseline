exp_name=exp_name
config_path=scripts/config/config_train_debug.yaml
train_output_dir=exp_name/train

num_workers=16

python scripts/quantize_audio.py $train_output_dir --config $config_path
python scripts/deduplicate.py --output $train_output_dir --max_units 512 --convert


config_path=scripts/config/config_dev_debug.yaml
dev_output_dir=$exp_name/dev

python scripts/quantize_audio.py $dev_output_dir --config $config_path
python scripts/deduplicate.py --output $dev_output_dir --max_units 512 --convert

config_path=scripts/config/config_test_correct_debug.yaml
test_output_correct_dir=$exp_name/test/correct

python scripts/quantize_audio.py $test_output_correct_dir --config $config_path
python scripts/deduplicate.py --output $test_output_correct_dir --max_units 512 --convert
python scripts/deduplicate.py --output $test_output_correct_dir --max_units 512

config_path=scripts/config/config_test_wrong_debug.yaml
test_output_wrong_dir=$exp_name/test/wrong

python scripts/quantize_audio.py $test_output_wrong_dir --config $config_path
python scripts/deduplicate.py --output $test_output_wrong_dir --max_units 512

fairseq-preprocess --only-source \
    --trainpref $train_output_dir/dedup_converted.txt \
    --validpref $dev_output_dir/dedup_converted.txt \
    --testpref $test_output_correct_dir/dedup_converted.txt \
    --destdir $exp_name \
    --workers $num_workers


