'''
Code description: 封装公共方法
Create time: 2020/12/14
Developer: 叶修
'''

import os
import time
import getpathinfo
from common.log import Log
from selenium import webdriver
from common.driver import WDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from  selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchFrameException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import TimeoutException

class LocatorTypeError(Exception):
    pass
class ElementNotFound(Exception):
    pass

class Base(object):
    '''基于原生selenium二次封装'''
    log = Log()

    def __init__(self,open_browser,timeout = 10,t = 0.5):
        url = "http://106.53.210.165:8989/mobiledevice/login/"
        self.base_url = url
        self.driver = open_browser
        self.timeout = timeout
        self.t = t

    def find(self, locator):
        """定位到元素，返回元素对象，没定位到，Timeout异常"""
        if not isinstance(locator, tuple):
            raise LocatorTypeError(self.log.info("参数类型错误，locator必须是元祖类型：loc = ('id','value1')"))
        else:
            self.log.info("正在定位元素信息：定位方式->%s,value值->%s" % (locator[0], locator[1]))
            #print("正在定位元素信息：定位方式->%s,value值->%s" % (locator[0], locator[1]))
            try:
                ele = WebDriverWait(self.driver, self.timeout, self.t).until(EC.presence_of_element_located(locator))
            except TimeoutException as msg:
                 self.log.info('定位元素出现超时！')
                 raise msg
            return ele

    def finds(self,locator):
        '''复数定位，返回elements对象 list'''
        if not isinstance(locator,tuple):
            raise LocatorTypeError(self.log.info('参数类型错误，locator必须是元组类型：loc = ("id","value")'))
        else:
            self.log.info("正在定位元素信息：定位方式->%s,value值->%s" % (locator[0], locator[1]))
            #print("正在定位元素信息：定位方式->%s,value值->%s"%(locator[0],locator[1]))
            try:
                eles = WebDriverWait(self.driver, self.timeout, self.t).until(EC.presence_of_all_elements_located(locator))
            except TimeoutException as msg:
                self.log.info('定位元素出现超时！')
                raise msg
            return eles

    def input(self,locator,text = ""):
        '''写入文本'''
        ele = self.find(locator)
        if ele.is_displayed():
            ele.send_keys(text)
        else:
            raise ElementNotVisibleException(self.log.info("元素不可见或者不唯一无法输入"))

    def click(self,locator):
        '''点击元素'''
        ele = self.find(locator)
        if ele.is_displayed():
            ele.click()
        else:
            raise ElementNotVisibleException(self.log.info("元素不可见或者不唯一无法点击"))

    def clear(self,locator):
        '''清空输入框文本'''
        ele = self.find(locator)
        if ele.is_displayed():
            ele.clear()
        else:
            raise ElementNotVisibleException(self.log.info("元素不可见或者不唯一"))

    def is_selected(self,locator):
        '''判断元素是否被选中，返回bool值'''
        ele  = self.find(locator)
        r = ele.is_selected()
        return r

    def is_element_exist(self,locator):
        '''是否找到'''
        try:
            self.find(locator)
            return True
        except :
            return False

    def is_title(self,title = ""):
        '''返回bool值'''
        try:
            result = WebDriverWait(self.driver,self.timeout,self.t).until(EC.title_is(title))
            return result
        except :
            return False

    def is_title_contains(self, title=''):
        """返回bool值"""
        try:
            result = WebDriverWait(self.driver, self.timeout, self.t).until(EC.title_contains(title))
            return result
        except:
            return False

    def is_text_in_element(self,locator,text = ''):
        '''返回bool值'''
        if not isinstance(locator,tuple):
            raise LocatorTypeError(self.log.info("参数类型错误，locator必须是元祖类型：loc = ('id','value1')"))
        try:
            result = WebDriverWait(self.driver, self.timeout, self.t).until(
                EC.text_to_be_present_in_element(locator, text))
            return result
        except :
            return False

    def is_value_in_element(self,locator,value = ""):
        if not isinstance(locator, tuple):
            raise LocatorTypeError(self.log.info("参数类型错误，locator必须是元祖类型：loc = ('id','value1')"))
        try:
            result = WebDriverWait(self.driver, self.timeout, self.t).until(
                EC.text_to_be_present_in_element_value(locator, value))
            return result
        except:
            return False

    def is_alert(self,timeout = 8):
        try:
            result = WebDriverWait(self.driver, timeout, self.t).until(EC.alert_is_present())
            return result
        except:
            return False

    def get_title(self):
        """获取title"""
        return self.driver.title

    def get_text(self, locator):
        """获取文本"""
        if not isinstance(locator, tuple):
            raise LocatorTypeError(self.log.info("参数类型错误，locator必须是元祖类型：loc = ('id','value1')"))
        try:
            t = self.find(locator).text
            return t
        except:
            self.log.info("获取text失败，返回''")
            #print("获取text失败，返回''")
            return ""

    def get_attribute(self, locator, name):
        """获取属性"""
        if not isinstance(locator, tuple):
            raise LocatorTypeError(self.log.info("参数类型错误，locator必须是元祖类型：loc = ('id','value1')"))
        try:
            element = self.find(locator)
            return element.get_attribute(name)
        except:
            self.log.info("获取%s属性失败，返回''" % name)
            #print("获取%s属性失败，返回''" % name)
            return ''

    def js_focus_element(self,locator):
        '''聚焦元素'''
        if not isinstance(locator,tuple):
            raise LocatorTypeError(self.log.info("参数类型错误"))
        target = self.find(locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", target)

    def js_scroll_top(self):
        '''滚到顶部'''
        js = "window.scrollTo(0,0)"
        self.driver.execute_script(js)

    def js_scroll_end(self,x = 0):
        '''滚到底部'''
        js = "window.scrollTo(%s, document.body.scrollHeight)" % x
        self.driver.execute_script(js)
       
    def jScript(self,src):
        '''执行js脚本'''
        try:
            self.driver.execute_script(src)
        except Exception as e:
            self.log.info('执行js脚本[%s]失败' %src)
            raise e
        else:
            self.log.info('执行js脚本[%s]成功' %src)

    def select_by_index(self,locator,index =0):
        '''通过索引，index是索引第几个，从0开始，默认第一个'''
        if not isinstance(locator,tuple):
            raise LocatorTypeError(self.log.info("参数类型错误"))
        element = self.find(locator)
        Select(element).select_by_index(index)

    def select_by_value(self, locator, value):
        """通过value属性"""
        if not isinstance(locator, tuple):
            raise LocatorTypeError(self.log.info("参数类型错误"))
        element = self.find(locator)
        Select(element).select_by_value(value)

    def select_by_text(self,locator,text):
        """通过文本值定位"""
        element = self.find(locator)
        Select(element).select_by_visible_text(text)

    def switch_iframe(self, id_index_locator):
        """切换iframe"""
        try:
            if isinstance(id_index_locator, int):
                self.driver.switch_to.frame(id_index_locator)
            elif isinstance(id_index_locator, str):
                self.driver.switch_to.frame(id_index_locator)
            elif isinstance(id_index_locator, tuple):
                ele = self.find(id_index_locator)
                self.driver.switch_to.frame(ele)
        except:
            self.log.info("iframe切换异常")
            #print("iframe切换异常")

    def switch_handle(self,window_name):
        self.driver.switch_to.window(window_name)

    def switch_alert(self):
        r = self.is_alert()
        if not r:
            self.log.info("alert不存在")
            #print("alert不存在")
        else:
            return r

    def move_to_element(self, locator):
        """鼠标悬停操作"""
        if not isinstance(locator, tuple):
            raise LocatorTypeError(self.log.info("参数类型错误"))
        ele = self.find(locator)
        ActionChains(self.driver).move_to_element(ele).perform()

if __name__ == '__main__':
    driver = Base().chromeDriver
    web = Base(driver)
    driver.get("https://www.baidu.com")
    loc_1 = ("id","kw")
    web.input(loc_1, "hello")
    time.sleep(5)
    driver.quit()










