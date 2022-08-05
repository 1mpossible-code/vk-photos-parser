from app.api.VkAPI import VkAPI
from app.utils.logger import get_logger


class PhotoService:
    def __init__(self, token):
        self.logger = get_logger(__name__)
        self.token = token

    def get_photo_ids_and_urls(self, profile_id: str):
        photos = VkAPI.get_photos_by_profile_id(profile_id, self.token)
        return self.__create_array_of_photo_ids_and_urls(photos)

    def __create_array_of_photo_ids_and_urls(self, photos):
        photo_ids_and_urls = []

        for photo in photos:
            photo_id, photo_url = self.__get_photo_id_and_url(photo)
            photo_ids_and_urls.append((photo_id, photo_url))

        return photo_ids_and_urls

    def __get_photo_id_and_url(self, photo):
        photos_of_different_sizes_array = photo['sizes']
        # I take the last index because the photo in the end is the photo
        # of original size. Generally VK returns us array with photos
        # of different sizes, but the best quality one is the last one.
        last_size_photo_index = len(photos_of_different_sizes_array) - 1
        photo_url = photos_of_different_sizes_array[last_size_photo_index]['url']

        photo_id = photo['id']

        return photo_id, photo_url
