from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup as bs

import os
import time
from datetime import datetime, timedelta
import calendar

from exception import selfException

class crawling:

    def __init__(self, url, page):

        self.url = url
        # self.category = page
        # self.driver = ''


    def set_driver(self, headless=None):

        for count in range(3,0,-1):
            
            driver = None
            
            try:

                # if profile == True:
                #     profile = webdriver.c
                #     profile.set_preference("general.useragent.override", "[user-agent string]")
                
                caps = webdriver.DesiredCapabilities().CHROME
                caps["marionette"] = True

                #옵션 설정
                prefs = {'profile.default_content_setting_values': \
                            {
                            # 'cookies' : 2, 
                            'images': 2, 
                            'plugins' : 2, 
                            'popups': 2, 
                            'geolocation': 2, 
                            'notifications' : 2, 
                            'auto_select_certificate': 2, 
                            'fullscreen' : 2, 
                            'mouselock' : 2, 
                            'mixed_script': 2, 
                            'media_stream' : 2, 
                            'media_stream_mic' : 2, 
                            'media_stream_camera': 2, 
                            'protocol_handlers' : 2, 
                            'ppapi_broker' : 2, 
                            'automatic_downloads': 2, 
                            'midi_sysex' : 2, 
                            'push_messaging' : 2, 
                            'ssl_cert_decisions': 2, 
                            'metro_switch_to_desktop' : 2, 
                            'protected_media_identifier': 2, 
                            'app_banner': 2, 
                            'site_engagement' : 2, 
                            'durable_storage' : 2
                            # 'javascript' : 2
                            }
                        }

                setOptions = Options()
                
                if headless == True:
                    setOptions.add_argument('--headless')
                
                setOptions.add_argument('--no-sandbox')
                setOptions.add_experimental_option('prefs', prefs)
                setOptions.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko")
                setOptions.add_argument("lang=ko_KR")  # 한국어!

                driver = webdriver.Chrome(executable_path=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'chromedriver.exe'), options=setOptions)

                # driver = Firefox(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'geckodriver.exe'), firefox_options=setOptions)
                # driver = Chrome(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'chromedriver.exe'), chrome_options=setOptions)

                # driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5]}})")
                # driver.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")
                # driver.execute_script("const getParameter = WebGLRenderingContext.getParameter;WebGLRenderingContext.prototype.getParameter = function(parameter) {if (parameter === 37445) {return 'NVIDIA Corporation'} if (parameter === 37446) {return 'NVIDIA GeForce GTX 980 Ti OpenGL Engine';}return getParameter(parameter);};")

                #드라이버 반환
                driver.get(self.url)
                return driver
                break
                # self.driver.implicitly_wait(20)

            except (Exception, KeyboardInterrupt, selfException):

                if count == 0:

                    raise selfException
                
                else:

                    del driver
                    continue

    def input_driver(self, driver, value, category=None, xpath=None, class_=None, id=None, css_selector=None, link_text=None):

        try:

            if link_text!=None:

                by_attribute = By.LINK_TEXT
                attribute = link_text

            elif class_!=None:

                by_attribute = By.CLASS_NAME
                attribute = class_

            elif xpath!=None:

                by_attribute = By.XPATH
                attribute = xpath    

            elif id!=None:

                by_attribute = By.ID
                attribute = id
            
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((by_attribute, attribute))).clear()
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((by_attribute, attribute))).send_keys(value)
        
        except (KeyboardInterrupt, Exception):

            raise selfException

    def submit_driver(self, driver, category=None, xpath=None, class_=None, id=None, css_selector=None, link_text=None):

        try:

            if link_text!=None:

                by_attribute = By.LINK_TEXT
                attribute = link_text

            elif class_!=None:

                by_attribute = By.CLASS_NAME
                attribute = class_

            elif xpath!=None:

                by_attribute = By.XPATH
                attribute = xpath    

            elif id!=None:

                by_attribute = By.ID
                attribute = id
            
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((by_attribute, attribute))).submit()
        
        except (KeyboardInterrupt, Exception):

            raise selfException

    def click_driver(self, driver, xpath=None, class_=None, id=None, css_selector=None, link_text=None):

        try:

            if link_text!=None:

                by_attribute = By.LINK_TEXT
                attribute = link_text

            elif class_!=None:

                by_attribute = By.CLASS_NAME
                attribute = class_

            elif xpath!=None:

                by_attribute = By.XPATH
                attribute = xpath

            elif id!=None:

                by_attribute = By.ID
                attribute = id

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((by_attribute, attribute))).click()

        except (KeyboardInterrupt, Exception):

            raise selfException

    def script_driver(self, driver, script, xpath=None, class_=None, id=None, css_selector=None, link_text=None):

        try:

            if class_!=None:

                by_attribute = By.CLASS_NAME
                attribute = class_

            elif xpath!=None:

                by_attribute = By.XPATH
                attribute = xpath        

            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((by_attribute, attribute)))
            driver.execute_script(script, element)

        except (KeyboardInterrupt, Exception):

            raise selfException


class path:

    def __init__(self, workDir=None):

        if workDir!=None:

            self.workDir = os.path.join(os.getcwd(), workDir)
        
        else:

            self.workDir = os.getcwd()
    
    def setWorkDir(self, path_list=None):

        setDir = self.workDir

        if path_list!=None:

            for path in path_list:

                setDir = os.path.join(setDir, path)
            
            self.workDir = setDir
        
        if os.path.isdir(setDir):

            self.workDir = setDir

        else:

            os.makedirs(setDir)
            self.workDir = setDir

    def getWorkDir(self):

        return self.workDir



# class parser:

#     def __init__(self, html_source):

#         self.source_soup = bs(html_source, 'html.parser')
    
#     def get_source_soup(self):

#         return self.source_soup