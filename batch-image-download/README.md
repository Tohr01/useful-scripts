# Batch image downloader
A small utility script to batch download images from a list of urls.

## 📝 Requirements
- Python3 (pref. 3.8+)
> [!NOTE]
> This script does not depend on other Python packages and only uses the built in packages

## 🛠️ Installation
1. Download the `download.py` script
<br />
You might be getting an error like this:
```
urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1108)
```
To resolve this run the `Install Certificates.command` on macOS located in /Applications/Python 3.X/

## 🚀 Usage
```
>> python3 download.py --help
usage: Batch image downloader [-h] [-u URLS] [-i IMAGES] [-c] [-t TIMEOUT]

A small utility script to batch download images from a list of urls.

options:
  -h, --help            show this help message and exit
  -u URLS, --urls URLS  Path to the text (txt) file containing the image urls. Default is urls.txt in the current dir.
  -i IMAGES, --images IMAGES
                        Path to directory where to download the images into. Will create the dir if it does not exist. Default will create a images
                        directory in the current dir.
  -c, --clear           When this flag is set the script will clear the contents of the images directory.
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout between download requests in milliseconds. Default is 0.
```
