import cv2
from cv2 import ROTATE_90_CLOCKWISE
import json
import random

for split in ['train','val']:
        f = open(f'./data/codebrim_coco/annotations/codebrim_{split}.json')
        ann = json.load(f)
        for entry in ann['images']:
                img=entry['file_name']
                id=entry['id']
                path = f'./data/codebrim_coco/{split}/{img}'
                print(entry)
                

                cv2.namedWindow(f'{split} bnbox', cv2.WINDOW_NORMAL) 
                image = cv2.imread(path)
                for note in ann['annotations']:
                        if note['image_id']==id:
                                print (note)
                                bbox=note['bbox']
                                category=int(note['category_id'])
                                if category==1: defect='Background'
                                elif category==2: defect='Crack'
                                elif category==3: defect='Spallation'
                                elif category==4: defect='Efflorescence'
                                elif category==5: defect='ExposedBars'
                                elif category==6: defect='CorrosionStain'
                                else: defect='ups'
                                start_point = (bbox[0], bbox[1])
                                end_point = (bbox[0]+bbox[2], bbox[1]+bbox[3])
                                text_point = (start_point[0],round(bbox[1]+bbox[3]*random.random()))
                                image = cv2.rectangle(image, start_point, end_point, (255,0,0), 5)
                                image = cv2.putText(image,defect,text_point,cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,0),5)
                cv2.imshow(f'{split} bnbox',image)
                keycode=cv2.waitKey()
                if keycode==27:
                        break       
        