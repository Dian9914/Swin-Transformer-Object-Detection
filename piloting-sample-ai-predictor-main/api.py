import uuid
from datetime import datetime, timedelta
import requests
import os

from requests.auth import HTTPBasicAuth

headers = {'Content-Type': 'application/json', 'authorization': ''}
urlDict = {'url': '', 'uuid': '', 'op': '', 'param': ''}


def get_file(file_id):
    """
        Get image file from server using file id
    """
    token = get_auth_token()
    url = 'https://isense-piloting.iccs.gr/apis/File/' + file_id + '/'
    return get_from_dms(url, token)


def get_auth_token():
    """ Responsible to retrieve an OAuth2 Token from the DMS"""

    payload = {'grant_type': 'password',
               'scope': 'openid',
               'client_id': os.getenv("CLIENT_ID"),
               'client_secret': os.getenv("CLIENT_SECRET"),
               'username': os.getenv("USERNAME"),
               'password': os.getenv("PASSWORD")}
    current_datetime = datetime.utcnow()
    r = requests.post(url=os.getenv("TOKEN_URL"), data=payload)
    data = r.json()
    data['expirationDate'] = current_datetime + timedelta(seconds=data['expires_in'])
    return data


def get_from_dms(url, token):
    """ Responsible to check if authorization token is alive and retrieve information from the DMS"""

    if not is_token_valid(token['expirationDate']):
        token = get_auth_token()

    headers['authorization'] = token['token_type'] + ' ' + token['access_token']
    r = requests.get(url=url, headers=headers)
    if r.status_code != 200:
        r.raise_for_status()
    return r


def is_token_valid(expiration_date):
    """ Compare expiration and current datetime
    and returns True if current datetime is prior to expiration datetime"""

    return False if datetime.utcnow() >= expiration_date else True


def create_url():
    url = urlDict['url'] + urlDict['uuid'] + urlDict['op']
    return url.strip()


def get_file_metadata(meta_id):
    token = get_auth_token()
    url = 'https://isense-piloting.iccs.gr/apis/FileMetadata/' + meta_id + '/'
    return get_from_dms(url, token)


def patch_mission(data, patch_url):
    urlDict.update(url=patch_url, uuid='', op='', param='')
    url = create_url()

    headers['Content-Type'] = "application/json"
    r = requests.patch(url=url, headers=headers, json=data,
                       auth=HTTPBasicAuth(os.getenv("USERNAME"), os.getenv("PASSWORD")))
    if r.status_code not in [200, 201]:
        print(f"ERROR in patching data : {data}")
        return None
    return r


def post_annotations(file_metadata_id, annotations):
    patch_data = [
        {
            "fileMetadataID": file_metadata_id,
            "algoType": 1,
            "regions": extract_region_obj_from_annotations(annotations)
        }]
    print(f"Posting {len(annotations)} annotations!")
    patch_mission(patch_data, os.getenv("PATCH_ANNOTATIONS_URL"))


def extract_region_obj_from_annotations(annotations):
    regions = []
    for annot in annotations:
        coords = annot["points"]
        region = {
            "id": str(uuid.uuid1())[0:8],
            "type": "polygon",
            "confidence": annot["confidence"],
            "tags": [
                "bounding box",
                "yolo",
                "corrosion"
            ],
            "boundingBox": {
                "height": coords[3],
                "width": coords[2],
                "left": coords[0],
                "top": coords[1]
            },
            "points": []
        }
        regions.append(region)
    return regions
