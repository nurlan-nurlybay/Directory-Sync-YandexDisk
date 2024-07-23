# Local Directory - Yandex Disk Synchronization

## Purpose and Usage
The program is used to actively synchronize a local directory of your choice 
with a Yandex Disk folder. When you run the program, it will make the first 
synchronization. Then, at time intervals you set. Developer's suggestion - 
10 minutes. Every 10 minutes, any updated and new files will be uploaded to 
the cloud. Any deleted files will be deleted from the cloud too, but not 
permanently - you can restore them from the trash folder in Yandex Disk within 
a month. When you terminate the program, then turn it back on later, consider it 
temporarily extending the time interval between synchronizations. 

It might be useful if you are working on a project, and you want to make sure 
that the updates made to the project are preserved at all times.

It also might help you work on a project from different devices.
You can synchronize the same Yandex Disk folder with multiple laptops, 
and they will all share the same folder. However, the program does not 
make it very convenient yet. If you sync the same cloud directory with 
multiple devices, when you add a new file to one of them, 
it will load it to cloud when the sync time comes. However, when sync time 
comes for another device, instead of uploading the new file from the cloud, 
it will delete it from there because the program does not see it locally. 
Please figure this out, updates are welcome, I have prepared a download 
method for you in InterfaceYandex. 

## Features

- Synchronizes a local directory with a folder in Yandex Disk on time intervals.  
- Uploads any new files - if it does not see the filename in cloud.
- Uploads any changed files and replaces with existing ones in the cloud - checks 
for the files' metadata and compares 'last modified' with the one it keeps in memory 
every sync round.
- Deletes all the files from the cloud that are missing in the local directory. 

## Installation

To run this program, you need Python 3.12+ and some packages from the Python package index. Follow these steps to set up:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/nurlan-nurlybay/Directory-Sync-YandexDisk.git
   cd Directory-Sync-YandexDisk

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt

3. **Set up configurations:**
   ```bash
   Go to https://yandex.ru/dev/disk/poligon/ and generate your token.
   Copy paste it to the value of AccessToken in config.ini.
   Choose your local folder, and insert its path to LocalFolderPath.
   Choose a folder in Yandex Disk (if there are no folders, I recommend you to create one instead of using the root folder)
   Actually, when you get your token, and make your first request with it, Yandex Disk automatically creates an app folder. 
   This folder is bound to the token, so it is better if you use it unless you want multiple folders.
   It is not crucial, though. You are free to use any folder.
   SyncInterval = 1 means the sync will occur every minute. Change it to 10 
   
4. **Run the program:**
   ```bash
   python main.py

## Usage

After you start the program, you forget it exists. It will make the last time sync when you terminate it. 
Just do not terminate it by closing the terminal on which it is running, do it properly: ctrl+C or stop button in your IDE.
Then, turn it back on when you come back to your project. 


## Contributions
Contributions are welcome! Please fork the repository and submit a pull request with your features or fixes.

## License
The project is unlicensed.
