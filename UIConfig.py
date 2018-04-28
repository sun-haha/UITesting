#!/usr/bin/env python3
# coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import logging
logger = logging.getLogger("UIConfig")

class NotInDesiredPageError(Exception):
    pass

class Page(object):
    '''
    基础类，用于页面对象类的继承
    '''
    defaultURL = "http://192.168.1.1"
    def __init__(self,driver,url=defaultURL, userName='admin', passwd='admin'):
        self.baseURL = url
        self.driver = driver
        self.userName = userName
        self.passwd = passwd
        self.driver.implicitly_wait(10)
        self.timeout = 30

    def is_on_page(self,kywords):
        '''
        check if current page is the desired page
        :param kywords: the keywords of the desired page url
        :return: True or False
        '''

        return (kywords in self.driver.current_url)

    def openPage(self, url = '/'):
        url = self.baseURL + url
        self.driver.get(url)

    def findElement(self, *location):
        return self.driver.find_element(*location)

    def inputValue(self,element,value):
        '''
        input values to textbox
        :param element: a WebElement
        :param value: the desired value of the WebElement
        :return: None
        '''

        element.clear()
        element.send_keys(value)



class UIConfig(Page):
    '''Configure router via UI, we try to set router parameters via UI, not via JNAP call just like end-users'''


    def login(self,*kywords):
        """
        kywords[0] should be 'click here' link text
        kywords[1] should be password id
        kywords[2] should be 'Sign in' id
         """
        try:
            self.openPage()
            clickhereLoc = self.findElement(By.LINK_TEXT,kywords[0])
            clickhereLoc.click()
            sleep(6)

            passwdLoc = self.findElement(By.ID,kywords[1])
            self.driver.execute_script('arguments[0].scrollIntoView(true)',passwdLoc)
            self.inputValue(passwdLoc,self.passwd)
            loginLoc = self.findElement(By.ID,kywords[2])
            loginLoc.click()
            sleep(10)

            if not (self.is_on_page("home.html")):
                raise NotInDesiredPageError("Login using password admin failed")


        except Exception as e:
            logger.debug("An exception is raised: {0}".format(e))
            raise NotInDesiredPageError(str(e))

        return True

    def setWiFiName(self, wifiName, wifiPasswd="12345678", wifisettingsame=True,**keyargs):
        '''
                keyargs["findWifiXPath"] should be xpath of Wi-Fi Settings://*[@id="68980747-C5AA-4C8B-AF53-FC1023DE2567"]/ul/li[3]
                keyargs["findwifiName"] should be the name of wifi name textbox
                keyargs["findwifiPasswd"] should be the name of wifi password

                Please be noted:
                This case will focus on changing wifi name, so we keep the security mode to WPA2 which is the default status after factory reset
                and the wifi password, we set it to '12345678'
        '''
        findWifiXPath = ""
        find24SSIDXPath = ""
        find24PasswdXPath = ""
        find5SSIDXPath = ""
        find5PasswdXPath = ""
        findOKId = ""
        findShowmoreId = ""
        findYesXPath = ""
        try:
            for key in keyargs:
                if key == "findWifiXPath":
                    findWifiXPath = keyargs[key]
                    continue
                if key == "find24SSIDXPath":
                    find24SSIDXPath = keyargs[key]
                    continue
                if key == "find24PasswdXPath":
                    find24PasswdXPath = keyargs[key]
                    continue
                if key == "find5SSIDXPath":
                    find5SSIDXPath = keyargs[key]
                    continue
                if key == "find5PasswdXPath":
                    find5PasswdXPath = keyargs[key]
                    continue
                if key == "findOKId":
                    findOKId = keyargs[key]
                    continue
                if key == "findShowmoreId":
                    findShowmoreId = keyargs[key]
                    continue
                if key == 'findYesXPath':
                    findYesXPath = keyargs[key]
                    continue

            self.findElement(By.XPATH,findWifiXPath).click()        #go to wi-fi settings page
            sleep(10)

            _24wifiNameTextbox = self.findElement(By.XPATH,find24SSIDXPath)
            _24wifiPasswdTextbox = self.findElement(By.XPATH,find24PasswdXPath)
            OKButton = self.findElement(By.ID,findOKId)
            if wifisettingsame:
                self.inputValue(_24wifiNameTextbox,wifiName)
                self.inputValue(_24wifiPasswdTextbox,wifiPasswd)
                OKButton.click()
                sleep(10)
            else:
                # click "show more"
                self.findElement(By.ID,findShowmoreId).click()
                sleep(2)

                _5wifiNameTextbox = self.findElement(By.XPATH,find5SSIDXPath)
                _5wifiPasswdTextbox = self.findElement(By.XPATH,find5PasswdXPath)

                self.inputValue(_24wifiNameTextbox, wifiName)
                self.inputValue(_24wifiPasswdTextbox, wifiPasswd)
                self.inputValue(_5wifiNameTextbox,wifiName + "5")
                self.inputValue(_5wifiPasswdTextbox,wifiPasswd)
                OKButton.click()
                sleep(10)

            # click "yes" to save settings
            element = self.findElement(By.XPATH,findYesXPath)
            element.click()
            sleep(10)
        except Exception as e:
            logger.debug("An exception is raised: {0}".format(e))
            print (str(e))
            return False

        return True

    def logout(self):
        self.driver.close()


if __name__ == '__main__':
    try:
        driver = webdriver.Firefox()
        UIObject = UIConfig(driver)
        UIObject.login("Click here","adminPass","submit-login")
        wifiDic = { \
        'findWifiXPath': r'//*[@id="68980747-C5AA-4C8B-AF53-FC1023DE2567"]/ul/li[3]', \
        'find24SSIDXPath': r'//*[@id="RADIO_2.4GHz"]/div/h3/input', \
        'find24PasswdXPath': r'//*[@id="RADIO_2.4GHz"]/div/input[1]', \
        'find5SSIDXPath': r'//*[@id="RADIO_5GHz"]/div/h3/input', \
        'find5PasswdXPath': r'//*[@id="RADIO_5GHz"]/div/input[1]', \
        'findOKId': 'submitWirelessButton', \
        'findShowmoreId': r'show-more' ,\
        'findYesXPath':r'//*[@id="radio-disconnect-warning"]/div[3]/button[2]' \
        }
        UIObject.setWiFiName('hello', **wifiDic)

    finally:
        driver.close()












