import configparser
import os
import urllib.parse

import requests


class Interface:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self._token = config["DEFAULT"]["AccessToken"]
        self._localFolderPath = config["DEFAULT"]["LocalFolderPath"]

        cloud_folder_path = config["DEFAULT"]["CloudFolderPath"]
        self._cloudFolderPath = urllib.parse.quote(cloud_folder_path, safe=':/')

    @property
    def headers(self):
        return {'Authorization': f'OAuth {self._token}'}

    def upload_file(self, filename: str, overwrite=True):
        params = {
            'path': os.path.join(self._cloudFolderPath, filename),
            'overwrite': str(overwrite).lower()  # Convert boolean to 'true'/'false'
        }

        response = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload',
                                headers=self.headers, params=params)

        if response.status_code != 200 or 'href' not in response.json():
            raise RuntimeError("problem with getting an upload link."
                               " response.status_code: {}, 'href' in response.json(): {}\n{}"
                               .format(response.status_code, 'href' in response.json(), response.json()))

        with open(os.path.join(self._localFolderPath, filename), 'rb') as file_to_upload:
            response2 = requests.put(response.json()['href'], data=file_to_upload)

        return response2.status_code

    def get_user_disk_info(self):
        response = requests.get('https://cloud-api.yandex.net/v1/disk/', headers=self.headers)
        return response.json()

    def download_file(self, filename: str):
        response = requests.get('https://cloud-api.yandex.net/v1/disk/resources/download',
                                headers=self.headers, params={'path': os.path.join(self._cloudFolderPath, filename)})

        if response.status_code != 200 or 'href' not in response.json():
            raise RuntimeError("Error in fetching download link")

        download_link = response.json()['href']
        download_response = requests.get(download_link)

        if download_response.status_code != 200:
            raise RuntimeError("Failed to download a file")

        full_save_path = os.path.join(self._localFolderPath, filename)
        with open(full_save_path, 'wb') as f:
            f.write(download_response.content)

        return download_response.status_code

    def delete_file(self, filename: str, permanently=False):
        path = os.path.join(self._cloudFolderPath, filename)
        params = {
            'path': path,
            'permanently': str(permanently).lower()  # Convert boolean to 'true'/'false'
        }
        response = requests.delete('https://cloud-api.yandex.net/v1/disk/resources',
                                   headers=self.headers, params=params)
        return response.status_code  # Access status_code directly from response

