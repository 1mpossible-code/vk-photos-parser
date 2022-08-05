import os
import urllib

from dotenv import load_dotenv

from app.api.VkAPI import VkAPI
from app.utils.logger import get_logger

load_dotenv()


class TokenService:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.username = urllib.parse.quote(os.getenv('USERNAME'))
        self.password = urllib.parse.quote(os.getenv('PASSWORD'))

    def get_token(self):
        with open('./temp/token.txt', 'r') as token_file:
            token = token_file.read()
        if not token:
            self.make_new_token()
        return token

    def make_new_token(self):
        token = VkAPI().get_token(self.username, self.password)
        self.__write_token_to_file(token)

    def __write_token_to_file(self, token):
        with open('./temp/token.txt', 'w') as token_file:
            token_file.write(token)
