#!/usr/bin/env bash

python tools/train.py configs/alora_swin_3x.py --work-dir /workspace/output/train_alora/ --resume-from /workspace/output/train_alora/epoch_100.pth