from ast import arg
import json
import os
import sys

from dotenv import load_dotenv
from io import BytesIO
import numpy as np

from utils import print_env_vars
from api import post_annotations, get_file
from RabbitMQ.rabbitMQ import RabbitMQ
from PIL import Image

import torch
from mmdet.apis import inference_detector, init_detector

import argparse


classes = ['Crack','Spallation','Efflorescence','ExposedBars','CorrosionStain']

load_dotenv()
print_env_vars()

def parse_args():
    parser = argparse.ArgumentParser(description='Configure the detection model')
    parser.add_argument('dir', help='directory to inference')
    parser.add_argument('config', help='test config file path')
    parser.add_argument('checkpoint', help='checkpoint file')   
    args = parser.parse_args()
    return args

def process_mission(body):
    global model
    print(f'received message from channel with body {body}')

    message = json.loads(body)
    for img_metadata in message['images']:
        file_metadata_id = img_metadata['fileMetadataID']
        url = img_metadata['url']
        file_id = url.split("/")[-2]

        print(f"processing url {url}")

        response = get_file(file_id)
        img = np.array(Image.open(BytesIO(response.content)))

        annotations = []
        # TODO fill ai predictor

        result = inference_detector(model, img)
        result_dict = dict()
        index = 0
        for defect_class in result:
            result_dict[f'{classes[index]}']=dict()
            defect_index = 0
            for defect in defect_class:
                if defect[4]>=0.5:
                    result_dict[f'{classes[index]}'][f'defect_{defect_index}']=dict()
                    result_dict[f'{classes[index]}'][f'defect_{defect_index}']['bbox']=np.ndarray.tolist(defect[:4])
                    result_dict[f'{classes[index]}'][f'defect_{defect_index}']['score']=str(defect[4])
                    defect_index = defect_index + 1

            index=index+1

        # annotations = predictor.predict_using_array(img)

        print(f"posting annotations")
        post_annotations(file_metadata_id, annotations)


def listen_for_missions():

    rab_mq = RabbitMQ(host=os.getenv("RABBITMQ_HOST"), port=os.getenv("RABBITMQ_PORT"),
                      queue=os.getenv("RABBITMQ_QUEUE"), heartbeat=int(os.getenv("RABBITMQ_HEARTBEAT")))
    while True:
        try:
            rab_mq.consume(callback=process_mission)
        except:
            e = sys.exc_info()[0]
            print(f"Error : {e}")
            rab_mq.close()
            break

        rab_mq.consume(callback=process_mission)


def main():
    # Arg parse
    args=parse_args()
    # Prepares the inference model
    device = torch.device('cuda:0')
    global model
    model = init_detector(args.config, args.checkpoint, device=device)
    listen_for_missions()


if __name__ == "__main__":
    main()
