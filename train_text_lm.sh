exp_name=text-based-cs-only-scratch-5kstep
run_id=text-topline-cs
config_dir=scripts/config/text
config_name=only_cs
data_dir=/work/b08202033/zerospeech2021_baseline/datasets/text_only_cs/bin

export WANDB_RUN_ID=$run_id

fairseq-hydra-train -m --config-dir $config_dir --config-name $config_name task.data=$data_dir common.wandb_project=$exp_name