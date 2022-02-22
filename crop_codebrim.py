
import cv2
import json
import random
from math import floor

for split in ['train','val']:
        f = open(f'./data/codebrim_coco/annotations/codebrim_{split}.json')
        ann = json.load(f)
        for entry in ann['images']:
                img=entry['file_name']
                id=entry['id']
                width=entry['width']
                height=entry['height']
                path = f'./data/codebrim_coco/{split}/{img}'
                image = cv2.imread(path)

                if width>2000 or height>2000:
                    print(f'Cropping image {img}...')

                    if width<3000: tile_w_n=2
                    elif width<4500: tile_w_n=3
                    else: tile_w_n=4
                        
                    tile_width=floor(width/tile_w_n)

                    if height<3000: tile_h_n=2
                    elif height<4500: tile_h_n=3
                    else: tile_h_n=4

                    tile_height=floor(height/tile_h_n)

                    tile_num=tile_w_n*tile_h_n

                    cv2.namedWindow(f'{img} crops', cv2.WINDOW_NORMAL) 
                    for index_w in range(tile_w_n):
                        for index_h in range(tile_h_n):
                            crop = image[tile_height*index_h:tile_height*(index_h+1),tile_width*index_w:tile_width*(index_w+1)]
                            
                            cv2.imwrite('./data/cropped/{}/{}_{:02}_{:02}.jpg'.format(split,img[0:-4],index_h,index_w),crop)
                            cv2.imshow(f'{img} crops',crop)
                            keycode=cv2.waitKey()
                    if keycode==27: break        

                    print(f'Image {img} cropped in {tile_num} tiles!')

                    print(f'Reannotating image {img}...')
                    
                    for note in ann['annotations']:
                        if note['image_id']==id:
                                print (note)
                                bbox=note['bbox']
                                category=int(note['category_id'])
                                if category==1: continue #defect='Background'
                                elif category==2: defect='Crack'
                                elif category==3: defect='Spallation'
                                elif category==4: defect='Efflorescence'
                                elif category==5: defect='ExposedBars'
                                elif category==6: defect='CorrosionStain'
                                else: defect='ups'
                                start_point = (bbox[0], bbox[1])
                                end_point = (bbox[0]+bbox[2], bbox[1]+bbox[3])

                                for index_w in range(tile_w_n):
                                    for index_h in range(tile_h_n):
                                        start_crop=(tile_height*index_h,tile_width*index_w)
                                        end_crop=(tile_height*(index_h+1),tile_width*(index_w+1))
                                        # if the start point is within the crop
                                        if start_point[0]>start_crop[0] and start_point[1]>start_crop[1] and start_point[0]<end_crop[0] and start_point[1]<end_crop[1]:
                                            # if the bbox is contained within the crop
                                            if end_point[0]>end_crop[0] and end_point[1]>end_crop[1]:
                                                #the bbox belongs to crop_w_h'
                                                crop_bbox=(start_point[0],start_point[1],end_point[0],end_point[1])

                                            # if the bbox isn't contained in the crop
                                            else: 
                                                # the bbox has to be cropped
                                                crop_bbox=(start_point[0],start_point[1],end_crop[0],end_crop[1])
                                                if end_crop[0]>end_point[0]: crop_bbox[2]=end_point[0]
                                                if end_crop[1]>end_point[1]: crop_bbox[3]=end_point[1]
                                        
                                        # if only end point is within the crop
                                        elif end_point[0]>start_crop[0] and end_point[1]>start_crop[1] and end_point[0]<end_crop[0] and end_point[1]<end_crop[1]:
                                            crop_bbox = 




                else:
                    print(f'Image {img} too small to be cropped')
        