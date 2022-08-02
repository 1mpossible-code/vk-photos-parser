import os
import urllib

import requests
from dotenv import load_dotenv

from logger import create_logger

load_dotenv()

logger = create_logger(__name__)


def get_token():
    try:
        username = urllib.parse.quote(os.getenv('USERNAME'))
        password = urllib.parse.quote(os.getenv('PASSWORD'))

        res = requests.get(
            f'https://oauth.vk.com/token?grant_type=password&client_id=2274003&client_secret=hHbZxrka2uZ6jB1inYsH'
            f'&username={username}&password={password}')

        return res.json()['access_token']

    except KeyError:
        err_msg = 'Username of password is incorrect'
        logger.error(err_msg)
        raise Exception(err_msg)
    except BaseException as e:
        logger.error(f'Some error occurred while getting new token: {e}')


def make_new_token():
    logger.info('Start getting new token...')
    with open('../token.txt', 'w') as token_file:
        token_file.write(get_token())
    logger.info('New token got successfully!')
