'''
Code description: 添加日志
Create time: 2020/12/14
Developer: 李万洋
'''

import logging,time
import os
import getpathinfo

path = getpathinfo.get_path()#获取本地路径
log_path = os.path.join(path,'logs')# log_path是存放日志的路径
# 如果不存在这个logs文件夹，就自动创建一个
if not os.path.exists(log_path):os.mkdir(log_path)

class Log():
    def __init__(self):
        #文件的命名
        self.logname = os.path.join(log_path,'%s.log'%time.strftime('%Y_%m_%d'))
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        #日志输出格式
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def __console(self,level,message):
        #创建一个fileHander，用于写入本地
        fh = logging.FileHandler(self.logname,'a',encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

        #创建一个StreamHandler,用于输入到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        #避免日志重复
        self.logger.removeHandler(fh)
        self.logger.removeHandler(ch)
        #关闭打开文件
        fh.close()

    def debug(self,message):
        self.__console('debug',message)

    def info(self,message):
        self.__console('info',message)

    def warning(self,message):
        self.__console('warning',message)

    def error(self,message):
        self.__console('error',message)

if __name__ == '__main__':
    log = Log()
    log.info('测试')
    log.debug('测试')
    log.warning('测试')
    log.error('测试')
