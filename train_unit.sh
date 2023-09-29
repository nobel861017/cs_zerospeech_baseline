exp_name=mhubert_kmeans_mix_unit_cs_only
run_id=unitLM_with_maxpos_6144_25k_dedup_lr1e-4
max_update=25000
total_num_update=25000
warmup_update=1000
max_positions=6144
max_tokens=20480
num_workers=16
update_freq=32
lr=0.0001

export WANDB_RUN_ID=$run_id

fairseq-train --fp16 $exp_name/bin \
    --task masked_lm --criterion masked_lm \
    --save-dir $exp_name/checkpoints/ \
    --keep-last-epochs 3 \
    --train-subset train \
    --num-workers $num_workers \
    --arch roberta_base \
    --optimizer adam --adam-betas '(0.9, 0.98)' --adam-eps 1e-06 --clip-norm 0.0 \
    --lr-scheduler polynomial_decay --lr $lr --total-num-update $total_num_update --warmup-updates $warmup_update \
    --dropout 0.1 --attention-dropout 0.1 --weight-decay 0.01 \
    --mask-multiple-length 10 --mask-prob 0.5 --mask-stdev 10 \
    --sample-break-mode eos --tokens-per-sample 3072 --max-positions $max_positions \
    --max-tokens $max_tokens --update-freq $update_freq --max-update $max_update \
    --seed 5 --log-format simple --log-interval 50 --skip-invalid-size-inputs-valid-test \
    --ddp-backend legacy_ddp --wandb-project $exp_name