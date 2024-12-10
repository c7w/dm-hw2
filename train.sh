# best for dataset 1
CUDA_VISIBLE_DEVICES=1 python3 experiment.py -d bank-marketing -bs 256 -s 3@16@512 -e401 -lrde 200 -lr 0.0002 -ki 0 -i 0 -wd 0.000 --print_rule

# Best for dataset 2
CUDA_VISIBLE_DEVICES=5 python3 experiment.py -d housing -bs 32 -s 9@32@512 -e101 -lrde 50 -lr 0.0001 -ki 0 -i 0 -wd 0.000 --print_rule

# Best for dataset 3
CUDA_VISIBLE_DEVICES=3 python3 experiment.py -d breast-cancer -bs 16 -s 3@512 -e51 -lrde 200 -lr 0.0002 -ki 0 -i 0 -wd 0.000 --print_rule
# /Node10_nvme/gaoha/rrl/log_folder/breast-cancer/breast-cancer_e51_bs16_lr0.0002_lrdr0.75_lrde200_wd0.0_ki0_rc0_useNOTFalse_saveBestFalse_useNLAFFalse_estimatedGradFalse_useSkipFalse_alpha0.999_beta8_gamma1_temp1.0_L3@512