# coding:utf8

# from selenium.webdriver.remote.webelement import WebElement
# from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import *


class WebEle:

    def __init__(self, dr, log):
        self.dr = dr
        self.log = log

    def get(self, locator):
        prefix = 'find_element_by_'
        method = prefix + locator.split('=')[0]
        if locator.find('=') == -1 and locator != '':
            self.log.write('error', 'Invalid locator:' + locator)
            raise Exception('Invalid locator:' + locator)
            return None
        loc = locator.split('=')[1]
        if hasattr(self.dr, method):
            try:
                func = getattr(self.dr, method)
                ele = func(loc)
                return ele
            except NoSuchElementException as e:
                self.log.write('error', 'No such element:' + locator)
                self.log.write('error', e.__str__())
                return None
            except Exception as e:
                self.log.write('error', e.__str__())
                return None
        else:
            self.log.write('error', 'No such method:' + method)
            return None

    def get_elements(self, locator):
        prefix = 'find_elements_by_'
        method = prefix + locator.split('=')[0]
        loc = locator.split('=')[1]
        if hasattr(self.dr, method):
            try:
                func = getattr(self.dr, method)
                ele = func(loc)
                return ele
            except NoSuchElementException as e:
                self.log.write('error', 'No such elements:' + locator)
                self.log.write('error', e.__str__())
                return None
            except Exception as e:
                self.log.write('error', e.__str__())
                return None
        else:
            self.log.write('error', 'No such method:' + method)
            return None




