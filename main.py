import os
import numpy as np
import argparse
import cv2
from Enhancement import AGC, HE, CLAHE

model_path = './BRISQUE/brisque_model_live.yml'   # model data of BRISQUE
range_path = './BRISQUE/brisque_range_live.yml'   # Range data of BRISQUE

def parse():
    parser = argparse.ArgumentParser()

    parser.add_argument('img_dir', help='the dir of images')
    parser.add_argument('--output', help='the dir to save images',default='./output')
    parser.add_argument('--method', help = 'the method to enhance images',default= 'AGC')
    args = parser.parse_args()

    return args

def main():

    args = parse()

    os.makedirs(args.output,exist_ok=True)

    img_dir = args.img_dir
    img_list = os.listdir(img_dir)

    for img in img_list:
        img_path = os.path.join(img_dir, img)
        img_basename = os.path.basename(img_path)

        if args.method == "AGC":
            enhance = AGC()
            enhanced_img = enhance.gamma_correction(img_path)

        elif args.method == "HE":
            enhanced_img = HE(img_path)

        elif args.method == "CLAHE":
            enhanced_img = CLAHE(img_path)

        else:
            raise ValueError(f"The method {args.method} does not exist.")

        enhanced_img.save(f"{args.output}/enhanced_{img_basename}")

        enhanced_img_np = np.uint8(enhanced_img)
        score = cv2.quality.QualityBRISQUE_compute(enhanced_img_np, model_path,range_path)
        print('score =', score[0])

if __name__ == "__main__":
    main()
