from mimetypes import guess_extension
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen
from re import compile
from argparse import ArgumentParser
from time import sleep

argparser = ArgumentParser(prog='Batch image downloader', description='A small utility script to batch download images from a list of urls.')
argparser.add_argument('-u', '--urls', help='Path to the text (txt) file containing the image urls. Default is urls.txt in the current dir.', default='./urls.txt', type=str)
argparser.add_argument('-i', '--images', help='Path to directory where to download the images into. Will create the dir if it does not exist. Default will create a images directory in the current dir.', default='./images', type=str)
argparser.add_argument('-c', '--clear', help='When this flag is set the script will clear the contents of the images directory.', action='store_true')
argparser.add_argument('-t', '--timeout', help="Timeout between download requests in milliseconds. Default is 250.", default=250, type=int)
args = argparser.parse_args()

CLEAR_OUTPUT_DIR = args.clear
URLS_FILE_PATH = Path(args.urls)
IMAGES_DIR_PATH = Path(args.images)
DOWNLOAD_TIMEOUT_MS = args.timeout 
URL_RGX = compile(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,4}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)')

IMAGES_DIR_PATH.mkdir(exist_ok=True)
if not IMAGES_DIR_PATH.is_dir():
    raise NotADirectoryError(f'❌ {str(IMAGES_DIR_PATH)} is not a directory') 

if CLEAR_OUTPUT_DIR:
    for file in IMAGES_DIR_PATH.iterdir():
        file.unlink()

if not URLS_FILE_PATH.exists() and URLS_FILE_PATH.is_file():
    raise FileNotFoundError('❌ File "urls.txt" was not found')

# Get links from links.txt file
with open(URLS_FILE_PATH, 'r') as urls_h:
    lines = urls_h.read().split('\n')
    urls = [*filter(lambda line: URL_RGX.match(line), lines)]

print(f'🚀 Starting download of {len(urls)} urls')

failed = 0
for idx, url in enumerate(urls):
    resp = urlopen(url)
    stat_code = resp.getcode()
    if stat_code != 200:
        failed += 1
        print(f'❌ Failed to download image. Server returned status code {stat_code}. Url: {url}')
        continue

    ext = None

    content_type_header = resp.headers.get('Content-Type')
    if content_type_header and content_type_header.startswith('image/'):
        # Guess extention from mime type
        ext = guess_extension(content_type_header)
        # We go with jpg instead of jpe
        if ext == '.jpe':
            ext = '.jpg'
    else:
        # Determine from url
        parsed_url = urlparse(url)
        split_path = parsed_url.path.split('.')
        if len(split_path) == 1:
            failed += 1
            print(f'❌ Could not determine extention for image url: {url}')
            continue
        ext = '.' + split_path[-1]

    filename = f'{idx + 1}{ext}'
    with open(IMAGES_DIR_PATH / filename, 'wb') as f:
        f.write(resp.read())
    print(f'✅ [{idx+1}/{len(urls)}] Successfully downloaded image from url: {url}')

    # Wait for next iteration
    if idx < len(urls) - 1: sleep(DOWNLOAD_TIMEOUT_MS / 1000)

print(f'🏁 Successfully downloaded {len(urls) - failed}/{len(urls)} images')
