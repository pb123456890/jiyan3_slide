import json
import os.path
import re
import time
import random

import cv2
import execjs
import requests
from PIL import Image
from loguru import logger


class JiYan3Slide:
    def __init__(self):
        self.img_path = "image/"
        self.img_req_prefix = "https://static.geetest.com/"
        self.gt = ""
        self.challenge1 = ""
        self.challenge2 = ""
        self.bg_img = ""
        self.fullbg_img = ""
        self.slice_img = ""
        self.c = []
        self.s = ""
        self.x = 0
        self.traceArr = []
        self.pass_time = 0
        self.js_file = "极验3滑块.js"
        self.w = ""

    def request1(self):
        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://demos.geetest.com/slide-float.html",
            "sec-ch-ua": "\"Chromium\";v=\"136\", \"Google Chrome\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }

        url = "https://demos.geetest.com/gt/register-slide"
        params = {
            "t": int(time.time() * 1000)
        }
        logger.info(f"请求1参数: {params}")
        response = requests.get(url, headers=headers, params=params)
        logger.info(f"响应1: {response.text}")
        result = json.loads(response.text)
        self.challenge1 = result["challenge"]
        self.gt = result["gt"]
        logger.info(f"获取到gt: {self.gt}")
        logger.info(f"获取到challenge1: {self.challenge1}")

    def request2(self):
        headers = {
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "referer": "https://demos.geetest.com/",
            "sec-ch-ua": "\"Chromium\";v=\"136\", \"Google Chrome\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "script",
            "sec-fetch-mode": "no-cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
        }
        url = "https://apiv6.geetest.com/gettype.php"
        params = {
            "gt": self.gt,
            "callback": "geetest_1748425641538"
        }
        logger.info(f"请求2参数: {params}")
        response = requests.get(url, headers=headers, params=params)
        logger.info(f"响应2: {response.text}")

    def request3(self):
        headers = {
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "referer": "https://demos.geetest.com/",
            "sec-ch-ua": "\"Chromium\";v=\"136\", \"Google Chrome\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "script",
            "sec-fetch-mode": "no-cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
        }

        url = "https://apiv6.geetest.com/get.php"
        params = {
            "gt": self.gt,
            "challenge": self.challenge1,
            "lang": "zh-cn",
            "pt": "0",
            "client_type": "web",
            "w": "tJl4eucd14)axYVCZE2oTkfPO5V7GzfJoMurOAKxhkt57jeDc2iOaMxuw4jNff8efQbeOSzF1fArS1Oj9(tjR)vn33rZdZEZs3XT5kUu)k8ZJP7XYWJYt7coOQywuHcyUmzqgJaEXsqsuSxICqwPv3xxcfXYOzChkH0xW03suLymhlSwOyKHRHYya1J6C8GaljYsKsHAyKORJJqElfgewJjYkpYFWVRu3GOvPBNAwsNGAwZMZhSWJ(NqPpt60QxFvBp5v5Z2OLP4J8r2lwPGWXemL1qfV1SW8n97DVmUElejcae0igcMTC8MdQsMSHtY9o2JMBX3B1iVq1GATvjMTMFkxmHt3Qoxtw0Ibr8mIllfa3)MbriYLWDo5tpgDuxHcme7zTIodcOIkXdN2nbRaf34rXt7gN3)FmlUL0pKcpn2(ntw81942wqq2gTqBj1MkB2TKQ1ge7EW(RRtKPjBOw(iwt(HWMoVUxcKErfzf46Rvo1ZVKiBKcyGO5qlR5DB3CAR2z2gDlOoSHR3f3Ofo4uRIS0yzp8VnOorILIl5wKkLNKmAu(6rSpPS0pGCivhqQN(dnlO76817wYn(WyHkQTFuywjxhbnJFJGPZVPgng3FPr21oxEXZSpaTgqJQ(oBunAKDWRNGqlhBowny9n5Mpa2illVIEElkhBVtVpdHZZf3WoJiGrjNLBOF(EPBt8aVUrQGeQz2zpEx8Lguurzq2(IVYITvWoYncyAS7IA2F1wk69(JNNNGpUUHgbdr1pIygiPtOcTNZBb5t3H9S2xq5c)U6kfiR2Y0hzVG7ghThENX6maU8jCLcRovR5xOu0KzJ)AHlisHjOBwbWzvi1yzyJtUwTN38HIMtLkzjyW3zRss3(am9v2qrrAwkeB3kefOKwrjbT7ejcaHwtSeivXjTMV2PvZOK6N1RSTMAHVW)Hjz5CZPTJPbmU7HhgN)0iv6OiquJ)3cKQpzLhEeV(4ftSH63U1j(M1gFkQ7tCfSyoarrFJdisAIlSxbeRXIPiNMkixn7Xzxe)8Mwol3lsKYGJT0uc11SfndV6T6KXE)M92CmNhyilisrXZrjDI3aA1p2D(E7bGYJ0pGflMXK4KQnW3d8N0(MBM90h2fL(GPnU6ZWDk3koJ8TdiVCObb2c69CmS3ktnVl(mZEIOxX8H85uGPMrJSN6PuhxYqL5zRdOvLaXBdXP0Eo(HmbF40y8gClarw5i0EvC9neDTzhjz2cUdH(Harll6LqXMpAScmU.70576ef61a3efced89de97963ebdede23ddc76257e346512b84e8d8d4c2dfadc7d8d49d14574b4ed30d78ffbc5c53f3504f8dfcacf9c8d8bcfffef7fa5f82910f811f7eed6a8b631c13eccfad2a6472e443a6101225cf68c5794e01ada3dd016c0fea556ae875bce50ebce0ace24d6fbb071174584bec70209506d6ff5c78a59",
            "callback": "geetest_1748426256875"
        }
        logger.info(f"请求3参数: {params}")
        response = requests.get(url, headers=headers, params=params)
        logger.info(f"响应3: {response.text}")

    def request4(self):
        headers = {
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Referer": "https://demos.geetest.com/",
            "Sec-Fetch-Dest": "script",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Storage-Access": "active",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Chromium\";v=\"136\", \"Google Chrome\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        url = "https://api.geevisit.com/ajax.php"
        params = {
            "gt": self.gt,
            "challenge": self.challenge1,
            "lang": "zh-cn",
            "pt": "0",
            "client_type": "web",
            "w": "xct7moGuFPBEOzVZaS0NLrOX6wTQav1ou)KsEK7)S0sw1URBSiEEPu0ggbMwbWVp)UCNExXM)M5P)3CtzW9BtF5jlTfd)G3E(7bAbfVjBnfk5SxgurYqrgpk8RGIiDuacrsLN3CoEwmMwf375agcDMTf)DAODiA8vSALySb8mPKJ8B91kWCzablXF6L1q2fkRgkzRTM2AQF)nA4gG2d6mJOW8C3ICVZLrCYwdlpjaWQ0CjruKutCKXeCZxM2FWrdT)sqDsRW8XXqgRcf7k0ErGWdyP1U4Lwn4t2Xy8EbL8GRyhqHE2SlokGE4)TIX6DVPgkDGhiWMDu7aYoJM07oUF6mjekTp2zXnqKH8WAoZBzarkUr0oMd0czA8WSvlEuSZCiXcGCvQps3qPNWynlmzFQghg4cDIR07QsmrwASpDW4iLFGQP0oHy)2EaRjtOh9kVHo387bfa3ukuJPd3TH7gSBkawjb11LRGB0RRF4aexLWx078VEonG9ySqNyo607ig6faPYkxudaC58HPwo)Y7FyVkMBzlDQfUUa)OXAohAPHyLOpaRDUwrvRfJnVH1C8a5WTvdrHbgGIDkkDzdU6qhbGu6HG6hKt)R5Wier(gUG5OGr6gk1tS9WeoCwluxGQQj(s68HDQ70hA9rhcR6f4z)Qc5et7rg(dCjssr1MZCABneo1sN99P82dWeQtYqfh00TRxjD33oU9)Ra)8YO0WDwojwDMzUnk1Pj6hYfF(nqqv4IYLEyfoojxht)JwyHEJPkpcQuNBWSmTRu7B4yZSfev0eE7AhTjV)F(HZEVUrsUNBgg8Yj2EqZxJHO8oYe3Cdwu97zbxV2FiJpB3sKWw1RT8eprELu5TK72i0FINMVODiCkzdG40PLIX(fpQyQwzrh2foILXJsCbAtIeZH59wSAK3Iy95ui09xNATbVy4bNqV21pDek4NZz8kJznzclhGn1q708pnbAmozx6kS56msNnlcsZj(dKRJi4FknE403pcmCUD42)XelYWMyZYiLBjJvxkwEMaCxkcweTFVhyUeZ550TjVIF4(G7eOX3CWg6(ZuQEgRUMvVrQq47XYEQ8W5pPjQy9o66Do6Zt5u4P2ORr814yIfDKGL5sTi)HPcE7KL1fL3p2qiw5vz6shCYW71ejBsZcU9bDjBda0xvL9EXN))DDkoDZrawq6ace66YfEoSXSOwjEOI)UqvMqwEst4SUkmvFwmDTUPDA6sq2KSr(D)J76DBccidgj57YQ7Fj2wy2ZreVET(19mOtPiagmsJvBnW1la3p7idQ7Yk7iGoh)sekniW2TErQWcahkJh05d4kzfaxoIWO5KGyboXlTeT6RG7gT0AATedIelEVH2aiMjscGpsFGlCVWBvEKg9rhDpv6PhthSXcQMYSeQXN4ekai7fSQ3l24FJxaTAX4F4FhSxTAoiYAjL4wmnJK(tNxaAqKp6Fq1aUL6rZFU0DGdbW)Dx7bBmNFkJmWs0FGcPuK8(kAXMUp(t069JjUmFV6PnlD9ZXjUDJ4WE5RjsGxp4pdfUWMTh2evrCwlerR(aQ)hbK80iGQZWJcwikTlBZ8FlijbYRhvKeRVGHC5cd4BgpIKWXD3W(wEEWKowRykPV5fY1ip7ypkuyj21rX1gE6BySsFh3)3vCPzpnPqyify4sWcohSJpXVjX3gWOfSn3ERTKNBBpyQs35eAqkymEmackWsL3mK8a4nD)8aXwiYM6)48T0ksjTYk53LQOtJLl0o0PMsfzOAaOxFPdqJaWZFMrlwNMSRq(492bCDwxNLgrZYr1OwJi3O2giZtFYViFMI(aU8iyVA1rl7TjoXGSLtSWWP5GmvMPyRzTk(mGYNVYP55SMxB35HCWXm8A)RQ8fRdSiDoG726mOCzPQ5oeSasfipgKYdwVhMiKkho9mPA4c9tVlIdgOs(UXOoIUUimzw)HE(lr73T2oOkB5W6GWZ60C8OK9f6AjBeGW3JAVIDh2o3cXuBW7aXBwvYibrmPsp3LsAyZxoCNVBWlJS2X4ip1plYgx9thHLe7hYJmr8GSYunQJHsRZYj)AgtURJzAimjO5XwgE5282JHNS6z96Kn9F91VT12fVN1sm)VXdcIQlf0BAzolPYMhY2oIPiFdcMj7W6bUNfY2JbtbMCZE85j8ov0H9wxR7I20D7l)Elq0Ocu7kreiXNTdoCNumY56JTcSnjWV1QZsPlGHSlUnHh)xFd)i0MgDm9ZWO1ybU9u13x4MtczzSjXeztB7)R)emQ8CE2X7(SUtxxwLPJ0q9IPOcnZYkrU2ZLcJ(B806pkGtb3GcpSOEcF7eOIgfs3VQeVZd13y(3nfoTTRhU2OjCg0)fRdvwFUHXjLLH1wQDH(ore076e72lACJicWza5pym5VzK9DCDp9IChNBVr4l4M(X4beLaifFX6cUtSDJLSy7Mkfh1Zh(QQ)LVoIA3)qxk5G7Y9uLqFgDrlhog)gwEXvdMPTjxW9IIC5bCLlRRa1(1trJzBobOSrCKe5vnet9OYPKu(icVQf3b1dH2CNnXjA0eNuv834nPX99qA",
            "callback": "geetest_1748426423105"
        }
        logger.info(f"请求4参数: {params}")
        response = requests.get(url, headers=headers, params=params)
        logger.info(f"响应4: {response.text}")

    def request5(self):
        headers = {
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Referer": "https://demos.geetest.com/",
            "Sec-Fetch-Dest": "script",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Storage-Access": "active",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Chromium\";v=\"136\", \"Google Chrome\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        url = "https://api.geevisit.com/get.php"
        params = {
            "is_next": "true",
            "type": "slide3",
            "gt": self.gt,
            "challenge": self.challenge1,
            "lang": "zh-cn",
            "https": "true",
            "protocol": "https://",
            "offline": "false",
            "product": "embed",
            "api_server": "api.geevisit.com",
            "isPC": "true",
            "autoReset": "true",
            "width": "100%",
            "callback": "geetest_1748426414603"
        }
        logger.info(f"请求5参数: {params}")
        response = requests.get(url, headers=headers, params=params)
        logger.info(f"响应5: {response.text}")
        result = re.search("\((.*)\)", response.text).group(1)
        res = json.loads(result)
        self.challenge2 = res["challenge"]
        self.bg_img = res["bg"]
        self.fullbg_img = res["fullbg"]
        self.slice_img = res["slice"]
        self.c = res["c"]
        self.s = res["s"]
        logger.info(f"获取到challenge2: {self.challenge2}")
        logger.info(f"获取到bg图片: {self.bg_img}")
        logger.info(f"获取到fullbg图片: {self.fullbg_img}")
        logger.info(f"获取到slice图片: {self.slice_img}")
        logger.info(f"获取到c: {self.c}")
        logger.info(f"获取到s: {self.s}")

    def download_img(self):
        if not os.path.exists(self.img_path):
            os.mkdir(self.img_path)
        bg_content = requests.get(self.img_req_prefix + self.bg_img).content
        self.bg_suffix = self.bg_img.split(".")[-1]
        with open(f"{self.img_path}bg.{self.bg_suffix}", "wb") as f:
            f.write(bg_content)
        fullbg_content = requests.get(self.img_req_prefix + self.fullbg_img).content
        self.fullbg_suffix = self.fullbg_img.split(".")[-1]
        with open(f"{self.img_path}fullbg.{self.fullbg_suffix}", "wb") as f:
            f.write(fullbg_content)
        slice_content = requests.get(self.img_req_prefix + self.slice_img).content
        self.slice_suffix = self.slice_img.split(".")[-1]
        with open(f"{self.img_path}slice.{self.slice_suffix}", "wb") as f:
            f.write(slice_content)
        logger.info(f"图片下载完成")

    def img_recover(self, image_path):
        o = image_path
        img = Image.open(o)
        serilize = [39, 38, 48, 49, 41, 40, 46, 47, 35, 34, 50, 51, 33, 32, 28, 29, 27, 26, 36, 37, 31, 30, 44, 45, 43,
                    42,
                    12, 13, 23, 22, 14, 15, 21, 20, 8, 9, 25, 24, 6, 7, 3, 2, 0, 1, 11, 10, 4, 5, 19, 18, 16, 17]
        target = Image.new('RGB', (260, 160))
        for i in range(52):
            c = serilize[i] % 26 * 12 + 1
            u = 80 if 25 < serilize[i] else 0
            box = (c, u, c + 10, u + 80)
            region = img.crop(box)
            b = 80 if 25 < i else 0
            target.paste(region, (i % 26 * 10, b))
        os.remove(o)
        target.save(os.path.splitext(o)[0] + '.jpg')

    def recover(self):
        self.img_recover(self.img_path + f"bg.{self.bg_suffix}")
        self.img_recover(self.img_path + f"fullbg.{self.fullbg_suffix}")
        logger.info("底图还原完成")

    def get_pos(self):
        bg_img = cv2.imread(self.img_path + f"bg.{self.bg_suffix}", 0)  # 背景图片（灰度模式）
        slider_img = cv2.imread(self.img_path + f"slice.{self.slice_suffix}", 0)  # 滑块图片（灰度模式）
        # 边缘检测
        bg_edge = cv2.Canny(bg_img, 100, 200)
        slider_edge = cv2.Canny(slider_img, 100, 200)
        # 模板匹配
        result = cv2.matchTemplate(bg_edge, slider_edge, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        # 返回缺口的横坐标
        x = max_loc[0]
        logger.info(f"获取到缺块横坐标为: {x}")
        self.x = x

        # slide = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
        # with open(self.img_path + f"bg.{self.bg_suffix}", "rb") as f:
        #     target_bytes = f.read()
        # with open(self.img_path + f"bg.{self.fullbg_suffix}", "rb") as f:
        #     background_bytes = f.read()
        # res = slide.slide_comparison(target_bytes, background_bytes)
        # self.x = res.get('target')[0]

    def __ease_out_expo(self, sep):
        if sep == 1:
            return 1
        else:
            return 1 - pow(2, -10 * sep)

    def get_slide_track(self):
        if not isinstance(self.x, int) or self.x < 0:
            raise ValueError(f"distance类型必须是大于等于0的整数: distance: {self.x}, type: {type(self.x)}")
        # 初始化轨迹列表
        slide_track = [
            [random.randint(-50, -10), random.randint(-50, -10), 0],
            [0, 0, 0],
        ]
        # 共记录count次滑块位置信息
        count = 30 + int(self.x / 2)
        # 初始化滑动时间
        t = random.randint(50, 100)
        # 记录上一次滑动的距离
        _x = 0
        _y = 0
        for i in range(count):
            # 已滑动的横向距离
            x = round(self.__ease_out_expo(i / count) * self.x)
            # 滑动过程消耗的时间
            t += random.randint(10, 20)
            if x == _x:
                continue
            slide_track.append([x, _y, t])
            _x = x
        slide_track.append(slide_track[-1])
        logger.info(f"获取到轨迹数组: {slide_track}")
        self.traceArr = slide_track
        self.pass_time = slide_track[-1][-1]

    def load_file(self):
        with open(self.js_file, "r", encoding="utf-8") as f:
            return f.read()

    def get_w(self):
        js_code = execjs.compile(self.load_file())
        self.w = js_code.call("get_w", self.x, self.challenge2, self.pass_time, self.traceArr, self.c, self.s, self.gt)
        logger.info(f"获取到w: {self.w}")

    def request6(self):
        headers = {
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Referer": "https://demos.geetest.com/",
            "Sec-Fetch-Dest": "script",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Storage-Access": "active",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Chromium\";v=\"136\", \"Google Chrome\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        url = "https://api.geevisit.com/ajax.php"
        params = {
            "gt": self.gt,
            "challenge": self.challenge2,
            "lang": "zh-cn",
            "%24_BCm": "0",
            "client_type": "web",
            "w": self.w,
            "callback": "geetest_1748442003056"
        }
        logger.info(f"请求6参数: {params}")
        response = requests.get(url, headers=headers, params=params)
        logger.info(f"响应6参数: {response.text}")

    def run(self):
        self.request1()
        self.request2()
        self.request3()
        self.request4()
        self.request5()
        self.download_img()
        self.recover()
        self.get_pos()
        self.get_slide_track()
        self.get_w()
        self.request6()

if __name__ == '__main__':
    slide3 = JiYan3Slide()
    slide3.run()
    # slide3.request1()
    # slide3.request2()
    # slide3.request3()
    # slide3.request4()
    # slide3.request5()
    # slide3.download_img()
    # slide3.recover()
    # slide3.get_pos()
    # slide3.get_slide_track()
    # slide3.get_w()
    # slide3.request6()

