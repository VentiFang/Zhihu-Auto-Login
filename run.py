from requests_html import HTMLSession
import base64
from PIL import Image
import hmac
from hashlib import sha1
import time
from urllib.parse import urlencode

import execjs



class Spider():
    def __init__(self):
        self.session = HTMLSession()
        self.login_page_url = 'https://www.zhihu.com/signin?next=%2F'
        self.captcha_api = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=en'
        self.login_api = 'https://www.zhihu.com/api/v3/oauth/sign_in'
        self.headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        }

        self.captcha = ''
        self.signature = ''

    def get_first_cookie(self):
        self.session.get(url=self.login_page_url,headers=self.headers)

    def deal_captcha(self):
        r = self.session.get(url=self.captcha_api,headers=self.headers)
        res = r.json()
        if res.get('show_captcha'):
            while True:
                r = self.session.put(url=self.captcha_api, headers=self.headers)
                res = r.json()
                img_base64 = res.get('img_base64')
                with open('captcha.png','wb') as f:
                    f.write(base64.b64decode(img_base64))
                img_obj = Image.open('captcha.png')
                img_obj.show()
                print(66666666666)
                self.captcha = input("输入验证码：")
                r = self.session.post(url=self.captcha_api, headers=self.headers,data={'input_text':self.captcha})
                res = r.json()
                if res.get('success'):
                    print("验证码输入正确")
                    # break
                    return

    def get_signature(self):
        a = hmac.new(b'd1b964811afb40118a12068ff74a12f4',digestmod=sha1)
        a.update(b'password')
        a.update(b'c3cef7c66a1843f8b3a9e6a1e3160e20')
        a.update(b'com.zhihu.web')
        a.update(str(int(time.time()*1000)).encode('utf-8'))
        self.signature = a.hexdigest()

    def sign_in(self):

        '''
        "username=%2B8618896530856&password=fdsfsdfsd&captcha=&lang=cn&utm_source=&ref_source=other_https%3A%2F%2Fwww.zhihu.com%2Fsignin%3Fnext%3D%252F"

        :return:
        '''
        data = {
            'client_id':'c3cef7c66a1843f8b3a9e6a1e3160e20',
            'grant_type':'password',
            'timestamp':str(int(time.time()*1000)),
            'source':'com.zhihu.web',
            'signature':self.signature,
            'username':'+86xxxxx',
            'password':'xxxxx',
            'captcha':self.captcha,
            'lang':'en',
            'utm_source':'',
            'ref_source':'https://www.zhihu.com/signin?next=%2F'
        }

        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
            'x-zse-83':'3_2.0',
            'content-type':'application/x-www-form-urlencoded',
        }

        with open('知乎加密.js','rt',encoding='utf-8') as f:
            # 指定目录下安装 >npm install jsdom
            js = execjs.compile(f.read(),cwd='../../node_modules')

        data = js.call('b',urlencode(data))
        r = self.session.post(url=self.login_api,headers=headers,data=data)
        if r.status_code == 201:
            print("登陆成功")
            r = self.session.get(url='https://www.zhihu.com',headers=self.headers)
            print(r.text)


    def run(self):

        self.get_first_cookie()
        self.deal_captcha()
        self.get_signature()
        self.sign_in()

if __name__ == '__main__':
    shihu = Spider()
    shihu.run()
