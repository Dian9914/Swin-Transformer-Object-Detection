import argparse
import os
import json
import cv2
import numpy as np

def parse_args():
    parser = argparse.ArgumentParser(description='Rejoin images after doing an inference')
    parser.add_argument('dir', help='directory to get images')
    parser.add_argument('dir_save', help='output directoy')    
    parser.add_argument('dir_json', help='directory to get json')
    parser.add_argument('min_size', help='minimum defect size')
    args = parser.parse_args()
    return args
def main():
    args=parse_args()
    img_names = next(os.walk(args.dir), (None, None, []))[2]
    
    for img_name in img_names:
        print(img_name[:-4])
        path=os.path.join(args.dir, img_name)
        h=1600
        w=2600
        json_names=os.listdir(args.dir_json)
        json_list=[]
        img=cv2.imread(path)
        size=img.shape
        xmax=0
        ymax=0
        if size[1]>w or size[0]>h:
            if size[1]< 2*w: xmax=1
            elif size[1]< 3*w: xmax=2
            else: xmax=3
            if size[0]< 2*h: ymax=1
            elif size[0]< 3*h: ymax=2
            else: ymax=3
            h_real=int(size[0]/(ymax+1))
            w_real=int(size[1]/(xmax+1))
        for json_name in json_names:
            if json_name.find('.json')>0:
                if json_name.find(img_name[:-4])==0:
                    #print('Llenando la lista de json')
                    json_list.append(json_name)
        for u in json_list:

            y=int(u[u.find("_r")+2])-1
            x=int(u[u.find("_c")+2])-1
            json_path=os.path.join(args.dir_json,u)
            f=open(json_path)
            data=json.load(f)
            for def_class in data:
                for defect in data[def_class]:
                    score=data[def_class][defect]['score']
                    i=int(data[def_class][defect]['bbox'][0]+x*w_real)
                    j=int(data[def_class][defect]['bbox'][1]+y*h_real)
                    i2=int(data[def_class][defect]['bbox'][2]+x*w_real)
                    j2=int(data[def_class][defect]['bbox'][3]+y*h_real)
                    #bbx_size=[int(data[def_class][defect]['bbox'][2]),int(data[def_class][defect]['bbox'][3])]
                    if def_class=='Crack': color=(0,255,0)
                    elif def_class=='Spallation': color=(0,0,255)
                    elif def_class=='Efflorescence': color=(255,0,0)
                    elif def_class=='ExposedBars': color=(125,125,255)
                    else: color=(255,125,125)
                    print(abs(i-i2)*abs(j-j2))
                    if (abs(i-i2)*abs(j-j2)>int(args.min_size)):
                        print('Dibujando las bbox')
                        img=cv2.rectangle(img,(i,j),(i2,j2),color,25)
                        text_size, _ =cv2.getTextSize(def_class + ' | ' + score[:4],cv2.FONT_HERSHEY_SIMPLEX, 5, 10)
                        text_w,text_h=text_size
                        if (j-50>(text_h+65)):#SI LA ESQUINA SUPERIOR -5O ES MAYOR QUE EL TAMAÑO DE TEXTO-H DIBUJO EL RECTANGULO ARRIBA SI NO LO DIBUJO ABAJO
                            img=cv2.rectangle(img,(i,j-35),(i+text_w,j-text_h-65), (0,0,0), -1)
                            img=cv2.putText(img,def_class + ' | ' + score[:4], (i,j-50), cv2.FONT_HERSHEY_SIMPLEX, 5, color, 10)
                        else:
                            img=cv2.rectangle(img,(i,j2+35),(i+text_w,j2+text_h+65), (0,0,0), -1)
                            img=cv2.putText(img,def_class + ' | ' + score[:4], (i,j2+text_h+50), cv2.FONT_HERSHEY_SIMPLEX, 5, color, 10)
            data=0
            json_list=[]
            cv2.imwrite(args.dir_save + img_name[:-4]+'_end.jpg',img)  


            
        
        
  
        




if __name__=="__main__":
    main()
