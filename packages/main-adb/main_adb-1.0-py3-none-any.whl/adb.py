"""
-*- coding: utf-8 -*-
@File  : adb.py
@Author: Waton
@Date  : 2024/8/31
@Desc  : adb 操作
"""

import os


class Adb:
    def __init__(self, device_ip, package_path=None):
        """
        初始化adb
        :param device_ip: 设备ip
        :param package_path: 安装包地址
        """
        self.device_ip = device_ip
        self.package_path = package_path

    def connect(self):
        os.system('chcp 65001')
        return os.system(f'adb connect {self.device_ip}')

    def disconnect(self):
        return os.system(f'adb disconnect {self.device_ip}')

    @staticmethod
    def get_device():
        return os.system(f'adb devices')

    def get_package_3(self):
        return os.system(f'adb -s {self.device_ip} shell pm list packages -3')

    def restart(self):
        return os.system(f'adb -s {self.device_ip} reboot')

    def uninstall(self):
        return os.system(f'adb -s {self.device_ip} uninstall com.htjy.xiaofeiji.hpt')

    def install(self):
        print('安装中...')
        return os.system(f'adb -s {self.device_ip} install -r {self.package_path}')

    def export(self):
        print('导出日志中...')
        os.system(f'adb -s {self.device_ip} logcat -t 1000000 > D:\log.txt')
        os.system('start D:\log.txt')

    def start_app(self, name):
        return os.system(f'adb -s {self.device_ip} shell am start -n com.htjy.xiaofeiji.hpt/com.htjy.xiaofeiji.hpt.MainActivity')

    def get_app_active(self):
        os.system(f'adb -s {self.device_ip} shell dumpsys activity | findstr /i "mFocused"')

    def get_logs(self):
        lines = input("筛选条数(默认10000条):")
        filters = input("筛选条件(默认D级别):")
        if lines:
            print("按查询条件筛选日志...")
            os.system(f'adb -s {self.device_ip} logcat -t {lines}| findstr /i {filters if filters else "D"}')
        else:
            os.system(f'adb -s {self.device_ip} logcat -t 100000 | findstr /i {filters if filters else "D"}')

    def clear_log(self):
        return os.system(f'adb -s {self.device_ip} logcat -c')

    def screenshot(self):
        fpath = r"C:\Users\admin\Desktop\1.png"
        os.system(f'adb -s {self.device_ip} shell screencap -p /sdcard/screen.png')
        os.system(f'adb -s {self.device_ip} pull /sdcard/screen.png {fpath}')
        os.system(f'start {fpath}')

    def video(self):
        vpath = r"C:\Users\admin\Desktop\1.mp4"
        time_limit = input("请输入录屏时间(秒):")
        print("正在录屏中，请稍等...")
        os.system(f'adb -s {self.device_ip} shell screenrecord --time-limit {time_limit} /sdcard/video.mp4')
        os.system(f'adb -s {self.device_ip} pull /sdcard/video.mp4 {vpath}')
        print("录屏完成，正在打开视频文件...")
        os.system(f'start {vpath}')

    def operate(self):
        while 1:
            func = {1:'screenshot', 2:'video', 3:'get_logs', 4:'get_package_3', 5:'install', 6:'uninstall', 7:'exit', 8:'restart', 9:'export', 10:'clear_log'}
            inp = input("1.截图 2.录屏 3.查看日志 4.安装包 5.安装 6.卸载 7.退出 8.重启设备 9.导出日志 10.清空日志\n请输入：")
            try:
                if hasattr(self, func[int(inp)]):
                    getattr(self, func[int(inp)])()
                elif inp == '7':
                    break
                else:
                    continue
            except ValueError:
                continue


if __name__ == '__main__':
    path = r"D:\资料\飞书下载记录\app-HongtuHaiPuTianXiaoFeiJi-debug(4).apk"  # 安装包路径
    # path = r"D:\资料\飞书下载记录\hongtu.apk"  # 安装包路径
    adb = Adb('192.168.83.116', path)
    # adb.connect()
    adb.operate()






