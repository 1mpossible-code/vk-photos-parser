from app.api.VkAPI import VkAPI
from app.utils.logger import get_logger


class ProfileService:
    def __init__(self, token):
        self.logger = get_logger(__name__)
        self.token = token

    def get_id_by_url(self, url: str):
        shortname = self.__get_profile_shortname_by_url(url)
        profile_id = VkAPI.get_id_by_shortname(shortname, self.token)
        return profile_id

    def __get_profile_shortname_by_url(self, url):
        profile_url = url.strip()
        profile_short_name = profile_url[15::]
        return profile_short_name
