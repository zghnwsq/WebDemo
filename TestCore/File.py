# coding:utf8


class File:

    @staticmethod
    def file_write(path, msg, mode):
        file = open(path, mode=mode)
        file.write(msg)
        file.close()
