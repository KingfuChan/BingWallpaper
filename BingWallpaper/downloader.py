import configparser
import json
from os import path
from urllib import request
from urllib.error import URLError  # raised when not connected to Internet

from directories import archive_dir, download_dir, main_dir


class DownloadError(Exception):
    pass


class ImageObject(object):

    def __init__(self, dictionary):  # dictionary contains infomation
        self.dict = dictionary

    def get_info(self, key):
        try:
            return self.dict[key]
        except Exception:  # if dict doesn't contain the message, ignore it
            return None

    def download_image(self, directory=download_dir):
        """download and save image. return 1 on success, DownloadError on error"""
        url_path = self.get_info('url')
        enddate = self.get_info('enddate')

        img_name = '.'.join((enddate, 'jpg'))

        try:
            # on error of connection problem raises URLError
            img_file = request.urlopen(
                f"https://cn.bing.com{url_path}").read()
        except URLError:
            raise DownloadError('Internet connection problem!')
        
        open(path.join(directory, img_name), 'wb').write(img_file)
        return 1

    def record_details(self, directory=main_dir):
        """save other information into a conf file?"""
        pass


def get_images_dicts(idx, n):
    """
    get url(s) of image(s)
    idx: -1 = from tomorrow; 0 from today; +(int) from (idx) days ago
    n: number of images.
    8 images are available for 1 request.
    images from tomorrow to 15 days ago (16 in total) can be referred.
    """

    try:
        idx, n = int(idx), int(n)
    except ValueError as v:
        raise DownloadError(
            f"{v},\nIllegal Parameters. Expect idx, n as integer")
    try:
        json_info = json.load(request.urlopen(
            f"https://cn.bing.com/HPImageArchive.aspx?format=js&idx={idx}&n={n}"))
    except URLError:
        raise DownloadError('Internet connection Problem!')

    if json_info:
        return json_info['images']
    else:
        raise DownloadError("No images found. Change parameters and retry.")


# for debug only
if __name__ == "__main__":
    pass
