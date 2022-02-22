#!/usr/bin/env bash

python tools/train.py configs/no_mask_config_1x_defo.py --work-dir /workspace/output/train_defo_1x/
python tools/train.py configs/no_mask_config_3x_defo.py --work-dir /workspace/output/train_defo_3x/