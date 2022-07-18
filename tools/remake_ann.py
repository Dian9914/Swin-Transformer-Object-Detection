#WIP

from __future__ import annotations
import cv2
import json
import random
import os

print('CONTROLS: \n\t[space]: Refresh image \n\t[enter]: Next image \n\t[a]: Previous image \n\t[s]: Confine image away from dataset \n\t[f/h]: Flip image \n\t[esc]: Exit')
print('[c]: Show controls again')

if not os.path.isdir(f'./data/no_ann/'):
        os.mkdir(f'./data/no_ann/')

for split in ['train','val']:
        with open(f'./data/codebrim_coco/annotations/codebrim_{split}.json') as f:
                ann = json.load(f)
                image_id = 0
                while image_id < len(ann['images']):
                        entry=ann['images'][image_id]
                        img=entry['file_name']
                        id=entry['id']

                        print(f'Showing image {img} with id {image_id}')
                        print(entry)

                        area_image=entry['width']*entry['height']
                        path = f'./data/codebrim_coco/{split}/{img}'
                        cv2.namedWindow(f'{split} bnbox', cv2.WINDOW_NORMAL) 
                        keycode=0
                        while(keycode!=27 and keycode!=13 and keycode!=97):

                        
                                image = cv2.imread(path)
                                bboxes = list()
                                indexes = list()
                                index2erase = list()
                                try:
                                        for index in range(len(ann['annotations'])):
                                                note = ann['annotations'][index]
                                                if note['image_id']==id:
                                                        print(note)
                                                        if keycode==115:
                                                                del ann['annotations'][index]
                                                                continue
                                                        bbox=note['bbox']
                                                        area=note['area']
                                                        category=int(note['category_id'])
                                                        if category==1: 
                                                                defect='Background'
                                                                print('Background detected and erased!')
                                                                del ann['annotations'][index]
                                                                continue
                                                        else: defect=f'Defect {index}'
                                                        ann['annotations'][index]['category_id']=2

                                                        start_point = (bbox[0], bbox[1])
                                                        end_point = (bbox[0]+bbox[2], bbox[1]+bbox[3])
                                                        text_point = (start_point[0],round(bbox[1]+bbox[3]*random.random()))
                                                        image = cv2.rectangle(image, start_point, end_point, (255,0,0), 5)
                                                        image = cv2.putText(image,defect,text_point,cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,0),5)

                                                        #buscamos buscar que bboxes estan contenidas en otras
                                                        #entre todos los pares posibles de bboxes para una imagen

                                                        #antes hemos comprobar si alguna bounding box coincide con el area total de la imagen, 
                                                        #pues no no es de interes mantenerla ni compararla
                                                        overlap_image=area/area_image
                                                        if overlap_image>=0.8 and area_image>3000000:
                                                                index2erase.append(index)
                                                                continue

                                                        for index_a in indexes:
                                                                bbox_a = ann['annotations'][index_a]['bbox']
                                                                print('------------------------------------')
                                                                print(f'Comparing {bbox} with index {index} with {bbox_a} with index {index_a}')
                                                                start_point_a=(bbox_a[0], bbox_a[1])
                                                                end_point_a = (bbox_a[0]+bbox_a[2], bbox_a[1]+bbox_a[3])

                                                                #rectangulo de interseccion
                                                                start_point_i=(max(start_point_a[0],start_point[0]), max(start_point_a[1],start_point[1]))
                                                                end_point_i=(min(end_point_a[0],end_point[0]), min(end_point_a[1],end_point[1]))
                                                                print(start_point_i,end_point_i)

                                                                area_a=ann['annotations'][index_a]['area']
                                                                area_i=(end_point_i[0]-start_point_i[0])*((end_point_i[1]-start_point_i[1]))

                                                                
                                                                overlap=area_i/area
                                                                print(overlap)
                                                                overlap_a=area_i/area_a
                                                                print(overlap_a)

                                                                #si el rectangulo tiene el start point por debajo del end point o a su derecha
                                                                #o el area es negativa o el overlap sea mayor que 1, es que no intersectan
                                                                if start_point_i[0]>end_point_i[0] or start_point_a[1]>end_point_i[1] or area_i<0 or overlap>1 or overlap_a>1:
                                                                        print('No intersection.')
                                                                        continue

                                                                #si el rectangulo de interseccion tiene un area muy similar a alguna de las bboxes, es que esa bbox
                                                                #esta practicamente contenida en la otra

                                                                if overlap>=0.85:
                                                                        index2erase.append(index)
                                                                elif overlap_a>=0.85:
                                                                        index2erase.append(index_a)
                                                                
                                                        bboxes.append(bbox)
                                                        indexes.append(index)
                                        print('--------------------------')
                                        for index in reversed(list(set(index2erase))):
                                                bbox=ann['annotations'][index]['bbox']
                                                print(f'Deleting bbox {bbox} with index {index}...')
                                                del ann['annotations'][index]
                                        print('Press [space] to refresh.')

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
                                if keycode==97 and image_id>0: #a
                                        image_id=image_id-1
                                if keycode==13: #intro
                                        image_id=image_id+1
                                if keycode==99: #c
                                        print('CONTROLS: \n\t[space]: Refresh image \n\t[enter]: Next image \n\t[a]: Previous image \n\t[s]: Confine image away from dataset \n\t[f/h]: Flip image \n\t[esc]: Exit')
                                        print('[c]: Show controls again')
                                
                                
                        if keycode==27:
                                break    
                        
                
                print(ann)
                with open(f'./data/codebrim_coco/annotations/codebrim_{split}_defect.json', 'w') as fp:
                        json.dump(ann, fp)
        