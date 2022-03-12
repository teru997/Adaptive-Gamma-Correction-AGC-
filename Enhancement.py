import numpy as np
from PIL import Image,ImageOps
import math
import cv2

class AGC:

    def first_classifies(self,img):

        t = 3.0
        v = img[:,:,2]
        mean = np.mean(v)
        std = np.std(v)
        D = (mean + 2*std) - (mean - 2*std)

        if D <= (1.0 / t):
            #low-contrast class
            return 1
        else: #high (or moderate)contrast class
            return 2

    def Heaviside(self,x): #式6
        if x <= 0:
            return 0
        else:
            return 1

    def logarithmic_func(self,img): #class1

        v = img[:,:,2]
        mean = np.mean(v)
        std = np.std(v)

        #γを設定 式3
        gamma = -1 * math.log2(std)

        #kを設定 式5
        k = v ** gamma + (1.0 - v ** gamma) * mean ** gamma

        #cを設定 式4
        c = 1 / (1 +  self.Heaviside(0.5 - mean) * (k - 1.0))

        return gamma,c

    def exponential_func(self,img): # class2

        v = img[:,:,2]
        mean = np.mean(v)
        std = np.std(v)

        #γを設定 式9
        gamma = math.exp(1 - (mean + std)/2)

        #kを設定 式5
        k = v ** gamma + (1.0 - v ** gamma) * mean ** gamma

        #cを設定 式4
        c = 1 / (1 + self.Heaviside(0.5 - mean) * (k - 1.0))

        return gamma,c

    def gamma_correction(self, img_path: str):

        img =  Image.open(f"{img_path}")

        img_hsv_pil = img.convert("HSV")
        img_hsv = np.float64(img_hsv_pil)/255.0
        #式1
        class_num = self.first_classifies(img_hsv)
        print("class:",class_num)

        #ガンマ,cの計算
        if class_num == 1:
            gamma,c = self.logarithmic_func(img_hsv)
        else:
            gamma,c = self.exponential_func(img_hsv)
        #in -> out
        img_hsv[:,:,2] = c * (img_hsv[:,:,2] ** gamma)
        #hsv ->　RGB
        img_hsv = np.uint8(img_hsv*255)
        img_hsv_PIL = Image.fromarray(img_hsv,'HSV') #ちゃんとHSVを指定してあげないと変な画像になる
        img_rgb = img_hsv_PIL.convert("RGB")

        return img_rgb

def HE(img_path):

    img =  Image.open(f"{img_path}")

    #HE
    img_hsv = img.convert("HSV")
    H, S, V = img_hsv.split()
    V = ImageOps.equalize(V)
    enhanced_img_hsv = Image.merge("HSV", (H, S, V))
    enhanced_img_rgb = enhanced_img_hsv.convert("RGB")

    #output
    return enhanced_img_rgb

def CLAHE(img_path: str,clipLimit=2.0,tileGridSize_h=8, tileGridSize_w=8):

    img =  Image.open(f"{img_path}")
    clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=(tileGridSize_h,tileGridSize_w))

    #CLAHE
    img_hsv = img.convert("HSV")
    img_hsv = np.uint8(img_hsv).copy()
    v = img_hsv[:,:,2].copy()
    img_hsv[:,:,2] = clahe.apply(v)
    enhanced_img_hsv = Image.fromarray(img_hsv,'HSV')
    enhanced_img_rgb = enhanced_img_hsv.convert("RGB")

    return enhanced_img_rgb