import os
import requests
import logging


class InterfaceYandex:
    def __init__(self, token: str, localPath: str, cloudPath: str):
        self._token = token
        self._localFolderPath = localPath
        self._cloudFolderPath = cloudPath
        self._headers = {'Authorization': f'OAuth {self._token}'}

    def upload_file(self, filename: str, isnew: bool, overwrite=True) -> int:
        try:
            params = {'path': os.path.join(self._cloudFolderPath, filename), 'overwrite': str(overwrite).lower()}
            response = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload', headers=self._headers,
                                    params=params)

            if response.status_code != 200 or 'href' not in response.json():
                logging.error("Upload link failed with status {}: {}".format(response.status_code, response.json()))
                return response.status_code

            with open(os.path.join(self._localFolderPath, filename), 'rb') as file_to_upload:
                upload_response = requests.put(response.json()['href'], data=file_to_upload)

            if isnew:
                logging.info("File uploaded successfully: {}".format(filename))
            else:
                logging.info("File updated successfully: {}".format(filename))
            return upload_response.status_code
        except Exception as e:
            logging.error("Failed to upload file {}: {}".format(filename, str(e)))
            raise

    def download_file(self, filename: str):
        try:
            response = requests.get('https://cloud-api.yandex.net/v1/disk/resources/download',
                                    headers=self._headers,
                                    params={'path': os.path.join(self._cloudFolderPath, filename)})

            if response.status_code != 200 or 'href' not in response.json():
                logging.error("Error fetching download link for {}: {}".format(filename, response.json()))
                return

            download_link = response.json()['href']
            download_response = requests.get(download_link)

            if download_response.status_code != 200:
                logging.error("Failed to download {}: {}".format(filename, download_response.status_code))
                return

            full_save_path = os.path.join(self._localFolderPath, filename)
            with open(full_save_path, 'wb') as f:
                f.write(download_response.content)
            logging.info("File downloaded successfully: {}".format(filename))

        except Exception as e:
            logging.error("Exception during downloading {}: {}".format(filename, str(e)))

    def delete_file(self, filename: str, permanently=False):
        try:
            params = {'path': os.path.join(self._cloudFolderPath, filename), 'permanently': str(permanently).lower()}
            response = requests.delete('https://cloud-api.yandex.net/v1/disk/resources',
                                       headers=self._headers, params=params)
            if response.status_code == 204:
                logging.info("File deleted successfully: {}".format(filename))
            else:
                logging.error("Delete failed: {} - {}".format(filename, response.text))
            return response.status_code
        except Exception as e:
            logging.error("Error deleting file {}: {}".format(filename, str(e)))
            raise

    def list_app_files(self):
        try:
            url = 'https://cloud-api.yandex.net/v1/disk/resources'
            params = {
                'path': self._cloudFolderPath,
                'fields': '_embedded.items.name'
            }
            response = requests.get(url, headers=self._headers, params=params)
            return response.json()
        except Exception as e:
            logging.error("Error fetching cloud file information")
            raise
