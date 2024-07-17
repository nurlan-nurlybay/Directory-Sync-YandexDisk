from InterfaceYandex import InterfaceYandex


class Interface:
    def __init__(self, token: str, localPath: str, cloudPath: str):
        self._token = token
        self._localFolderPath = localPath
        self._cloudFolderPath = cloudPath
        self._headers = {'Authorization': f'OAuth {self._token}'}
        self._service = InterfaceYandex(token, localPath, cloudPath)

    def load(self, filename):
        return self._service.upload_file(filename, isnew=True)

    def reload(self, filename):
        return self._service.upload_file(filename, isnew=False)

    def delete(self, filename):
        return self._service.delete_file(filename)

    def get_info(self):
        return self._service.list_app_files()
