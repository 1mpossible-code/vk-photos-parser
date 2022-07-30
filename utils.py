import requests

from logger import create_logger

logger = create_logger(__name__)


def get_id_by_url(url: str, token: str):
    profile_url = url.strip()
    profile_short_name = profile_url[15::]

    try:
        res = requests.get(f'https://api.vk.com/method/users.get?user_ids={profile_short_name}&v=5.131',
                           {'access_token': token})
        if len(res.json()['response']) == 0:
            logger.error('Not existing profile', url)
        profile_id = str(res.json()['response'][0]['id'])
        return profile_id
    except Exception:
        logger.error('Error occurred')
