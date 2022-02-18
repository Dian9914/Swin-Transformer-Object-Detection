_base_ = './swin/mask_rcnn_swin_small_patch4_window7_mstrain_480-800_adamw_3x_coco.py'

# 1. dataset settings
dataset_type = 'CocoDataset'
classes = ('Background', 'Crack', 'Spallation', 'Efflorescence', 'ExposedBars', 'CorrosionStain')
data_root = 'data/codebrim_coco/'
data = dict(
    samples_per_gpu=1,
    workers_per_gpu=0,
    train=dict(
        type=dataset_type,
        # explicitly add your class names to the field `classes`
        classes=classes,
        ann_file=data_root + 'annotations/codebrim_train.json',
        img_prefix=data_root + 'train/'),
    val=dict(
        type=dataset_type,
        # explicitly add your class names to the field `classes`
        classes=classes,
        ann_file=data_root + 'annotations/codebrim_val.json',
        img_prefix=data_root + 'val/'),
    test=dict(
        type=dataset_type,
        # explicitly add your class names to the field `classes`
        classes=classes,
        ann_file=data_root + 'annotations/codebrim_val.json',
        img_prefix=data_root + 'val/'))
evaluation = dict(metric=['bbox'], classwise=True)


# 2. model settings

# explicitly over-write all the `num_classes` field from default 80 to 6.
model = dict(
    roi_head=dict(
        bbox_head=[
            dict(
                type='Shared2FCBBoxHead',
                # explicitly over-write all the `num_classes` field from default 80 to 6.
                num_classes=6),
            dict(
                type='Shared2FCBBoxHead',
                # explicitly over-write all the `num_classes` field from default 80 to 6.
                num_classes=6),
            dict(
                type='Shared2FCBBoxHead',
                # explicitly over-write all the `num_classes` field from default 80 to 6.
                num_classes=6)],
    # disable all the mask related stuff
    mask_roi_extractor=None,
    mask_head=None))

train_pipeline = [ dict(type='LoadAnnotations', with_bbox=True, with_mask=True),
                    dict(type='Collect', keys=['img', 'gt_bboxes', 'gt_labels'])]

# Runtime settings
checkpoint_config = dict(interval=1) # Saves checkpoint every 1 epoch