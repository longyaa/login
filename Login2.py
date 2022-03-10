from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys


class WebDriverChrome(object):
    def __init__(self, userid):
        self.driver = self.StartWebdriver(userid)

    def StartWebdriver(self, userid):
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximzed")
        path = "D:\download\smt\{}".format(userid)
        prefs = {"downlaod.default_directory": "{}".format(path), "download.prompt_for_download": False, }
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        driver = webdriver.Chrome(options=options)

        driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': "{}".format(path)}}
        command_result = driver.execute("send_command", params)

        with open('./stealth.min.js') as f:
            js = f.read()

        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": js
        })
        return driver

    def RunStart(self, f1, f2):
        # self.driver.set_window_position(0,-2000)
        self.driver.get(
            'https://login.aliexpress.com/seller.htm?flag=1&return_url=http%3A%2F%2Fgsp.aliexpress.com%2F')
        self.driver.implicitly_wait(10)
        self.driver.switch_to.frame('alibaba-login-box')
        self.driver.find_element_by_xpath('//*[@id="fm-login-id"]').send_keys(f1)
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="fm-login-password"]').send_keys(f2)
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="fm-login-submit"]').send_keys(Keys.ENTER)

        try:
            self.driver.find_element_by_xpath(
                '//*[@id="WTTAG-1413"]/div/div[1]/div[1]/div/span[1]').click()  # 关掉弹窗,弹窗不一定会有
        except Exception as e:
            print(e)
        time.sleep(4)
        self.driver.get('https://gsp.aliexpress.com/apps/order/index')
        self.driver.implicitly_wait(4)
        cookie_list = self.driver.get_cookies()
        print(cookie_list)
        self.driver.close()
        self.driver.quit()


if __name__ == '__main__':
    i={'userId':'123','userName':'yourname','passWord':'pwd'}
    Crawl = WebDriverChrome(i['userId'])
    Crawl.RunStart(f1=i['userName'], f2=i['passWord'])

    print("下载完成")
