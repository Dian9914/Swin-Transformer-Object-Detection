from __future__ import annotations
import cv2
import json
import random
import os


for split in ['train','val']:
        with open(f'./data/codebrim_coco/annotations/codebrim_{split}.json') as f:
                ann = json.load(f)

                try:
                        for image_id in range(len(ann['images'])):
                                entry=ann['images'][image_id]
                                img=entry['file_name']
                                id=entry['id']
                                path = f'./data/codebrim_coco/{split}/{img}'
                                print(entry)
                                cv2.namedWindow(f'{split} bnbox', cv2.WINDOW_NORMAL) 
                                keycode=0
                                while(keycode!=27 and keycode!=13):

                                
                                        image = cv2.imread(path)
                                        try:
                                                for index in range(len(ann['annotations'])):
                                                        note = ann['annotations'][index]
                                                        if note['image_id']==id:
                                                                if keycode==115:
                                                                        del ann['annotations'][index]
                                                                        continue
                                                                bbox=note['bbox']
                                                                category=int(note['category_id'])
                                                                if category==1: 
                                                                        defect='Background'
                                                                        print('----------BACKGROUND-----------')
                                                                        del ann['annotations'][index]
                                                                        continue
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
                                        except IndexError:
                                                pass

                                        if keycode==115:
                                                break
                                        cv2.imshow(f'{split} bnbox',image)
                                        keycode=cv2.waitKey()
                                        if keycode==102: #f
                                                image = cv2.imread(path)
                                                image=cv2.flip(image,1)
                                                cv2.imwrite(path,image)
                                        if keycode==104: #h
                                                image = cv2.imread(path)
                                                image=cv2.flip(image,0)
                                                cv2.imwrite(path,image)
                                        if keycode==115: #s
                                                os.rename(path, f'./data/no_ann/{img}')
                                                print(f'Image {img} contained')
                                                del ann['images'][image_id]
                                        
                                        
                                        
                                if keycode==27:
                                        break    
                                
                except IndexError:
                        pass

                print(ann)
                with open(f'./data/codebrim_coco/annotations/codebrim_{split}_nobg.json', 'w') as fp:
                        json.dump(ann, fp)
        