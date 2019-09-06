# pylint: disable=E0401

import datetime
import os
import sys
import time

import win10toast

import configurator
from directories import archive_dir, download_dir, main_dir, icon_dir
# icon_dir a function, use icon_dir()
from downloader import ImageObject, get_images_dicts, DownloadError


class ProcessFunctions(object):

    def __init__(self, argv=sys.argv):
        # unpack and initialize arguments
        # limit_n: limited number of images
        # noti_t: notification duration
        # retry_t: retry times
        # retry_i: retry interval
        # error_t: error times
        # ck_rst: result of checking images
        self.executable, *args = argv
        self.cwd = os.path.dirname(self.executable)
        self.error_t = 0
        self.ck_rst = {}
        try:
            self.limit_n, self.noti_d, self.retry_t, self.retry_i = args
            self.limit_n = int(self.limit_n)
            self.noti_d = int(self.noti_d)
            self.retry_t = int(self.retry_t)
            self.retry_i = int(self.retry_i)
        except Exception:  # examine if arguments are wrong or missing
            configurator.execute(sys.argv)

        os.makedirs(download_dir, exist_ok=True)
        os.makedirs(archive_dir, exist_ok=True)

    def check_img(self):  # determine by whether in the list or not
        """returns a dictionary containing the list of archive/download images"""
        file_list = os.listdir(download_dir)
        today = datetime.date.today()
        if self.limit_n <= 0:
            download_list = [f"{str(today).replace('-','')}.jpg"]
        else:
            download_list = [f"{str(today - datetime.timedelta(days=i)).replace('-','')}.jpg"
                             for i in range(0, self.limit_n)]
        # no '-' in filename

        archive_list = [l for l in file_list if not l in download_list]
        download_list = [l for l in download_list if not l in file_list]

        self.ck_rst = {'archive': archive_list, 'download': download_list}
        return self.ck_rst

    def start_download(self):
        """return 1 on success, 0 on skip, -1 on error."""
        try:
            download_list = self.ck_rst['download']
        except KeyError:
            download_list = self.check_img()['download']

        try:
            if download_list:
                # download past images at the same time
                img_list = [d for d in get_images_dicts(0, 7)]
                img_list.extend([d for d in get_images_dicts(7, 8)])
            else:
                # no need to download
                img_list = []

            dscr = {}  # initialize description list (date:description)
            for il in img_list:
                io = ImageObject(il)
                enddate = io.get_info('enddate')

                if f"{enddate}.jpg" in download_list:  # judge whether to download
                    if io.download_image():
                        dscr[enddate] = io.get_info('copyright')
                        io.record_details()

            today_str = str(datetime.date.today())
            today = today_str.replace('-', '')
            if today in dscr.keys():
                self.push_notification(f"今日（{today_str}）图片：\n{dscr[today]}。")

            return 1

        except DownloadError:
            self.error_t += 1
            if self.error_t <= self.retry_t:
                self.push_notification(
                    f"发生错误，{self.retry_i}秒后重试！\n剩余重试次数：{self.retry_t - self.error_t}")
                time.sleep(self.retry_i)
                self.check_img()  # reset ck_rst
                return self.start_download()
            else:
                self.push_notification("已达最大重试次数，程序退出！")
                sys.exit()
                return -1

    def archive_img(self):
        """return 0 on skip, 1 on success"""
        if self.limit_n <= 0:
            return 0

        try:
            archive_list = self.ck_rst['archive']
        except KeyError:
            archive_list = self.check_img()['archive']

        for al in archive_list:
            src_name = os.path.join(download_dir, al)
            dst_name = os.path.join(archive_dir, al)
            if os.path.exists(dst_name):  # prevents file exist error
                os.remove(src_name)
            else:
                os.rename(src_name, dst_name)

        return 1

    def set_wallpaper(self):
        pass

    def push_notification(self, msg):
        toast = win10toast.ToastNotifier()
        toast.show_toast(title="必应每日一图", msg=msg, duration=self.noti_d,
                         icon_path=icon_dir())


if __name__ == "__main__":

    pro = ProcessFunctions()
    pro.start_download()
    pro.archive_img()
