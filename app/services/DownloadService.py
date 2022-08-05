from time import sleep

import requests

from app.services.PhotoService import PhotoService
from app.utils.logger import get_logger


class DownloadService:
    def __init__(self, token):
        self.logger = get_logger(__name__)
        self.photoService = PhotoService(token)
        self.RESPONSE_SUCCESS_CODE = 200

    def download_photos_of_profile(self, profile_id: str):
        photo_ids_and_urls = self.photoService.get_photo_ids_and_urls(profile_id)

        for photo_id_and_url in photo_ids_and_urls:
            photo_id, photo_url = photo_id_and_url
            # Sleep is needed not to be blocked on VK server
            sleep(0.1)
            self.__download_photo(photo_id, photo_url)

    def __download_photo(self, name: str, url: str):
        try:
            self.logger.info(f'Downloading {name}')

            photo_data = self.__get_photo_data(url)
            self.__save_new_photo(name, photo_data)

        except BaseException as e:
            self.logger.error(f'Error occurred while getting photo with name: {name}\n{e}')

    def __get_photo_data(self, url: str):
        response = requests.get(url)
        if response.status_code == self.RESPONSE_SUCCESS_CODE:
            photo_content = response.content
            return photo_content

    def __save_new_photo(self, name: str, new_photo_data):
        with open(f'{name}.jpg', 'wb') as new_photo_file:
            new_photo_file.write(new_photo_data)
