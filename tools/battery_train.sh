#!/usr/bin/env bash

python tools/train.py configs/no_mask_config_1x.py --work_dir /workspace/output/train_1/
python tools/train.py configs/no_mask_config_2x.py --work_dir /workspace/output/train_2/