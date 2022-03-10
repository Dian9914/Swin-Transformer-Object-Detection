from __future__ import annotations
import cv2
import json
import random
import os
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Checks and fixes an entire dataset')
    parser.add_argument('dir', help='dataset directory')
    parser.add_argument('--reb-classes', default=False, help='Rebuild classes or not')
    parser.add_argument('--save', default=False, help='Save the output')
    parser.add_argument('--auto', default=False, help='Just process the dataset')
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
                                                        category=int(note['category_id'])
                                                        if category==1: 
                                                                defect='Background'
                                                                print('----------BACKGROUND-----------')
                                                                del ann['annotations'][index]
                                                                continue
                                                        elif category==2: 
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

                                                        note['segmentation']=[]

                                                        seg = []
                                                        # bbox[] is x1,y1,w,h
                                                        # left_top
                                                        seg.append(int(bbox[0]))
                                                        seg.append(int(bbox[1]))
                                                        # left_bottom
                                                        seg.append(int(bbox[0]))
                                                        seg.append(int(bbox[1]+bbox[3]))
                                                        # right_bottom
                                                        seg.append(int(bbox[0]+bbox[2]))
                                                        seg.append(int(bbox[1]+bbox[3]))
                                                        # right_top
                                                        seg.append(int(bbox[0]+bbox[2]))
                                                        seg.append(int(bbox[1]))

                                                        note['segmentation'].append(seg)

                                                        start_point = (bbox[0], bbox[1])
                                                        end_point = (bbox[0]+bbox[2], bbox[1]+bbox[3])
                                                        text_point = (start_point[0],round(bbox[1]+bbox[3]*random.random()))
                                                        image = cv2.rectangle(image, start_point, end_point, color, 5)
                                                        image = cv2.putText(image,defect,text_point,cv2.FONT_HERSHEY_SIMPLEX,3,color,5)
                                
                                except IndexError:
                                        pass                       
                        
                                
                                if args.reb_classes:
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
                                if args.auto: keycode = 13
                                else:
                                        cv2.imshow(f'{split} bnbox',image)
                                        keycode=cv2.waitKey()
                                print(img)
                                
                                 
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
                                if keycode==97: #a
                                        image_id=image_id-1
                                if keycode==13: #intro
                                        image_id=image_id+1
                                if keycode==99: #c
                                        print('CONTROLS: \n\t[space]: Refresh image \n\t[enter]: Next image \n\t[a]: Previous image \n\t[s]: Confine image away from dataset \n\t[f/h]: Flip image \n\t[esc]: Exit')
                                        print('[c]: Show controls again')
                                
                                
                                
                        if keycode==27:
                                break    
                        
                if args.reb_classes:
                        ann['categories'][1]['supercategory']='Structural'
                        ann['categories'][2]['supercategory']='Structural'
                        ann['categories'][3]['supercategory']='Stains'
                        ann['categories'][4]['supercategory']='Structural'
                        ann['categories'][5]['supercategory']='Stains'
                        ann['categories'].append("{'supercategory': 'Structural', 'id': 7, 'name': 'SpallatedBars'}")
                        ann['categories'].append("{'supercategory': 'Stains', 'id': 8, 'name': 'CorrodedEfflorescence'}")


                img_names = next(os.walk(os.path.join(args.dir,f'{split}/')), (None, None, []))[2] 
                
                for img_name in img_names:
                        if img_name[-4:]!='.jpg': continue
                        path=os.path.join(args.dir,f'{split}/{img_name}')
                        in_ann=False
                        for entry in ann['images']:
                                if img_name == entry['file_name']:
                                        print(entry)
                                        in_ann=True
                                        break
                        if in_ann: continue
                        else:
                                print(img_name)
                                img=cv2.imread(path)
                                id=ann['images'][-1]['id']+1
                                width,height=img.shape[0:2]
                                annotation=dict()
                                annotation['id']=id
                                annotation['file_name']=img_name
                                annotation['width']=width
                                annotation['height']=height
                                print(annotation)
                                ann['images'].append(dict(annotation))
                                print(ann['images'])

                if args.save:
                        with open(os.path.join(args.dir,f'annotations/codebrim_{split}_mod.json'), 'w') as fp:
                                json.dump(ann, fp)
        