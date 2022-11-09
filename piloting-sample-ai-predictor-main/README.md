# AI Predictor

- Python 3+

## Description

Sample project for pub-sub on AI Predictor for PILOTING. 

`.env` file has some basic variables needed for the project and `requirements.txt` contains basic libraries. 

IMPORTANT 

In `.env` file the following variables needs to be filled with correct values

```sh
CLIENT_SECRET
USERNAME
PASSWORD
```
 
## Clone repository

To clone the repository use the following commands:

```sh
git clone ...
cd piloting-sample-ai-predictor/
pip install -r requirements.txt
```

## Build docker container

To build the container locally run on the root folder

```sh
docker build .
```

To run the docker-compose.yml with rabbitMQ and the predictor run
```sh
docker-compose up -d
```


### Environmental variables

The environmental variables are loaded using [python-dotenv](https://pypi.org/project/python-dotenv/). The file containing the variables is named `.env`  

The environmental variables in this project are 
```sh
# api
DB_USER
DB_PASSWORD
DB_NAME
DMS_INSPECTION_PLAN_URL
DMS_MISSION_URL
DMS_MISSION_TASK_URL
DMS_INSPECTION_TASK_URL
DMS_PAYLOAD_URL
DMS_FILE_URL
DMS_FILE_METADATA_URL
TOKEN_URL
CLIENT_SECRET
USERNAME
PASSWORD
CLIENT_ID
PATCH_ANNOTATIONS_URL

# RabbitMQ
RABBITMQ_PORT
RABBITMQ_HOST
RABBITMQ_QUEUE
RABBITMQ_HEARTBEAT
```
