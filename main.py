import os

from dotenv import load_dotenv

from logger import create_logger
from services.PhotoService import download_photos, get_photos
from utils import get_id_by_url

load_dotenv()

# Get token https://vkhost.github.io/
token = os.getenv('TOKEN')

logger = create_logger(__name__)


def create_and_jump_in_directory(directory: str):
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.chdir(directory)


def init_photos_directory(photos_dir):
    create_and_jump_in_directory(photos_dir)


def main():
    with open('../profiles.txt', 'r') as profiles:
        for profile_url in profiles:
            profile_id = get_id_by_url(profile_url, token)

            logger.info(f'Start processing {profile_id}')

            create_and_jump_in_directory(str(profile_id))

            photos_urls = get_photos(profile_id, 'profile', token)

            try:
                if len(photos_urls) == 0:
                    logger.warning(f'Profile {profile_id} does not have photos')
                    raise Exception('No photos')
                download_photos(photos_urls)
                with open('../../proceed.txt', 'a') as proceed:
                    proceed.write(f'\n{profile_url.strip()}')

                logger.info(f'Success in downloading album of user with id: {profile_id}')
                os.chdir('../')
            except Exception:
                with open('../../failed.txt', 'a') as failed:
                    failed.write(f'\n{profile_url.strip()}')
                logger.error('Some error occurred while downloading photos')
                os.chdir('../')
                os.rmdir(f'./{profile_id}')

        logger.info('The process for all profiles completed successfully')


if __name__ == '__main__':
    init_photos_directory('photos')
    main()
