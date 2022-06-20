# Better version as remake_ann.py

from __future__ import annotations
import cv2
import json
import random
import os


for split in ['train','val']:
        with open(f'./data/codebrim_coco/annotations/codebrim_{split}.json') as f:
                ann = json.load(f)

                image_id = 0
                while image_id < len(ann['images']):
                        entry=ann['images'][image_id]
                        img=entry['file_name']
                        id=entry['id']
                        path = f'./data/codebrim_coco/{split}/{img}'
                        print(entry)
                        cv2.namedWindow(f'{split} bnbox', cv2.WINDOW_NORMAL) 
                        keycode=0
                        while(keycode!=27 and keycode!=13 and keycode!=97):

                        
                                image = cv2.imread(path)
                                spallated_bars = list()
                                corroded_efflores = list()
                                try:
                                        for index in range(len(ann['annotations'])):
                                                
                                                note = ann['annotations'][index]
                                                if note['image_id']==id:

                                                        print(note)
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
                                                        elif category==3: 
                                                                defect='Spallation'
                                                                spallated_bars.append((bbox,index))
                                                        elif category==4: 
                                                                defect='Efflorescence'
                                                                corroded_efflores.append((bbox,index))
                                                        elif category==5: 
                                                                defect='ExposedBars'
                                                                spallated_bars.append((bbox,index))
                                                        elif category==6: 
                                                                defect='CorrosionStain'
                                                                spallated_bars.append((bbox,index))
                                                                corroded_efflores.append((bbox,index))
                                                        elif category==7: defect='SpallatedBars'
                                                        elif category==8: defect='CorrodedEfflorescence'
                                                        else: defect='ups'

                                                        

                                                        start_point = (bbox[0], bbox[1])
                                                        end_point = (bbox[0]+bbox[2], bbox[1]+bbox[3])
                                                        text_point = (start_point[0],round(bbox[1]+bbox[3]*random.random()))
                                                        image = cv2.rectangle(image, start_point, end_point, (255,0,0), 5)
                                                        image = cv2.putText(image,defect,text_point,cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,0),5)
                                
                                except IndexError:
                                        pass                       
                        
                                
                                
                                for ind in reversed(range(len(spallated_bars))):
                                        for ind2 in reversed(range(ind)):
                                                if spallated_bars[ind][0]==spallated_bars[ind2][0] and spallated_bars[ind][1]!=spallated_bars[ind2][1]:
                                                        ann['annotations'][spallated_bars[ind2][1]]['category_id']=7
                                                        del ann['annotations'][spallated_bars[ind][1]]
                                                        print(ann['annotations'][spallated_bars[ind2][1]])
                                                        break
                                                        
                               
                                for ind in reversed(range(len(corroded_efflores))):
                                        for ind2 in reversed(range(ind)):
                                                if corroded_efflores[ind][0]==corroded_efflores[ind2][0] and corroded_efflores[ind][1]!=corroded_efflores[ind2][1]:
                                                        ann['annotations'][corroded_efflores[ind2][1]]['category_id']=8
                                                        del ann['annotations'][corroded_efflores[ind][1]]
                                                        print(ann['annotations'][corroded_efflores[ind2][1]])
                                                        break
                                 

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
                                if keycode==97 and image_id>0: #a
                                        image_id=image_id-1
                                if keycode==13: #intro
                                        image_id=image_id+1
                                if keycode==99: #c
                                        print('CONTROLS: \n\t[space]: Refresh image \n\t[enter]: Next image \n\t[a]: Previous image \n\t[s]: Confine image away from dataset \n\t[f/h]: Flip image \n\t[esc]: Exit')
                                        print('[c]: Show controls again')
                                
                                
                                
                        if keycode==27:
                                break    
                        

                ann['categories'][1]['supercategory']='Structural'
                ann['categories'][2]['supercategory']='Structural'
                ann['categories'][3]['supercategory']='Stains'
                ann['categories'][4]['supercategory']='Structural'
                ann['categories'][5]['supercategory']='Stains'
                ann['categories'].append("{'supercategory': 'Structural', 'id': 7, 'name': 'SpallatedBars'}")
                ann['categories'].append("{'supercategory': 'Stains', 'id': 8, 'name': 'CorrodedEfflorescence'}")
                print(ann['categories'])
                '''
                with open(f'./data/codebrim_coco/annotations/codebrim_{split}_V2.json', 'w') as fp:
                        json.dump(ann, fp)'''
        