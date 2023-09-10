exp=hubert-xl-en400

python scripts/compute_proba_BERT.py $exp/test/correct/dedup_not_converted.txt $exp/prob/dedup/test_correct.txt \
                                        $exp/checkpoints/checkpoint_best.pt --dict $exp/bin/dict.txt

python scripts/compute_proba_BERT.py $exp/test/wrong/dedup_not_converted.txt $exp/prob/dedup/test_wrong.txt \
                                        $exp/checkpoints/checkpoint_best.pt --dict $exp/bin/dict.txt

cat $exp/prob/dedup/test_correct.txt $exp/prob/dedup/test_wrong.txt > $exp/prob/dedup/test.txt

python scripts/evaluate_v2.py --input $exp/prob/dedup/test.txt