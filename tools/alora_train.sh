#!/usr/bin/env bash

python tools/train.py configs/alora_swin_3x.py --work-dir /workspace/output/train_codebrim/ --resume-from checkpoints/codebrim_swin_epoch_60.pth 