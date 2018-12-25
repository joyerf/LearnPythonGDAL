#!/usr/bin/python
# coding: utf-8

import logging
import logging.handlers
import os

LOG_FILE = "testlog.log"
# %(levelno)s:         打印日志级别的数值
# %(levelname)s:    打印日志级别名称
# %(pathname)s:    打印当前执行程序的路径，其实就是sys.argv[0]
# %(filename)s:      打印当前执行程序名
# %(funcName)s:    打印日志的当前函数
# %(lineno)d:         打印日志的当前行号
# %(asctime)s:      打印日志的时间
# %(thread)d:        打印线程ID
# %(threadName)s: 打印线程名称
# %(process)d:      打印进程ID
# %(message)s:    打印日志信息
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)s %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"


class MyLog(object):
    __slots__ = ('__logger', 'debug', 'info', 'warning', 'error', 'critical')

    def __init__(self):
        os.chdir(r'D:\GitHub\SHP&CAD')
        self.__logger = logging.getLogger()
        self.__logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
        # 创建一个handler，用于写入日志文件
        rht = logging.handlers.TimedRotatingFileHandler(LOG_FILE, 'D')
        rht.setFormatter(fmt)
        self.__logger.addHandler(rht)
        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setFormatter(fmt)
        self.__logger.addHandler(ch)
        self.debug = self.__logger.debug
        self.info = self.__logger.info
        self.warning = self.__logger.warning
        self.error = self.__logger.error
        self.critical = self.__logger.critical


__log = MyLog()
debug = __log.debug
info = __log.info
warning = __log.warning
error = __log.error
critical = __log.critical
