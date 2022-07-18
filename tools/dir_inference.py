# Realiza una inferencia a todas las imagenes de un directorio utilizando mmdetection. Te devuelve el resultado clasificado entre defecto y no defecto.

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
from dataset_cropper import Image_Cropper


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
    parser.add_argument(
        '--max-height', type=int, default=1600, help='max resolution for the crops')
    parser.add_argument(
        '--max-width', type=int, default=2600, help='max resolution for the crops')
    args = parser.parse_args()
    return args

def main():
    # Reads the arguments
    args = parse_args()
    classes = args.classes

    # Prepares the paths and creates the directories if needed
    o_path_def=os.path.join(args.out_dir,'defect/')
    o_path_nodef=os.path.join(args.out_dir,'no_defect/')

    if not os.path.isdir(args.out_dir):
        os.mkdir(args.out_dir)

    if not os.path.isdir(o_path_def):
        os.mkdir(o_path_def)

    if not os.path.isdir(o_path_nodef):
        os.mkdir(o_path_nodef)

    # Creates the cropper
    cropper = Image_Cropper(args.max_height, args.max_width)

    # Prepares the inference model
    device = torch.device(args.device)
    model = init_detector(args.config, args.checkpoint, device=device)

    # Starts processing the directory, one image at a time
    print('Inferencing directory')
    img_names = next(os.walk(args.dir), (None, None, []))[2] 
    img_counter = 1
    for img_name in img_names:
        path=os.path.join(args.dir, img_name)
        source_img= cv2.imread(path)
        print(f'Processing image {img_counter} of {len(img_names)}')
        # Gets a list of crops with the desired resolution
        (crops, n_rows, n_cols) = cropper.crop(source_img)
        
        row = 1
        col = 1
        crop_counter = 1
        for img in crops:
            print(f'Procesing crop {crop_counter} of image {img_counter}.')
            start=time.time()
            result = inference_detector(model, img)
            result_dict = dict()
            infer_time=time.time()-start

            o_path=o_path_nodef
            index = 0
            isdefect = False
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
                        isdefect = True

                index=index+1

            if isdefect: 
                with open(osp.join(args.out_dir,f'{img_name[:-4]}_r{row}_c{col}.json'), 'w') as outf: json.dump(dict(result_dict), outf)
            
            o_path=os.path.join(o_path, f'{img_name[:-4]}_r{row}_c{col}.jpg')

            cv2.imwrite(o_path,model.show_result(
                img, result, score_thr=args.score_thr, wait_time=0, show=False, thickness=15, font_size=40))  

            elapsed_time=time.time()-start
            print(f'Processing time: {elapsed_time}, Inference time: {infer_time}')
            crop_counter = crop_counter + 1    
            if row < n_rows: row = row + 1
            else: 
                col = col + 1
                row = 1
        
        print('')
        img_counter = img_counter+1 


if __name__ == '__main__':
    main()