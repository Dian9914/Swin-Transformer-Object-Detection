import argparse
import os
import json
import cv2

def parse_args():
    parser = argparse.ArgumentParser(description='Rejoin images after doing an inference')
    parser.add_argument('dir', help='directory to get images')
    parser.add_argument('dir_save', help='output directoy')    
    parser.add_argument('dir_json', help='directory to get json')
    parser.add_argument('dir_def', help='directory to get images with defect')
    args = parser.parse_args()
    return args
def main():
    args=parse_args()
    img_names = next(os.walk(args.dir), (None, None, []))[2]
    
    for img_name in img_names:
        path=os.path.join(args.dir, img_name)
        h=1600
        w=2600
        json_names=os.listdir(args.dir_json)
        json_list=[]
        img=cv2.read(path)
        size=img.size
        x=0
        y=0
        if size[1]< w and size[2]<h:
            if size[1]< 2*w: x=1
            elif size[1]< 3*w: x=2
            else: x=3
            if size[2]< 2*h: y=1
            elif size[2]< 3*h: y=2
            else: x=3
        for json_name in json_names:
            if json_name.find(img_name):
                json_list.append(json_name)
        for u in json_list:
            x=int(u(u.find("_r")+1))
            y=int(u(u.find("_c")+1))
            json_path=os.path.join(args.dir_json,i)
            f=open(json_path)
            data=json.load(f)
            for def_class in data:
                for defect in def_class:
                    i=defect.bbx[1]+x*w
                    j=defect.bbx[2]+y*h
                    bbx_size=[defect.bbx[3],defect.bbx[4]]
                    score=defect.score
                    if def_class=='Crack': color=(0,255,0)
                    elif def_class=='Spallation': color=(0,0,255)
                    elif def_class=='Efflorescence': color=(255,0,0)
                    elif def_class=='ExposedBars': color(125,125,0)
                    else: color=(0,125,125)
                    cv2.rectangle(img,(i,j),(i+bbx_size[1],j+bbx_size[2]),color,5)
                    cv2.putText(img,def_class, (i,j-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color)
        cv2.write(args.dir_save + img_name[:-4]+'_end.jpg',)  


            
        
        
  
        




if __name__=="__main__":
    main()
