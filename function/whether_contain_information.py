from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
import cv2
import matplotlib.pyplot as plt

#判断芯片是两排的还是四排的
def judge(img_path):
    ocr = PaddleOCR(use_angle_cls=True, lang="en", use_gpu=True, ir_optim=False, rec=False)
    result = ocr.ocr(img_path, cls=True, rec=False)
    for line in result:
        print(line)
    #image = Image.open(img_path).convert('RGB')
    boxes = [line for line in result]  # 文本框     只检测



    if len(boxes) == 0:
        print('无信息')
        return 0
    else:
        #location.append(boxes)
        print("有信息")
        return 1

def judge_(img_path, location):
    ocr = PaddleOCR(use_angle_cls=True, lang="en", use_gpu=True, ir_optim=False, rec=False)
    result = ocr.ocr(img_path, cls=True, rec=False)
    #or line in result:
        #print(line)
    #image = Image.open(img_path).convert('RGB')
    boxes = [line for line in result]  # 文本框     只检测



    if len(boxes) == 0:
        #print('无信息')
        return 0
    else:
        location.append(boxes)
        #print("有信息")
        return 1
