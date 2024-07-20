from paddleocr import PaddleOCR
from paddleocr import draw_ocr
from PIL import Image
from paddleocr import PPStructure, draw_structure_result, save_structure_res
import cv2
import os

from PyQt5.QtWidgets import QApplication,QMainWindow, QFileDialog, QMessageBox, QListWidget, QInputDialog, QLineEdit, QListWidgetItem

path = os.getcwd() #获取当前路径

def identi(img_path, lang_choice):
    #这里的img_path应为截图之后的路径

    if lang_choice == 'ch':
        ocr = PaddleOCR(det_model_dir = '..\PaddleOCR\output\ch_db_res18_7.22_inference', use_angle_cls=True, lang="ch", use_gpu=False, ir_optim=False)
    elif lang_choice == 'en':
        ocr = PaddleOCR(det_model_dir = '..\PaddleOCR\output\ch_db_res18_7.22_inference', use_angle_cls=True, lang="en", use_gpu=False, ir_optim=False)
        #ocr = PaddleOCR(use_angle_cls=True, use_gpu=True, ir_optim=False)

    print(lang_choice)
    result = ocr.ocr(img_path, cls=True)
    for line in result:
        print(line)
    # 显示结果

    image = Image.open(img_path).convert('RGB')
    boxes = [detection[0] for line in result for detection in line]  # Nested loop added
    txts = [detection[1][0] for line in result for detection in line]  # Nested loop added
    scores = [detection[1][1] for line in result for detection in line]  # Nested loop added
    new_txts = [x.strip() for x in txts if x.strip() != '']         #去除列表中元素的前后空格和换行
    scores = [line[1][1] for line in result]  # 识别置信度
    #im_show = draw_ocr(image, boxes, new_txts, scores)
    im_show = draw_ocr(image, boxes)
    im_show = Image.fromarray(im_show)
    im_show.save('results.jpg')  # 结果图片保存在代码同级文件夹中。

    return new_txts   #传递列表



def identi_more_pic(img_path, lang_choice):
    # 这里的img_path应为截图之后的路径,存放路径的列表

    if lang_choice == 'ch':
        ocr = PaddleOCR(det_model_dir = '..\PaddleOCR\output\ch_db_res18_7.22_inference', use_angle_cls=True, lang="en", use_gpu=False, ir_optim=False)
    elif lang_choice == 'en':
        ocr = PaddleOCR(det_model_dir = '..\PaddleOCR\output\ch_db_res18_7.22_inference', use_angle_cls=True, lang="en", use_gpu=False, ir_optim=False)

    print(lang_choice)

    final_txt = []

    for i in range(0,len(img_path)):
        result = ocr.ocr(img_path[i])
        for line in result:
            print(line)
        # 显示结果

        image = Image.open(img_path[i]).convert('RGB')

        boxes = [detection[0] for line in result for detection in line]  # Nested loop added
        txts = [detection[1][0] for line in result for detection in line]  # Nested loop added
        scores = [detection[1][1] for line in result for detection in line]  # Nested loop added

        '''
        boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        scores = [line[1][1] for line in result]
        '''



        if len(boxes) == 0:
            print("这张图片中没有识别出信息")
            continue


        # 把列表变成字符串
        #txts = " ".join('%s' %id for id in txts)

        new_txts = [x.strip() for x in txts if x.strip() != '']  # 去除列表中元素的前后空格和换行
        final_txt.extend(new_txts)
        #scores = [line[1][1] for line in result]  # 识别置信度
        # im_show = draw_ocr(image, boxes, new_txts, scores)
        im_show = draw_ocr(image, boxes)
        im_show = Image.fromarray(im_show)
        im_show.save(f'results_{i + 1}.jpg')  # 结果图片保存在代码同级文件夹中。

    return final_txt  # 传递列表


def identi_BGA(img_path):
    table_engine = PPStructure(show_log=True)
    print("识别BGA类型图片")
    img = cv2.imread(img_path)

    result = table_engine(img)
    print("result:\n", result)

    save_folder = './output/table'

    save_structure_res(result, save_folder, os.path.basename(img_path).split('.')[0])

    print("name:", os.path.basename(img_path).split('.')[0])

    #for line in result:
    #    line.pop('img')
    #    print(line)

    from PIL import Image

    #font_path = 'PaddleOCR/doc/fonts/simfang.ttf'  # PaddleOCR下提供字体包
    #image = Image.open(img_path).convert('RGB')
    #im_show = draw_structure_result(image, result, font_path=font_path)
    #im_show = Image.fromarray(im_show)
    #im_show.save('result.jpg')




    #save_structure_res(result, save_folder, os.path.basename(img_path).split('.')[0])

