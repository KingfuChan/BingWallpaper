try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Download Bing "IMAGE OF THE DAY", manage images of past-days, (and set image as wallpaper).',
    'author': 'Keefe Chan',
    'url': '',
    'download_url': '',
    'author_email': 'cjordf2000@foxmail.com',
    'version': '0.3',
    'install_requires': ['nose', 'win10toast', 'pyqt5'],
    'packages': ['BingWallpaper'],
    'scripts': [],
    'name': 'Bing Wallpaper v3'
}

setup(**config)
