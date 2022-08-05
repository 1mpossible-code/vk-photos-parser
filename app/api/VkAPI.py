import requests

from app.utils.logger import get_logger


class VkAPI:
    def __init__(self):
        self.__logger = get_logger(__name__)

    def get_id_by_shortname(self, profile_shortname, token):
        response = self.__make_request_with_token(
            f'https://api.vk.com/method/users.get?user_ids={profile_shortname}&v=5.131', token)

        if 'error' in response:
            self.__logger.error(f'Error while getting id of a profile with shortname: {profile_shortname}')
            raise Exception(f'Error {response.json()["error_code"]}: {response.json()["error_message"]}')

        profile_id = str(response.json()['response'][0]['id'])
        return profile_id

    def get_photos_by_profile_id(self, profile_id, token):
        self.__logger.info(f'Getting photos of profile with id: {profile_id}')
        response = self.__make_request_with_token(
            f'https://api.vk.com/method/photos.getAll?owner_id={profile_id}&count=200&v=5.131', token)

        if 'error' in response:
            self.__logger.error(f'Error while getting photos of profile with id: {profile_id}')
            raise Exception(f'Error {response.json()["error_code"]}: {response.json()["error_message"]}')

        return response.json()['response']['items']

    def get_token(self, username, password):
        response = requests.get(
            f'https://oauth.vk.com/token?grant_type=password&client_id=2274003&client_secret=hHbZxrka2uZ6jB1inYsH'
            f'&username={username}&password={password}')

        if 'error' in response.json():
            self.__logger.error(f'Error while getting token. Maybe username of password is incorrect.')
            raise Exception(f'Error {response.json()["error_code"]}: {response.json()["error_message"]}')

        return response.json()['access_token']

    def __make_request_with_token(self, url, token):
        response = requests.get(url, {'access_token': token})
        return response.json()
