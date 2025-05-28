import json
import os
import random
import re
import time
import cv2
import ddddocr as ddddocr
import execjs
import requests
from PIL import Image
from loguru import logger

import 轨迹数组生成 as Trace

challenge1 = ""
challenge2 = ""
c = []
s = ""
x = 0

def load_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def img_recover(image_path):
    o = image_path
    img = Image.open(o)
    serilize = [39, 38, 48, 49, 41, 40, 46, 47, 35, 34, 50, 51, 33, 32, 28, 29, 27, 26, 36, 37, 31, 30, 44, 45, 43, 42,
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
    logger.info("底图还原完成")

def get_pos():
    bg_img = cv2.imread('./image/bg.jpg', 0)  # 背景图片（灰度模式）
    slider_img = cv2.imread('./image/slice.jpg', 0)  # 滑块图片（灰度模式）
    # 边缘检测
    bg_edge = cv2.Canny(bg_img, 100, 200)
    slider_edge = cv2.Canny(slider_img, 100, 200)
    # 模板匹配
    result = cv2.matchTemplate(bg_edge, slider_edge, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    # 返回缺口的横坐标
    x = max_loc[0]
    return x
    # slide = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
    # with open('./image/bg.jpg', 'rb') as f:
    #     target_bytes = f.read()
    # with open('./image/fullbg.jpg', 'rb') as f:
    #     background_bytes = f.read()
    # res = slide.slide_comparison(target_bytes, background_bytes)
    # return res.get('target')[0]

def request1():
    headers1 = {
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
    url1 = "https://demos.geetest.com/gt/register-slide"
    params1 = {
        "t": "1747844229639"
    }
    response1 = requests.get(url1, headers=headers1, params=params1)
    logger.info(f"响应1: {response1.text}")
    params1["t"] = (time.time() * 1000)
    res1 = json.loads(response1.text)
    global challenge1, gt
    challenge1 = res1["challenge"]
    gt = res1["gt"]
    logger.info(f"获取到gt: {gt}")
    logger.info(f"获取到challenge1: {challenge1}")

def request2(gt):
    headers2 = {
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
    url2 = "https://apiv6.geetest.com/gettype.php"
    params2 = {
        "gt": "019924a82c70bb123aae90d483087f94",
        "callback": "geetest_1747848418221"
    }
    params2["gt"] = gt
    params2["callback"] = f"geetest_{int(time.time() * 1000)}"
    response2 = requests.get(url2, headers=headers2, params=params2)
    logger.info(f"响应2: {response2.text}")

def request3(challenge1, gt):
    headers3 = {
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
    url3 = "https://apiv6.geetest.com/get.php"
    params3 = {
        "gt": "019924a82c70bb123aae90d483087f94",
        "challenge": "7570e5cb23bb811b6e618b0daa320093",
        "lang": "zh-cn",
        "pt": "0",
        "client_type": "web",
        "w": "tJl4eucd14)axYVCZE2oTkfPO5V7GzfJoMurOAKxhkt57jeDc2iOaMxuw4jNff8efQbeOSzF1fArS1Oj9(tjR)vn33rZdZEZs3XT5kUu)k8ZJP7XYWJYt7coOQywuHcyUmzqgJaEXsqsuSxICqwPv3xxcfXYOzChkH0xW03suLymhlSwOyKHRHYya1J6C8GaljYsKsHAyKORJJqElfgewJjYkpYFWVRu3GOvPBNAwsNGAwZMZhSWJ(NqPpt60QxFvBp5v5Z2OLP4J8r2lwPGWXemL1qfV1SW8n97DVmUElejcae0igcMTC8MdQsMSHtY9o2JMBX3B1iVq1GATvjMTMFkxmHt3Qoxtw0Ibr8mIllfa3)MbriYLWDo5tpgDuxHcme7zTIodcOIkXdN2nbRaf34rXt7gN3)FmlUL0pKcpn2(ntw81942wqq2gTqBj1MkB2TKQ1ge7EW(RRtKPjBOw(iwt(HWMoVUxcKErfzf46Rvo1ZVKiBKcyGO5qlR5DB3CAR2z2gDlOoSHR3f3Ofo4uRIS0yzp8VnOorILIl5wKkLNKmAu(6rSpPS0pGCivhqQN(dnlO76817wYn(WyHkQTFuywjxhbnJFJGPZVPgng3FPr21oxEXZSpaTgqJQ(oBunAKDWRNGqlhBowny9n5Mpa2illVIEElkhBVtVpdHZZf3WoJiGrjNLBOF(EPBt8aVUrQGeQz2zpEx8Lguurzq2(IVYITvWoYncyAS7IA2F1wk69(JNNNGpUUHgbdr1pIygiPtOcTNZBb5t3H9S2xq5c)U6kfiR2Y0hzVG7ghThENX6maU8jCLcRovR5xOu0KzJ)AHlisHjOBwbWzvi1yzyJtUwTN38HIMtLkzjyW3zRss3(am9v2qrrAwkeB3kefOKwrjbT7ejcaHwtSeivXjTMV2PvZOK6N1RSTMAHVW)Hjz5CZPTJPbmU7HhgN)0iv6OiquJ)3cKQpzLhEeV(4ftSH63U1j(M1gFkQ7tCfSyoarrFJdisAIlSxbeRXIPiNMkixn7Xzxe)8Mwol3lsKYGJT0uc11SfndV6T6KXE)M92CmNhyilisrXZrjDI3aA1p2D(E7bGYJ0pGflMXK4KQnW3d8N0(MBM90h2fL(GPnU6ZWDk3koJ8TdiVCObb2c69CmS3ktnVl(mZEIOxX8H85uGPMrJSN6PuhxYqL5zRdOvLaXBdXP0Eo(HmbF40y8gClarw5i0EvC9neDTzhjz2cUdH(Harll6LqXMpAScmU.70576ef61a3efced89de97963ebdede23ddc76257e346512b84e8d8d4c2dfadc7d8d49d14574b4ed30d78ffbc5c53f3504f8dfcacf9c8d8bcfffef7fa5f82910f811f7eed6a8b631c13eccfad2a6472e443a6101225cf68c5794e01ada3dd016c0fea556ae875bce50ebce0ace24d6fbb071174584bec70209506d6ff5c78a59",
        "callback": "geetest_1747848414270"
    }
    params3["challenge"] = challenge1
    params3["gt"] = gt
    response3 = requests.get(url3, headers=headers3, params=params3)
    logger.info(f"响应3: {response3.text}")

def request4(challenge1, gt):
    headers4 = {
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
    url4 = "https://api.geevisit.com/ajax.php"
    params4 = {
        "gt": "019924a82c70bb123aae90d483087f94",
        "challenge": "7570e5cb23bb811b6e618b0daa320093",
        "lang": "zh-cn",
        "pt": "0",
        "client_type": "web",
        "w": "xct7moGuFPBEOzVZaS0NLrOX6wTQav1ou)KsEK7)S0sw1URBSiEEPu0ggbMwbWVp)UCNExXM)M5P)3CtzW9BtF5jlTfd)G3E(7bAbfVjBnfk5SxgurYqrgpk8RGIiDuacrsLN3CoEwmMwf375agcDMTf)DAODiA8vSALySb8mPKJ8B91kWCzablXF6L1q2fkRgkzRTM2AQF)nA4gG2d6mJOW8C3ICVZLrCYwdlpjaWQ0CjruKutCKXeCZxM2FWrdT)sqDsRW8XXqgRcf7k0ErGWdyP1U4Lwn4t2Xy8EbL8GRyhqHE2SlokGE4)TIX6DVPgkDGhiWMDu7aYoJM07oUF6mjekTp2zXnqKH8WAoZBzarkUr0oMd0czA8WSvlEuSZCiXcGCvQps3qPNWynlmzFQghg4cDIR07QsmrwASpDW4iLFGQP0oHy)2EaRjtOh9kVHo387bfa3ukuJPd3TH7gSBkawjb11LRGB0RRF4aexLWx078VEonG9ySqNyo607ig6faPYkxudaC58HPwo)Y7FyVkMBzlDQfUUa)OXAohAPHyLOpaRDUwrvRfJnVH1C8a5WTvdrHbgGIDkkDzdU6qhbGu6HG6hKt)R5Wier(gUG5OGr6gk1tS9WeoCwluxGQQj(s68HDQ70hA9rhcR6f4z)Qc5et7rg(dCjssr1MZCABneo1sN99P82dWeQtYqfh00TRxjD33oU9)Ra)8YO0WDwojwDMzUnk1Pj6hYfF(nqqv4IYLEyfoojxht)JwyHEJPkpcQuNBWSmTRu7B4yZSfev0eE7AhTjV)F(HZEVUrsUNBgg8Yj2EqZxJHO8oYe3Cdwu97zbxV2FiJpB3sKWw1RT8eprELu5TK72i0FINMVODiCkzdG40PLIX(fpQyQwzrh2foILXJsCbAtIeZH59wSAK3Iy95ui09xNATbVy4bNqV21pDek4NZz8kJznzclhGn1q708pnbAmozx6kS56msNnlcsZj(dKRJi4FknE403pcmCUD42)XelYWMyZYiLBjJvxkwEMaCxkcweTFVhyUeZ550TjVIF4(G7eOX3CWg6(ZuQEgRUMvVrQq47XYEQ8W5pPjQy9o66Do6Zt5u4P2ORr814yIfDKGL5sTi)HPcE7KL1fL3p2qiw5vz6shCYW71ejBsZcU9bDjBda0xvL9EXN))DDkoDZrawq6ace66YfEoSXSOwjEOI)UqvMqwEst4SUkmvFwmDTUPDA6sq2KSr(D)J76DBccidgj57YQ7Fj2wy2ZreVET(19mOtPiagmsJvBnW1la3p7idQ7Yk7iGoh)sekniW2TErQWcahkJh05d4kzfaxoIWO5KGyboXlTeT6RG7gT0AATedIelEVH2aiMjscGpsFGlCVWBvEKg9rhDpv6PhthSXcQMYSeQXN4ekai7fSQ3l24FJxaTAX4F4FhSxTAoiYAjL4wmnJK(tNxaAqKp6Fq1aUL6rZFU0DGdbW)Dx7bBmNFkJmWs0FGcPuK8(kAXMUp(t069JjUmFV6PnlD9ZXjUDJ4WE5RjsGxp4pdfUWMTh2evrCwlerR(aQ)hbK80iGQZWJcwikTlBZ8FlijbYRhvKeRVGHC5cd4BgpIKWXD3W(wEEWKowRykPV5fY1ip7ypkuyj21rX1gE6BySsFh3)3vCPzpnPqyify4sWcohSJpXVjX3gWOfSn3ERTKNBBpyQs35eAqkymEmackWsL3mK8a4nD)8aXwiYM6)48T0ksjTYk53LQOtJLl0o0PMsfzOAaOxFPdqJaWZFMrlwNMSRq(492bCDwxNLgrZYr1OwJi3O2giZtFYViFMI(aU8iyVA1rl7TjoXGSLtSWWP5GmvMPyRzTk(mGYNVYP55SMxB35HCWXm8A)RQ8fRdSiDoG726mOCzPQ5oeSasfipgKYdwVhMiKkho9mPA4c9tVlIdgOs(UXOoIUUimzw)HE(lr73T2oOkB5W6GWZ60C8OK9f6AjBeGW3JAVIDh2o3cXuBW7aXBwvYibrmPsp3LsAyZxoCNVBWlJS2X4ip1plYgx9thHLe7hYJmr8GSYunQJHsRZYj)AgtURJzAimjO5XwgE5282JHNS6z96Kn9F91VT12fVN1sm)VXdcIQlf0BAzolPYMhY2oIPiFdcMj7W6bUNfY2JbtbMCZE85j8ov0H9wxR7I20D7l)Elq0Ocu7kreiXNTdoCNumY56JTcSnjWV1QZsPlGHSlUnHh)xFd)i0MgDm9ZWO1ybU9u13x4MtczzSjXeztB7)R)emQ8CE2X7(SUtxxwLPJ0q9IPOcnZYkrU2ZLcJ(B806pkGtb3GcpSOEcF7eOIgfs3VQeVZd13y(3nfoTTRhU2OjCg0)fRdvwFUHXjLLH1wQDH(ore076e72lACJicWza5pym5VzK9DCDp9IChNBVr4l4M(X4beLaifFX6cUtSDJLSy7Mkfh1Zh(QQ)LVoIA3)qxk5G7Y9uLqFgDrlhog)gwEXvdMPTjxW9IIC5bCLlRRa1(1trJzBobOSrCKe5vnet9OYPKu(icVQf3b1dH2CNnXjA0eNuv834nPX99qA",
        "callback": "geetest_1747848415327"
    }
    params4["challenge"] = challenge1
    params4["gt"] = gt
    response4 = requests.get(url4, headers=headers4, params=params4)
    logger.info(f"响应4: {response4.text}")

def request5(challenge1, gt):
    headers5 = {
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
    url5 = "https://api.geevisit.com/get.php"
    params5 = {
        "is_next": "true",
        "type": "slide3",
        "gt": "019924a82c70bb123aae90d483087f94",
        "challenge": "dd014f022cd3d173e1867994a5f2b167",
        "lang": "zh-cn",
        "https": "true",
        "protocol": "https://",
        "offline": "false",
        "product": "embed",
        "api_server": "api.geevisit.com",
        "isPC": "true",
        "autoReset": "true",
        "width": "100%",
        "callback": "geetest_1747844320863"
    }

    params5["challenge"] = challenge1
    params5["gt"] = gt
    response = requests.get(url5, headers=headers5, params=params5)
    logger.info(f"响应5: {response.text}")
    result = re.search(r"\((.*)\)", response.text).group(1)
    res5 = json.loads(result)
    global challenge2, c, s
    challenge2 = res5["challenge"]
    c = res5["c"]
    s = res5["s"]
    bg_url = "https://static.geetest.com/" + res5["bg"]
    bg_content = requests.get(bg_url).content
    with open("./image/bg.jpg", "wb") as bg:
        bg.write(bg_content)
    slice_url = "https://static.geetest.com/" + res5["slice"]
    slice_content = requests.get(slice_url).content
    with open("./image/slice.jpg", "wb") as sc:
        sc.write(slice_content)
    fullbg_url = "https://static.geetest.com/" + res5["fullbg"]
    fullbg_content = requests.get(fullbg_url).content
    with open("./image/fullbg.jpg", "wb") as fb:
        fb.write(fullbg_content)
    img_recover("./image/bg.jpg")
    img_recover("./image/fullbg.jpg")
    global x
    x = get_pos()
    logger.info(f"获取到challenge2: {challenge2}")
    logger.info(f"获取到bg图片: {bg_url}")
    logger.info(f"获取到fullbg图片: {slice_url}")
    logger.info(f"获取到slice图片: {fullbg_url}")
    logger.info(f"获取到c: {c}")
    logger.info(f"获取到s: {s}")
    logger.info(f"获取到x: {x}")


def request6(x, challenge2, gt, c, s):
    js_code = execjs.compile(load_file('极验滑块.js'))
    traceArr = Trace.get_slide_track(x)   # 轨迹数组
    logger.info(f"轨迹数组: {traceArr}")
    logger.info(f"passtime: {traceArr[-1][-1]}")
    w3 = js_code.call("get_w", x, challenge2, traceArr[-1][-1], traceArr, c, s, gt)
    headers6 = {
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
    url6 = "https://api.geevisit.com/ajax.php"
    params6 = {
        "gt": "019924a82c70bb123aae90d483087f94",
        "challenge": "72fffff59437b320d6414d1ad711b6ccft",
        "lang": "zh-cn",
        "$_BCm": "0",
        "client_type": "web",
        "w": "CT05at4hSuoR8tBiMQAHYobD0rlP6wS7XmTw5jP5M3faroozb)MFzeyOnLlBRE2yCgQciYwSIi5Fp)3ADZOUmM21)E1iNzWu9DC6aTwBd(Yx1ZxrwWhqW05qcDj0YKwGJ4qkA1aEhfEaNgvLohxzvXXU(GJ9P6naJZLrvzTinq5dSVBifRWo9X5SbnjgEWWDnix(5GgfxuNRvPHGp4Z(XtlrcQv)akyK16PXAHwqGdEmzZANOCCm1iyCZZ8nOSS2uUHVAwmOc4nJ1hvgvS54z7yDLbvyI8W7wDGYr(vat3fiLr4miWGQZRq2NjgVJpFTLsBLVrrjxUKc5j(yHuT7Pt5zhCZowDbVmqgqTv564Z7t3e9c0rN46U4ot)QVFyyMe4G3sYAhG4rPkBZQ4i1kIUz3NoPKrBr6o57LiSTuVXo)J9z3dd0vVqJwa4A4ntT)7AryWu0WXC0FzCouTv3nXg7s)ibUL9(3nj)5WeAJCHc4py8D8nf)uifXfi7qoW3jed0OUql(ZjDM79FzZj7cvCmtOfTqb(bCblybFrfY8yMGjENZ0T1fSicnHdCKZ8JG5wEMbtAFkF)8v9uT61Y2noAdRRV3T63H)Q78czY8jxu21cZkgwaGCznrpKz(L1H4zrpA80PMuZ6fQy63O)01lpP)Zf4tkEJKEk)RjyCJTMp9zXsCGqWJkLpnuhHppG40qfdzyL35OvYGDx5xKL)RKglcRo0nzImbXNKcaRERIr0ztjNMZKL4vYKEoql78DhqB9i64RruJrInVC3Gwu5Oa05nkIh(1eO2D2M(UrOnom6hhzux48HYtLayg1m7Yvx1mIr5X(vtbZDiVv5A7Kgsy22tcUr(GFcDncppABABZOu6(26RiR58aKX6nXk6pLzjTl2WJ(ETapc3BckllpjM1egPnLZ7S1UEMOj6bX6q1)oSmBklfOaJgwXXLKPQoLtICBK7ntYzx(elEFBdrKTxs2c8JTvsKPRdMZNPMLUNrWjKCUTGza9bqZcJdTz)MXqV71d9a7867c78667e5a7ac59ccd2e5423b7d46f248946732fb9819448974e91128d73fdf32f0fbe8c9fdda87a53abebb327b8c348e0dfdfc5fb1e1565e0d056d6f39881993443103e87284fbfb3d354af6ab6718034eb3d68ac083f3d4b2bd14cd93263f8a9871e3a27bcc5b6a46c55e4b0ca75ae21b5460d61e88988a6214450",
        "callback": "geetest_1748022064556"
    }
    params6["gt"] = gt
    params6["challenge"] = challenge2
    params6["w"] = w3
    response = requests.get(url6, headers=headers6, params=params6)
    logger.info(f"响应6: {response.text}")

if __name__ == '__main__':
    request1()
    request2(gt)
    request3(challenge1, gt)
    request4(challenge1, gt)
    request5(challenge1, gt)
    request6(x, challenge2, gt, c, s)
