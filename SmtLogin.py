import asyncio
import random
import tkinter
from pyppeteer.launcher import launch
import re
import hashlib
class smtLogin():
    def __init__(self,shop_dict):
        self.shop = shop_dict

    def screen_size(self):
        tk = tkinter.Tk()
        width = tk.winfo_screenwidth()
        height = tk.winfo_screenheight()
        return {'width':width,'height':height}

    async def login(self,username,password):
        self.browser = await launch(
            {
                # 'devtools': True,
                'headless': False,
                'dumpio': True,
                'ignoreDefaultArgs': ['--enable-automation']
            },
            args=['--user-data-dir=./userData'],
        )
        page = await self.browser.newPage()
        try:
            await page.setViewport(viewport=self.screen_size())
            await page.setJavaScriptEnabled(enabled=True)
            await page.setUserAgent(
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'
            )
            await self.page_evaluate(page)

            await page.goto("https://login.aliexpress.com/seller.htm?flag=1&return_url=http%3A%2F%2Fgsp.aliexpress.com%2F")
            await asyncio.sleep(2)
            sub_page = [frame for frame in page.frames if 'login' in frame.name][0]#获取页面上所有的名字中含有login的frame,取第一个
            if sub_page:
                await sub_page.evaluate('document.querySelector("#fm-login-id").value=""')#账号
                await sub_page.type('#fm-login-id',self.shop['userName'],{'delay':self.input_time_random()-10})
                await sub_page.evaluate('document.querySelector("#fm-login-password").value=""')#密码
                await sub_page.type('#fm-login-password', self.shop['passWord'],
                            {'delay': self.input_time_random() - 50})
                await sub_page.waitFor(6000)
                await sub_page.click('#fm-login-submit')#提交
                await sub_page.waitFor(6000)
            await asyncio.sleep(2)
            await page.goto("https://gsp.aliexpress.com/apps/order/index")
            await page.waitFor(6000)
            order_cookie = await self.get_cookie(page)#取得cookie
        except:
            return {'code':-1,'msg':'error'}
        finally:
            await page.waitFor(3000)
            await self.page_close(self.browser)

    async def get_cookie(self,page):
        cookie_list = await page.cookies()
        # print(cookie_list)
        cookies = ''
        for cookie in cookie_list:
            str_cookie = '{0}={1};'
            str_cookie = str_cookie.format(cookie.get('name'),cookie.get('value'))
            cookies += str_cookie
        # print(cookies)
        return cookies

    def input_time_random(self):
        return random.randint(100, 151)

    def get_token(self,cookies):
        token = re.findall("_m_h5_tk=(.*?)_", cookies)[0]
        return token


    def get_sign(self, t,sellerid,data):#js断点，解析出sign的规律

        token = ''
        datas = token + '&' + t + '&' + sellerid + '&' + data
        sign = hashlib.md5()
        sign.update(datas.encode("utf8"))
        signs = sign.hexdigest()
        return signs

    async def page_close(self, browser):
        for _page in await browser.pages():
            await _page.close()
        await browser.close()

    async def page_evaluate(self,page):
        await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => undefined } }) }''')
        await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
        await page.evaluate(
            '''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
        await page.evaluate(
            '''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')
        await page.waitFor(3000)

    def run(self):
        loop = asyncio.get_event_loop()
        i_futrue = asyncio.ensure_future(self.login(self.shop['userName'],self.shop['passWord']))
        loop.run_until_complete(i_futrue)
        return i_futrue.result()

if __name__=="__main__":
    user = {'userName':'yourname','passWord':'yourpassword'}
    smtLogin(user)

