# coding:utf8

from django.conf import settings
import time
import os
from selenium.webdriver.remote.webdriver import WebDriver as Remote
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.ie.webdriver import WebDriver as IE
from selenium.webdriver.chrome.webdriver import WebDriver as Chrome
from selenium.common.exceptions import *
from .WebEle import WebEle
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select


class WebKeywords:

    def __init__(self, log, var_map):
        self.log = log
        self.var_map = var_map
        self.dr = None
        self.ele = None
        self.wait = None

    # @staticmethod
    # def is_string(item):
    #     return isinstance(item, str)
    #
    # def _handle_variables_in_expression(self, expression, namespace):
    #     expr = expression
    #     beg = 0
    #     end = 0
    #     while expr.find('{', beg) != -1:
    #         beg = expr.find('{', beg) + 1
    #         end = expr.find('}', end + 1)
    #         varname = expr[beg: end]
    #         val = self.var_map[varname]
    #         namespace[varname] = val
    #     return namespace
    #
    # def web_eval(self, params):
    #     try:
    #         expression = params[0].strip()
    #         modules = params[1].strip()
    #         var_name = params[2].strip()
    #         namespace = {}
    #         if self.is_string(expression) and '${' in expression:
    #             namespace = self._handle_variables_in_expression(expression, namespace)
    #             expression = expression.replace('${', '').replace('}', '')
    #         if modules:
    #             modules = modules.replace(' ', '').split(',') if modules else []
    #             namespace.update((m, __import__(m)) for m in modules if m)
    #         if not self.is_string(expression):
    #             raise TypeError("Expression must be string")
    #         if not expression:
    #             raise ValueError("Expression cannot be empty.")
    #         val =  eval(expression, namespace)
    #         self.var_map.set_var(var_name, val)
    #         self.log.write('info', 'Evaluate of : | %s = %s |---Success!' % (val, expression))
    #         return True
    #     except Exception as e:
    #         self.log.write('error', 'Evaluate of : | %s |---Fail!' % expression)
    #         self.log.write('error', e.__str__())
    #         self.take_screenshot()
    #         return False

    def take_screenshot(self):
        try:
            stamp = time.mktime(time.localtime()).replace('.0', '')
            base = os.path.join(settings.MEDIA_ROOT, 'screenshots')
            if not os.path.isdir(base):
                os.mkdir(base)
            else:
                for i in range(10):
                    link = stamp + str(i) + '.png'
                    image = os.path.join(base, link)
                    if os.path.isfile(image):
                        link = stamp + str(i+1) + '.png'
                        image = os.path.join(base, link)
                    else:
                        break
            self.dr.get_screenshot_as_file(image)
            self.log.write('info', '<a href="/upload/screenshots/' + link + '">截图</a>')
        except WebDriverException as e:
            self.log.write('error', 'Try to take screenshot fail!')
            self.log.write('error', e.__str__())
            return False
        except Exception as e:
            self.log.write('error', 'Try to take screenshot fail!')
            self.log.write('error', e.__str__())
            return False

    def web_quit(self, params):
        try:
            self.dr.close()
            self.dr.quit()
            self.log.write('info', 'Quit!')
            return True
        except WebDriverException as e:
            self.log.write('info', 'Quit!')
            self.log.write('error', e.__str__())
            return False
        except Exception as e:
            self.log.write('error', e.__str__())
            return False

    def web_ie(self, params):
        try:
            # ip = self.var_map.get_var('ip')
            ip = params[0].strip()
            host = 'http://' + ip + ':4444/wd/hub'
            driver = self.var_map.get_var('driver')
            if not driver:
                self.log.write('error', 'Undefined driver path: web_set_driver ${driver}')
                return False
            if host.find('127.0.0.1') != -1 or ip == '':
                self.dr = IE(executable_path=driver)
            else:
                dc = DesiredCapabilities.INTERNETEXPLORER
                dc['webdriver.ie.driver'] = driver
                self.dr = Remote(command_executor=host, desired_capabilities=dc)
            self.dr.maximize_window()
            self.dr.set_page_load_timeout(30)
            self.dr.implicitly_wait(10)
            self.log.write('info', 'Try to open ie:|' + params[0] + '|---Success!')
            self.ele = WebEle(self.dr, self.log)
            return True
        except WebDriverException as e:
            self.log.write('error', 'Try to open ie:|' + params[0] + '|---Fail!')
            self.log.write('error', e.__str__())
            return False
        except Exception as e:
            self.log.write('error', 'Try to open ie:|' + params[0] + '|---Fail!')
            self.log.write('error', e.__str__())
            return False

    def web_chrome(self, params):
        try:
            # ip = self.var_map.get_var('ip')
            ip = params[0].strip()
            host = 'http://' + ip + ':4444/wd/hub'
            driver = self.var_map.get_var('driver')
            if not driver:
                self.log.write('error', 'Undefined driver path: web_set_driver ${driver}')
                return False
            if host.find('127.0.0.1') != -1 or ip == '':
                self.dr = Chrome(executable_path=driver)
            else:
                dc = DesiredCapabilities.CHROME
                dc['webdriver.chrome.driver'] = driver
                self.dr = Remote(command_executor=host, desired_capabilities=dc)
            self.dr.maximize_window()
            self.dr.set_page_load_timeout(30)
            self.dr.implicitly_wait(10)
            self.log.write('info', 'Try to open chrome:|' + params[0] + '|---Success!')
            self.ele = WebEle(self.dr, self.log)
            return True
        except WebDriverException as e:
            self.log.write('error', 'Try to open chrome:|' + params[0] + '|---Fail!')
            self.log.write('error', e.__str__())
            return False
        except Exception as e:
            self.log.write('error', 'Try to open chrome:|' + params[0] + '|---Fail!')
            self.log.write('error', e.__str__())
            return False

    def web_set_driver(self, params):
        try:
            driver = params[0].strip()
            if driver:
                self.var_map.set_var('driver', driver)
                self.log.write('info', 'Set driver path: ' + params[0])
                return True
            else:
                self.log.write('error', 'Empty driver path: ' + params[0])
                return False
        except Exception as e:
            self.log.write('error', e.__str__())
            return False

    def web_get(self, params):
        try:
            url = params[0].strip()
            if url:
                self.dr.get(url)
                self.log.write('info', 'Try to open : |' + url + '|---Success!')
                return True
            else:
                self.log.write('error', 'Empty url: ' + params[0])
                return False
        except WebDriverException as e:
            self.log.write('error', 'Try to open : |' + url + '|---Fail!')
            self.log.write('error', e.__str__())
            self.take_screenshot()
            return False
        except Exception as e:
            self.log.write('error', 'Try to open : |' + url + '|---Fail!')
            self.log.write('error', e.__str__())
            self.take_screenshot()
            return False

    def web_sleep(self, params):
        try:
            seconds = int(params[0].strip())
            if seconds:
                time.sleep(seconds)
                self.log.write('info', 'Try to sleep : |' + seconds + '|---Success!')
                return True
            else:
                self.log.write('error', 'Empty seconds: ' + params[0])
                return False
        except WebDriverException as e:
            self.log.write('error', 'Try to sleep : |' + seconds + '|---Fail!')
            self.log.write('error', e.__str__())
            self.take_screenshot()
            return False
        except Exception as e:
            self.log.write('error', 'Try to sleep : |' + seconds + '|---Fail!')
            self.log.write('error', e.__str__())
            self.take_screenshot()
            return False

    def web_wait(self, params):
        try:
            locator = params[0].strip()
            seconds = int(params[1].strip())
            element = self.ele.get(locator)
            self.wait = WebDriverWait(self.dr, seconds or 30)
            self.wait.until(element.is_displayed())
            self.log.write('info', 'Try to wait : | %s for %s seconds |---Success!' % (locator, params[1]))
            return True
        except WebDriverException as e:
            self.log.write('error', 'Try to wait : | %s for %s seconds |---Fail!' % (locator, params[1]))
            self.log.write('error', e.__str__())
            self.take_screenshot()
            return False
        except Exception as e:
            self.log.write('error', 'Try to wait : | %s for %s seconds |---Fail!' % (locator, params[1]))
            self.log.write('error', e.__str__())
            self.take_screenshot()
            return False

    def web_click(self, params):
        try:
            locator = params[0].strip()
            element = self.ele.get(locator)
            element.click()
            self.log.write('info', 'Try to click : | %s |---Success!' % locator)
            return True
        except WebDriverException as e:
            self.log.write('error', 'Try to click : | %s |---Fail!' % locator)
            self.log.write('error', e.__str__())
            self.take_screenshot()
            return False
        except Exception as e:
            self.log.write('error', 'Try to click : | %s |---Fail!' % locator)
            self.log.write('error', e.__str__())
            self.take_screenshot()
            return False

    def web_select_by_index(self, params):
        try:
            locator = params[0].strip()
            element = self.ele.get(locator)
            index = int(params[1].strip())
            Select(element).select_by_index(index)
            self.log.write('info', 'Try to select by index: | %s of %s |---Success!' % (params[1], locator))
            return True
        except WebDriverException as e:
            self.log.write('error', 'Try to select by index: | %s of %s |---Fail!' % (params[1], locator))
            self.log.write('error', e.__str__())
            self.take_screenshot()
            return False
        except Exception as e:
            self.log.write('error', 'Try to select by index: | %s of %s |---Fail!' % (params[1], locator))
            self.log.write('error', e.__str__())
            self.take_screenshot()
            return False

    def web_select_by_text(self, params):
        try:
            locator = params[0].strip()
            element = self.ele.get(locator)
            text = params[1].strip()
            Select(element).select_by_visible_text(text)
            self.log.write('info', 'Try to select by text: | %s of %s |---Success!' % (params[1], locator))
            return True
        except WebDriverException as e:
            self.log.write('error', 'Try to select by text: | %s of %s |---Fail!' % (params[1], locator))
            self.log.write('error', e.__str__())
            self.take_screenshot()
            return False
        except Exception as e:
            self.log.write('error', 'Try to select by text: | %s of %s |---Fail!' % (params[1], locator))
            self.log.write('error', e.__str__())
            self.take_screenshot()
            return False

    def web_select_by_value(self, params):
        try:
            locator = params[0].strip()
            element = self.ele.get(locator)
            value = params[1].strip()
            Select(element).deselect_by_value(value)
            self.log.write('info', 'Try to select by value : | %s of %s |---Success!' % (params[1], locator))
            return True
        except WebDriverException as e:
            self.log.write('error', 'Try to select by value: | %s of %s |---Fail!' % (params[1], locator))
            self.log.write('error', e.__str__())
            self.take_screenshot()
            return False
        except Exception as e:
            self.log.write('error', 'Try to select by value : | %s of %s |---Fail!' % (params[1], locator))
            self.log.write('error', e.__str__())
            self.take_screenshot()
            return False

    def web_input(self, params):
        try:
            locator = params[0].strip()
            element = self.ele.get(locator)
            text = params[1].strip()
            element.send_keys(text)
            self.log.write('info', 'Try to input : | %s to %s |---Success!' % (params[1], locator))
            return True
        except WebDriverException as e:
            self.log.write('error', 'Try to input : | %s to %s |---Fail!' % (params[1], locator))
            self.log.write('error', e.__str__())
            self.take_screenshot()
            return False
        except Exception as e:
            self.log.write('error', 'Try to input : | %s to %s |---Fail!' % (params[1], locator))
            self.log.write('error', e.__str__())
            self.take_screenshot()
            return False

    def web_get_text(self, params):
        try:
            locator = params[0].strip()
            text = self.ele.get(locator).text
            var = params[1].strip()
            self.var_map.set_var(var, text)
            self.log.write('info', 'Get text of : | %s : %s |---Success!' % (locator, text))
            return True
        except WebDriverException as e:
            self.log.write('error', 'Get text of : | %s : %s |---Fail!' % (locator, text))
            self.log.write('error', e.__str__())
            self.take_screenshot()
            return False
        except Exception as e:
            self.log.write('error', 'Get text of : | %s : %s |---Fail!' % (locator, text))
            self.log.write('error', e.__str__())
            self.take_screenshot()
            return False

    def web_get_attr(self, params):
        try:
            locator = params[0].strip()
            attribute = params[1].strip()
            attr = self.ele.get(locator).get_attribute(attribute)
            var = params[2].strip()
            self.var_map.set_var(var, attr)
            self.log.write('info', 'Get %s of : | %s : %s |---Success!' % (attribute, locator, attr))
            return True
        except WebDriverException as e:
            self.log.write('error', 'Get %s of : | %s : %s |---Fail!' % (attribute, locator, attr))
            self.log.write('error', e.__str__())
            self.take_screenshot()
            return False
        except Exception as e:
            self.log.write('error', 'Get %s of : | %s : %s |---Fail!' % (attribute, locator, attr))
            self.log.write('error', e.__str__())
            self.take_screenshot()
            return False









