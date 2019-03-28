# coding:utf8

import os

class File:

    @staticmethod
    def file_write(path, msg, mode):
        file = open(path, mode=mode, encoding='utf-8')
        file.write(msg)
        file.close()

    @staticmethod
    def file_read(path):
        file = open(path, mode='r', encoding='utf-8')
        text = file.read()
        return text

    @staticmethod
    def file_rename(path, new_path):
        if os.access(path, os.F_OK):
            os.rename(path, new_path)
