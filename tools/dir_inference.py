import argparse

import cv2
import torch
import os
import os.path as osp
import json
import numpy as np

import time

from mmdet.apis import inference_detector, init_detector
from mmdet.datasets import CocoDataset



def parse_args():
    classes = ['Crack','Spallation','Efflorescence','ExposedBars','CorrosionStain']
    parser = argparse.ArgumentParser(description='Does an inference to an entire directory')
    parser.add_argument('dir', help='directory to inference')
    parser.add_argument('config', help='test config file path')
    parser.add_argument('checkpoint', help='checkpoint file')    
    parser.add_argument(
        '--out-dir', type=str, default='results/dir_inference', help='output directory')
    parser.add_argument(
        '--device', type=str, default='cuda:0', help='CPU/CUDA device option')
    parser.add_argument(
        '--score-thr', type=float, default=0.5, help='bbox score threshold')
    parser.add_argument(
        '--classes', type=list, default=classes, help='classes to detect')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    classes = args.classes

    o_path_def=os.path.join(args.out_dir,'defect/')
    o_path_nodef=os.path.join(args.out_dir,'no_defect/')

    if not os.path.isdir(args.out_dir):
        os.mkdir(args.out_dir)

    if not os.path.isdir(o_path_def):
        os.mkdir(o_path_def)

    if not os.path.isdir(o_path_nodef):
        os.mkdir(o_path_nodef)

    device = torch.device(args.device)

    model = init_detector(args.config, args.checkpoint, device=device)

    print('Inferencing directory')
    img_names = next(os.walk(args.dir), (None, None, []))[2] 
    print(img_names)
    for img_name in img_names:
        path=os.path.join(args.dir, img_name)
        img= cv2.imread(path)

        start=time.time()
        result = inference_detector(model, img)
        result_dict = dict()
        elapsed_time=time.time()-start

        o_path=o_path_nodef
        index = 0
        for defect_class in result:
            result_dict[f'{classes[index]}']=dict()
            defect_index = 0
            for defect in defect_class:
                if defect[4]>=args.score_thr:
                    result_dict[f'{classes[index]}'][f'defect_{defect_index}']=dict()
                    result_dict[f'{classes[index]}'][f'defect_{defect_index}']['bbox']=np.ndarray.tolist(defect[:4])
                    result_dict[f'{classes[index]}'][f'defect_{defect_index}']['score']=str(defect[4])
                    defect_index = defect_index + 1
                    o_path=o_path_def
                    print('defect')

            index=index+1

        with open(osp.join(args.out_dir,f'result_{img_name[:-4]}.json'), 'w') as outf:
            json.dump(dict(result_dict), outf)
        
        o_path=os.path.join(o_path, img_name)

        cv2.imwrite(o_path,model.show_result(
            img, result, score_thr=args.score_thr, wait_time=0, show=False, thickness=15, font_size=40))       

        print(f'Inference time: {elapsed_time}')


if __name__ == '__main__':
    main()