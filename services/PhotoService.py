from time import sleep

import requests

from logger import create_logger

logger = create_logger(__name__)


def get_photos(profile_id: str, album_type: str, token: str):
    if album_type != 'profile' and album_type != 'wall':
        err_msg = f'The type of album is wrong: {album_type}'
        logger.error(err_msg)

    try:
        res = requests.get(f'https://api.vk.com/method/photos.getAll?owner_id={profile_id}&count=200&v=5.131',
                           {'access_token': token})

        if 'error' in res.json():
            server_err_code = res.json()['error']['error_code']
            server_err_msg = res.json()['error']['error_msg']
            err_msg = f'Error {server_err_code}: {server_err_msg}'
            logger.error(err_msg)

        if len(res.json()['response']) == 0:
            err_msg = f'Profile does not have photos, or request is bad'
            logger.error(err_msg)
            return []
        return res.json()['response']['items']

    except Exception:
        logger.error('Error occurred while getting photos')


def download_photos(photos):
    for photo in photos:
        photo_id = photo['id']
        photos_of_diff_sizes = photo['sizes']

        file_url = photos_of_diff_sizes[len(photos_of_diff_sizes) - 1]['url']

        sleep(0.1)

        try:
            logger.info(f'Downloading {photo_id}')
            r = requests.get(file_url)
            if r.status_code == 200:
                with open(f'{photo_id}.jpg', 'wb') as output_file:
                    output_file.write(r.content)
        except Exception:
            logger.error(f'Error occurred while getting photo with id: {photo_id}')