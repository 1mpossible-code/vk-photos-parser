import os
from time import sleep

import requests
from dotenv import load_dotenv

load_dotenv()

# Get token https://vkhost.github.io/
token = os.getenv('TOKEN')

path = 'photos'

if not os.path.exists(path):
    os.makedirs(path)

os.chdir(path)

with open('../profiles.txt', 'r') as profiles:
    for profile_url in profiles:
        url = profile_url.strip()
        profile_short = url[15::]
        res = requests.get(f'https://api.vk.com/method/users.get?user_ids={profile_short}&v=5.131',
                           {'access_token': token})
        if len(res.json()['response']) == 0:
            print('Not existing profile', profile_url)
            continue
        profile_id = str(res.json()['response'][0]['id'])

        if not os.path.exists(profile_id):
            os.makedirs(profile_id)

        os.chdir(profile_id)

        print('Start processing', profile_id)

        res = requests.get(f'https://api.vk.com/method/photos.get?album_id=profile&owner_id={profile_id}&v=5.131',
                           {'access_token': token})
        res2 = requests.get(f'https://api.vk.com/method/photos.get?album_id=wall&owner_id={profile_id}&v=5.131',
                           {'access_token': token})

        if 'error' in res.json():
            print('Error:', res.json()['error']['error_code'], res.json()['error']['error_msg'])
            continue


        photos = res.json()['response']['items']
        photos2 = res2.json()['response']['items']

        def download(photos):
            for photo in photos:
                photo_id = photo['id']
                sizes = photo['sizes']
                file_url = sizes[len(sizes) - 1]['url']
                sleep(0.1)
                try:
                    print('Downloading', photo_id)
                    r = requests.get(file_url)
                    if r.status_code == 200:
                        with open(f'{photo_id}.jpg', 'wb') as output_file:
                            output_file.write(r.content)

                except OSError:
                    print(photo_id)
        download(photos)
        download(photos2)

        print(f'Success in downloading album of {profile_id}')
        os.chdir('../')
    print('Everything downloaded successfully')
