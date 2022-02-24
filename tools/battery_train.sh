#!/usr/bin/env bash

python tools/train.py configs/no_mask_config_3x_7_classes.py --work-dir /workspace/output/train_3x_7cl/
python tools/train.py configs/no_mask_config_3x.py --work-dir /workspace/output/train_3x_base/
python tools/train.py configs/no_mask_config_3x_defo.py --work-dir /workspace/output/train_3x_defo/