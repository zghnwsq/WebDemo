# coding=utf-8
import logging


class Log:
    def __init__(self, logfile, level="info"):
        self.logfile = logfile
        self.level = level
        # self.msg = msg
        # 初始化
        self.logger = logging.getLogger()

        # 设定级别
        if self.level == "debug":
            self.logger.setLevel(logging.DEBUG)
        elif self.level == "info":
            self.logger.setLevel(logging.INFO)
        elif self.level == "warning":
            self.logger.setLevel(logging.WARNING)
        elif self.level == "error":
            self.logger.setLevel(logging.ERROR)
        elif self.level == "critical":
            self.logger.setLevel(logging.CRITICAL)
        # 第二步，创建handler，用于写入日志文件
        self.handler = logging.FileHandler(self.logfile, mode='a')
        if self.level == "debug":
            self.handler.setLevel(logging.DEBUG)
        elif self.level == "info":
            self.handler.setLevel(logging.INFO)
        elif self.level == "warning":
            self.handler.setLevel(logging.WARNING)
        elif self.level == "error":
            self.handler.setLevel(logging.ERROR)
        elif self.level == "critical":
            self.handler.setLevel(logging.CRITICAL)
        # 第四步，定义handler的输出格式
        self.formatter = logging.Formatter(' %(asctime)s - %(levelname)s: %(message)s',
                                      datefmt='%a, %d %b %Y %H:%M:%S')
        self.handler.setFormatter(self.formatter)
        # 第五步，将logger添加到handler里面
        self.logger.addHandler(self.handler)

    def write(self, msg, level):
        # 写入日志
        if level == "debug":
            self.logger.debug(msg)
        elif level == "info":
            self.logger.info(msg)
        elif level == "warning":
            self.logger.warning(msg)
        elif level == "error":
            self.logger.error(msg)
        elif level == "critical":
            self.logger.critical(msg)
