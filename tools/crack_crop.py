#WIP

from __future__ import annotations
import cv2
import json
import random
import os
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Crops the cracks out of a dataset')
    parser.add_argument('dir', help='dataset directory')
    parser.add_argument('--auto', default= True, help ='Lets you go one image at a time')
    parser.add_argument('--out', default='./output/', help='Directory to save the output')
    args = parser.parse_args()
    return args

args = parse_args()

for split in ['train','val']:
        with open(os.path.join(args.dir,f'annotations/codebrim_{split}.json'),'r') as f:
                ann = json.load(f)

                image_id = 0
                while image_id < len(ann['images']):
                        entry=ann['images'][image_id]
                        img=entry['file_name']
                        id=entry['id']
                        path = os.path.join(args.dir,f'{split}/{img}')
                        print(entry)
                        if not args.auto: cv2.namedWindow(f'{split} bnbox', cv2.WINDOW_NORMAL) 
                        keycode=0
                        while(keycode!=27 and keycode!=13 and keycode!=97):

                        
                                image = cv2.imread(path)
                                spallated_bars = list()
                                corroded_efflores = list()
                                try:
                                        for index in range(len(ann['annotations'])):
                                                
                                                note = ann['annotations'][index]
                                                if note['image_id']==id:
                                                        if keycode==115:
                                                                del ann['annotations'][index]
                                                                continue
                                                        bbox=note['bbox']
                                                        note_id = note['id']
                                                        category=int(note['category_id'])
                                                        if category==1: 
                                                                defect='Crack'
                                                                color=(255,0,0)

                                                        elif category==3: 
                                                                defect='Spallation'
                                                                spallated_bars.append((bbox,index))
                                                                color=(0,255,0)
                                                        elif category==4: 
                                                                defect='Efflorescence'
                                                                corroded_efflores.append((bbox,index))
                                                                color=(0,0,255)
                                                        elif category==5: 
                                                                defect='ExposedBars'
                                                                spallated_bars.append((bbox,index))
                                                                color=(255,255,0)
                                                        elif category==6: 
                                                                defect='CorrosionStain'
                                                                spallated_bars.append((bbox,index))
                                                                corroded_efflores.append((bbox,index))
                                                                color=(255,0,255)
                                                        elif category==7: 
                                                                defect='SpallatedBars'
                                                                color=(0,255,255)
                                                        elif category==8: 
                                                                defect='CorrodedEfflorescence'
                                                                color=(255,255,255)
                                                        else: defect='ups'

                                                        start_point = (round(bbox[0]), round(bbox[1]))
                                                        end_point = (round(bbox[0]+bbox[2]), round(bbox[1]+bbox[3]))

                                                        if category==1:
                                                                cropped_image = cv2.imread(path)
                                                                cropped_image = cropped_image[start_point[1]:end_point[1],start_point[0]:end_point[0]]
                                                                if cropped_image.shape[0]>=400 and cropped_image.shape[1]>=400:
                                                                        cropped_image = cropped_image[0:min(cropped_image.shape[:2]),0:min(cropped_image.shape[:2])]
                                                                        cropped_image=cv2.resize(cropped_image, (800,800), interpolation = cv2.INTER_AREA)
                                                                        out_path=os.path.join(args.out,f'crack_{note_id}.jpg')
                                                                        cv2.imwrite(out_path,cropped_image)
                                                                        print(f'Image saved in {out_path}')

                                                        text_point = (start_point[0],round(bbox[1]+bbox[3]*random.random()))
                                                        image = cv2.rectangle(image, start_point, end_point, color, 5)
                                                        image = cv2.putText(image,defect,text_point,cv2.FONT_HERSHEY_SIMPLEX,3,color,5)
                                
                                except IndexError:
                                        pass                       

                                if keycode==115:
                                        break
                                if args.auto: keycode = 13
                                else:
                                        cv2.imshow(f'{split} bnbox',image)
                                        keycode=cv2.waitKey()
                                
                                if keycode==13: #intro
                                        image_id=image_id+1
                                
                                
                        if keycode==27:
                                break    
