import os

import cv2
import ddddocr
import requests
from PIL import Image

url = "https://static.geetest.com/" + "pictures/gt/09b7341fb/bg/ec3a7cad9.jpg"
img_content = requests.get(url).content
with open("./image_/bg.jpg", "wb") as f:
    f.write(img_content)

url = "https://static.geetest.com/" + "pictures/gt/09b7341fb/09b7341fb.jpg"
img_content = requests.get(url).content
with open("./image_/slide.jpg", "wb") as f:
    f.write(img_content)
url = "https://static.geetest.com/" + "pictures/gt/09b7341fb/09b7341fb.jpg"

# img_content = requests.get(url).content
# with open("./image_/fullbg.jpg", "wb") as f:
#     f.write(img_content)

def img_recover(image_name):
    o = f"./image_/{image_name}.jpg"
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

def get_pos():
    bg_img = cv2.imread('./image/bg.jpg', 0)  # 背景图片（灰度模式）
    slider_img = cv2.imread('./image/slide.jpg', 0)  # 滑块图片（灰度模式）
    # 边缘检测
    bg_edge = cv2.Canny(bg_img, 100, 200)
    slider_edge = cv2.Canny(slider_img, 100, 200)
    # 模板匹配
    result = cv2.matchTemplate(bg_edge, slider_edge, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    # 返回缺口的横坐标
    print(max_loc[0])
    x = max_loc[0]
    print("获取缺块x坐标: ", x)
    return x
    # slide = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
    # with open('./image_/bg.jpg', 'rb') as f:
    #     target_bytes = f.read()
    # with open('./image_/fullbg.jpg', 'rb') as f:
    #     background_bytes = f.read()
    # res = slide.slide_comparison(target_bytes, background_bytes)
    # return res.get('target')[0]

img_recover("bg")
img_recover("fullbg")
print(get_pos())