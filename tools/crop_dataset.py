import argparse
import cv2
import random
from math import floor
import os

def parse_args():
    parser = argparse.ArgumentParser(description='Crops all the images within an entire directory')
    parser.add_argument('dir', help='directory to crop')
    parser.add_argument(
        '--out-dir', type=str, default='~/piloting/dataset/cropped/', help='output directory')
    parser.add_argument(
        '--max-height', type=int, default=1600, help='max resolution for the crops')
    parser.add_argument(
        '--max-width', type=int, default=2600, help='max resolution for the crops')
    parser.add_argument(
        '--manual', type=bool, default=False, help='enable preview')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    if not os.path.isdir(args.out_dir):
            os.mkdir(args.out_dir)

    img_names = next(os.walk(args.dir), (None, None, []))[2] 

    for img_name in img_names:
        path=os.path.join(args.dir, img_name)

        img = cv2.imread(path)
        print(img.shape)

        width,height=img.shape[0:2]
        print(width,height)

        if width>args.max_width or height>args.max_height:
            print(f'Cropping image {img_name}...')

            if width<args.max_width*2: tile_w_n=2
            elif width<args.max_width*3: tile_w_n=3
            else: tile_w_n=4
                
            tile_width=floor(width/tile_w_n)

            if height<args.max_height*2: tile_h_n=2
            elif height<args.max_height*3: tile_h_n=3
            else: tile_h_n=4

            tile_height=floor(height/tile_h_n)

            tile_num=tile_w_n*tile_h_n

            if args.manual: cv2.namedWindow(f'{img_name} crops', cv2.WINDOW_NORMAL) 
            
            for index_w in range(tile_w_n):
                for index_h in range(tile_h_n):
                    crop = img[tile_width*index_w:tile_width*(index_w+1),tile_height*index_h:tile_height*(index_h+1)]
                    
                    cv2.imwrite(os.path.join(args.out_dir,'{}_{:02}_{:02}.jpg'.format(img_name[0:-4],index_h,index_w)),crop)
                    if args.manual:    
                        cv2.imshow(f'{img_name} crops',crop)
                        keycode=cv2.waitKey()
                    else: keycode=1
            if keycode==27: break        

            print(f'Image {img_name} cropped in {tile_num} tiles!')

        else:
            print(f'Image {img_name} too small to be cropped')
            

if __name__ == '__main__':
    main()