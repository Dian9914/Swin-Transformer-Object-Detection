#!/usr/bin/env bash

python tools/train.py configs/no_mask_config_1x.py --work-dir /workspace/output/train_1/
python tools/train.py configs/no_mask_config_3x.py --work-dir /workspace/output/train_2/