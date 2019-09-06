import sys
from os import path

main_dir = path.dirname(sys.argv[0])
download_dir = path.join(main_dir, 'download')
archive_dir = path.join(main_dir, 'archived')

def icon_dir():
    if getattr(sys, 'frozen', False):
        # running in a bundle (pyinstaller exe)
        return path.join(str(sys._MEIPASS), "Bing.ico")
    else:
        # running live
        return path.join(main_dir, "Bing.ico")
