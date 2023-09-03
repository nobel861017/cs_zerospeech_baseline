text_dir=datasets/cs_16k/csv
output_dir=datasets/cs_tokenized

# python scripts/tokenize_data.py --input $text_dir/dev_cs_es-en.csv --output $output_dir/dev/es-en/ --only_correct
# python scripts/tokenize_data.py --input $text_dir/dev_cs_fr-en.csv --output $output_dir/dev/fr-en/ --only_correct
# python scripts/tokenize_data.py --input $text_dir/dev_cs_zh-en.csv --output $output_dir/dev/zh-en/ --only_correct

# python scripts/tokenize_data.py --input $text_dir/test_cs_es-en.csv --output $output_dir/test/es-en/ --only_correct
# python scripts/tokenize_data.py --input $text_dir/test_cs_fr-en.csv --output $output_dir/test/fr-en/ --only_correct
# python scripts/tokenize_data.py --input $text_dir/test_cs_zh-en.csv --output $output_dir/test/zh-en/ --only_correct

python scripts/tokenize_data.py --input $text_dir/dev_cs_es-en.csv --output $output_dir/dev_total/es-en/ 
python scripts/tokenize_data.py --input $text_dir/dev_cs_fr-en.csv --output $output_dir/dev_total/fr-en/
python scripts/tokenize_data.py --input $text_dir/dev_cs_zh-en.csv --output $output_dir/dev_total/zh-en/

# python scripts/tokenize_data.py --input $text_dir/train_cs_es-en.csv --output $output_dir/train/es-en/ --only_correct
# python scripts/tokenize_data.py --input $text_dir/train_cs_fr-en.csv --output $output_dir/train/fr-en/ --only_correct
# python scripts/tokenize_data.py --input $text_dir/train_cs_zh-en.csv --output $output_dir/train/zh-en/ --only_correct
# python scripts/tokenize_data.py --input $text_dir/train_cs_en-zh.csv --output $output_dir/train/en-zh/ --only_correct

# python scripts/tokenize_data.py --input $text_dir/mono_chinese_100hr.csv --output $output_dir/mono/chinese_100hr/ --mono
# python scripts/tokenize_data.py --input $text_dir/mono_english_100hr.csv --output $output_dir/mono/english_100hr/ --mono
# python scripts/tokenize_data.py --input $text_dir/mono_french_100hr.csv --output $output_dir/mono/french_100hr/ --mono
# python scripts/tokenize_data.py --input $text_dir/mono_spanish_100hr.csv --output $output_dir/mono/spanish_100hr/ --mono

# cat $output_dir/dev/es-en/tokenized_converted.txt $output_dir/dev/fr-en/tokenized_converted.txt  $output_dir/dev/zh-en/tokenized_converted.txt  > $output_dir/dev_tokenized.txt
# cat $output_dir/test/es-en/tokenized_converted.txt  $output_dir/test/fr-en/tokenized_converted.txt  $output_dir/test/zh-en/tokenized_converted.txt  > $output_dir/test_tokenized.txt
# cat $output_dir/train/es-en/tokenized_converted.txt  $output_dir/train/fr-en/tokenized_converted.txt  $output_dir/train/zh-en/tokenized_converted.txt  $output_dir/train/en-zh/tokenized_converted.txt $output_dir/mono/chinese_100hr/tokenized_mono.txt \
#  $output_dir/mono/english_100hr/tokenized_mono.txt $output_dir/mono/french_100hr/tokenized_mono.txt $output_dir/mono/spanish_100hr/tokenized_mono.txt \
#   > $output_dir/train_tokenized.txt

cat $output_dir/dev_total/es-en/tokenized_not_converted.txt  $output_dir/dev_total/fr-en/tokenized_not_converted.txt  $output_dir/dev_total/zh-en/tokenized_not_converted.txt  > $output_dir/dev_total/tokenized_not_converted.txt