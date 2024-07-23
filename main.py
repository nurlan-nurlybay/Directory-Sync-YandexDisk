import configparser
import json
import logging
import os
import time
import urllib.parse
import schedule
from Interface import Interface
import atexit

logging.basicConfig(filename='sync.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


def save_local_dict(localDict, filepath):
    with open(filepath, 'w') as file:
        json.dump(localDict, file)


def load_local_dict(filepath):
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return None


def load_local_disk_data(path: str) -> dict:
    return {filename: os.path.getmtime(os.path.join(path, filename)) for filename in os.listdir(path)
            if os.path.isfile(os.path.join(path, filename))}


def load_cloud_disk_data(interface: Interface) -> set:
    file_data = set()
    json_response = interface.get_info()

    for filename in json_response["_embedded"]["items"]:
        file_data.add(filename["name"])

    return file_data


def sync(localDict: dict, cloud_set: set, localPath: str):
    try:
        cloud_set_temp = cloud_set.copy()

        for entry in os.listdir(localPath):
            full_path = os.path.join(localPath, entry)
            if os.path.isdir(full_path):
                continue
            try:
                if entry not in cloud_set:
                    Interface.load(entry)
                    cloud_set.add(entry)
                    localDict[entry] = os.path.getmtime(full_path)
                elif os.path.getmtime(full_path) != localDict[entry]:
                    Interface.reload(entry)
                    localDict[entry] = os.path.getmtime(full_path)
                    cloud_set_temp.remove(entry)
                else:
                    cloud_set_temp.remove(entry)
            except Exception as e:
                logging.error("Failed processing {}: {}".format(entry, str(e)))

        for filename in cloud_set_temp:
            try:
                Interface.delete(filename)
                cloud_set.remove(filename)
                localDict.pop(filename)
            except Exception as e:
                logging.error("Failed deleting {}: {}".format(filename, str(e)))

        save_local_dict(localDict, 'local_dict.json')

    except Exception as e:
        logging.error("Sync operation failed: {}".format(str(e)))


config = configparser.ConfigParser()
config.read('config.ini')
local_folder_path = config["DEFAULT"]["LocalFolderPath"]
cloud_folder_path = urllib.parse.quote(config["DEFAULT"]["CloudFolderPath"], safe=':/')
token = config["DEFAULT"]["AccessToken"]
interval = config.getint("DEFAULT", "SyncInterval")
local_dict_path = 'local_dict.json'

Interface = Interface(token, local_folder_path, cloud_folder_path)

local_dict = load_local_dict(local_dict_path)
if local_dict is None:
    local_dict = load_local_disk_data(local_folder_path)
cloud_files = load_cloud_disk_data(Interface)


@atexit.register
def last_sync() -> None:
    sync(local_dict, cloud_files, local_folder_path)


if __name__ == "__main__":
    sync(local_dict, cloud_files, local_folder_path)

    schedule.every(interval).minutes.do(lambda: sync(local_dict, cloud_files, local_folder_path))
    while True:
        schedule.run_pending()
        time.sleep(1)
