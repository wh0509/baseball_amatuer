from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup as BS

import os
import time
from datetime import datetime, timedelta
import calendar
import pandas as pd

class selfException(Exception):    # Exception을 상속받아서 새로운 예외를 만듦
    def __init__(self):
        super().__init__('강제종료')

### 드라이버 생성

def set_driver(category=None, profile=None):

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
        # setOptions.add_argument('--headless')
        setOptions.add_argument('--no-sandbox')
        setOptions.add_experimental_option('prefs', prefs)
        setOptions.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko")
        setOptions.add_argument("lang=ko_KR")  # 한국어!

        driver = webdriver.Chrome(executable_path=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'chromedriver.exe'), chrome_options=setOptions)

        # driver = Firefox(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'geckodriver.exe'), firefox_options=setOptions)
        # driver = Chrome(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'chromedriver.exe'), chrome_options=setOptions)

        # driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5]}})")
        # driver.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")
        # driver.execute_script("const getParameter = WebGLRenderingContext.getParameter;WebGLRenderingContext.prototype.getParameter = function(parameter) {if (parameter === 37445) {return 'NVIDIA Corporation'} if (parameter === 37446) {return 'NVIDIA GeForce GTX 980 Ti OpenGL Engine';}return getParameter(parameter);};")

        #드라이버 반환
        return driver
    
    except (Exception, KeyboardInterrupt):

        raise selfException

def submit_driver(driver, category=None, xpath=None, class_=None, id=None, css_selector=None, link_text=None):

    pass

def click_driver(driver, category=None, xpath=None, class_=None, id=None, css_selector=None, link_text=None):

    if category == "rapsodo":

        if link_text!=None:

            by_attribute = By.LINK_TEXT
            attribute = link_text
        
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((by_attribute, attribute))).click()
        driver.implicitly_wait(60)

def date_driver(driver, date, category=None, xpath=None, class_=None, id=None, css_selector=None, link_text=None):
    
    date_format = "{} - {}".format(date, date)

    if category == "rapsodo":

        if class_!=None:

            by_attribute = By.CLASS_NAME
            attribute = class_
        
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((by_attribute, attribute))).sendKeys(date_format)
        driver.implicitly_wait(60)

# ### 클래스 생성(Coming Soon)

# class rapsodo_driver(self):

#     def __init__(self):

#     def click(self):

def main():
    
    driver = set_driver()
    driver.get("https://cloud.rapsodo.com/#/auth/login")
    driver.implicitly_wait(180)

    driver.find_element_by_id("username").send_keys('tomtango@lotte.net')
    driver.find_element_by_id("password").send_keys('Giantsv3!23$56')

    driver.find_element_by_id("login-button-text").click()
    driver.implicitly_wait(180)

    # player_df = pd.read_excel("idmap_update_210208.xlsx")
    # player_lotte_df = player_df[player_df["epit_team"]=="Lotte"]

    player_lotte_list = ["스트레일리_58"]

    # for index in player_lotte_df.index:

    #     player_name = player_lotte_df.at[index, "kpitname"]
    #     player_back = player_lotte_df.at[index, "kpitback"]

    #     player_select_button = "{}_{}".format(player_name, player_back)
    #     player_lotte_list.append(player_select_button)

    for index, name in enumerate(player_lotte_list):

        today = datetime.today()
        today_str = today.strptime("mm/dd/yyyy")

        today_day = today.day
        today_month = calendar.month_abbr[today.month]
        today_year = today.year

        link_text = "{} {}, {}".format(today_month, today_day, today_year)
        
        if index == 0:

            driver.find_element_by_link_text(name).click()
            driver.implicitly_wait(180)

            date_driver(driver, today_str, category="rapsodo", class_="daterangepicker-input ng-valid ng-dirty ng-touched")
            click_driver(driver, category="rapsodo", link_text=link_text)


if __name__ == "__main__":

    main()