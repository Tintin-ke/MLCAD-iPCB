import cv2
import numpy as np
from paddleocr import PaddleOCR, draw_ocr
import math

def find_name(midpoint, image, name):
    print("\n开始寻找名字！")
    #name = ''   #定义一个空的字符串，存储芯片的名字（如果有的话）
    #image = cv2.imread(img_path)
    ocr = PaddleOCR(det_model_dir = '../PaddleOCR/output/ch_db_res18_7.22_inference', use_angle_cls=True, lang = 'en',use_gpu=True, ir_optim=False)

    result = ocr.ocr(image, cls=True, rec=False)          #error
    for line in result:
        for detection in line:
            print("detection:\n", detection)
            print("[0][0]:", detection[0][0])
            flag = isinside(detection[0][0], detection[0][1],
                    detection[1][0], detection[1][1],
                    detection[3][0], detection[3][1],
                    detection[2][0], detection[2][1],
                    midpoint[0], midpoint[1])
            #print(line[0][0], line[0][1],
                    #line[1][0], line[1][1],
                    #line[2][0], line[2][1],
                    #line[3][0], line[3][1],
                    #midpoint[0], midpoint[1])
            if flag == True:
                print("\n找到了名字！")
                #参数 tr[1]:左上角或右上角的纵坐标值 参数bl[1]:左下角或右下角的纵坐标值 参数tl[0]:左上角或左下角的横坐标值 参数br[0]:右上角或右下角的横坐标值
                crop = image[int(detection[0][1]):int(detection[2][1]), int(detection[0][0]):int(detection[1][0]) ]
                #cv2.imshow("name", crop)
                #cv2.waitKey()
                result_1 = ocr.ocr(crop, cls=True)
                name_ = [detection[1][0] for line in result_1 for detection in line]  # 文字
                name_ = [x.strip() for x in name_ if x.strip() != '']  # 去除列表中元素的前后空格和换行
                #name.append(name_[0])
                #print("函数内芯片名字：", name_[0])

                #将这一区域内的像素全部转换成白色
                image[int(detection[0][1]):int(detection[2][1]), int(detection[0][0]):int(detection[1][0])] = [255, 255, 255]
                #cv2.imshow('white', image)
                #cv2.waitKey()

                return image
    print('本芯片图片中不包含名字')
    #name_ = ''
    #name.append(name_)
    return image

#判断这个矩形是否是平行于坐标轴的
def isinmatrix(x1,y1,x2,y2,x,y):
    if x <= x1 or x >= x2 or y <= y1 or y >= y2:
        return False
    return True

#判断中点是否在矩形中间,line为矩形的四个点,midpoint为中点
def isinside(x1,y1,x2,y2,x3,y3,x4,y4,x,y):
    if y1 == y2: return isinmatrix(x1, y1, x4, y4, x, y)
    l, k, s = y4 - y3, x4 - x3, math.sqrt((x4 - x3) ** 2 + (y4 - y3) ** 2)
    cos, sin = l / (s + float("1e-8")), k / (s + float("1e-8"))
    x1r, y1r = x1 * cos + y1 * sin, y1 * cos - x1 * sin
    x4r, y4r = x4 * cos + y4 * sin, y4 * cos - x4 * sin
    xr, yr = x * cos + y * sin, y * cos - x * sin
    return isinmatrix(x1r, y1r, x4r, y4r, xr, yr)

#进一步分割图片
def split_numandname(x, y, w, h, width, height, imagepath, up_down):
    #imgpath为列表
    print("imagepath:", imagepath)

    new_imgpath = []
    # 距离图片左边界距离x， 距离图片上边界距离y，距离图片左边界距离+裁剪框宽度x+w，距离图片上边界距离+裁剪框高度y+h
    if len(imagepath) == 4:
        print("这是一个四排的芯片")
        img_1 = cv2.imread(imagepath[0])
        img_2 = cv2.imread(imagepath[1])
        img_3 = cv2.imread(imagepath[2])
        img_4 = cv2.imread(imagepath[3])

        cv2.imwrite('img_4.jpg',img_4)
        print("读取完毕")

        #顺序为上、左、右、下
        size_1 = img_1.shape
        size_3 = img_3.shape
        size_4 = img_4.shape
        width_1 = size_1[1]
        height_1 = size_1[0]
        width_3 = size_3[1]
        height_4 = size_4[0]
        width_4 = size_4[1]


        #不对1和4旋转90°，应该怎么切分
        cv2.imwrite("1.jpg", img_1[0:y, :])  # name
        cv2.imwrite("2.jpg", img_1[y:height_1, :])

        cv2.imwrite("7.jpg", img_4[0:int(h / 2), :])  # name
        cv2.imwrite("8.jpg", img_4[int(h / 2):height_4, :])


        '''
        #旋转90°后这么切分
        cv2.imwrite("1.jpg", img_1[:, width_1 - y:width_1])       #name
        cv2.imwrite("2.jpg", img_1[:, 0:width_1 - y])

        cv2.imwrite("7.jpg", img_4[:, 0:height - y - h])       #name
        cv2.imwrite("8.jpg", img_4[:, height - y - h:height_4])
        '''
        


        cv2.imwrite("3.jpg", img_2[:, 0:x])  # name
        cv2.imwrite("4.jpg", img_2[:, x:int(x + (w / 2))])

        cv2.imwrite("5.jpg", img_3[:, int(w / 2):width_3])       #name
        cv2.imwrite("6.jpg", img_3[:, 0:int(w / 2)])



        print("切分完成")

    elif len(imagepath) == 2:
        print("这是一个两排的芯片")
        img_1 = cv2.imread(imagepath[0])
        img_2 = cv2.imread(imagepath[1])
        size = img_2.shape
        width_ = size[1]  # 宽度
        height_ = size[0]
        print("读取完毕")
        if up_down == 0:
            cv2.imwrite("1.jpg", img_1[y:y + h, 0:x])  # name
            cv2.imwrite("2.jpg", img_1[y:y + h, x:int(x + (w / 2))])
            print("x+w:", x + w)
            print("width:", width)
            cv2.imwrite("3.jpg", img_2[y:y + h, (x + w) - int(width / 2):width_])  # name
            print("2-1")

            cv2.imwrite("4.jpg", img_2[y:y + h, 0:(x + w) - int(width / 2)])
            print("over")
        elif up_down == 1:
            cv2.imwrite("1.jpg", img_1[0:y, x:x + w])  # name
            cv2.imwrite("2.jpg", img_1[y: int(y + (h / 2)), x:x + w])
            print("x+w:", x + w)
            print("width:", width)
            cv2.imwrite("3.jpg", img_2[int(h / 2):height_, x:x + w])  # name
            print("2-1")

            cv2.imwrite("4.jpg", img_2[0:int(h / 2), x:x + w])




    else:
        print("\n这种结果还没做出来！")

    for i in range(1, 2 * len(imagepath) + 1):
        #print('开始赋值：',i)
        new_imgpath.append(f"{i}.jpg")
        print("new_imgpath", new_imgpath)
        #new_imgpath.append(f"{i}.jpg")

    return new_imgpath

#将图片分成四个部分，或是两部分，有问题!!!
def split(location, image, x, y, w, h, width, height):
    #location中存储的顺序为上下左右四个部分，

    max_y = 0
    min_y = 0





    """
    if len(location) == 4:
        max_y = location[0][0][3][1]
        min_y = location[1][0][3][1]
        max_x = location[2][0][0][0]
        min_x = location[3][0][0][0]
        for i in range(0, len(location[0])):
            #首先两个对比取出较大值
            if location[0][i][3][1] > location[0][i][2][1]:
                large_value_y = location[0][i][3][1]
            else:
                large_value_y = location[0][i][2][1]
            if large_value_y > max_y:
                max_y = large_value_y

        for i in range(0, len(location[1])):
            # 首先两个对比取出较小值
            if location[1][i][0][1] < location[1][i][1][1]:
                smaller_value_y = location[1][i][0][1]
            else:
                smaller_value_y = location[1][i][1][1]
            if smaller_value_y < min_y:
                min_y = smaller_value_y

        for i in range(0, len(location[2])):
            # 首先两个对比取出较大值
            if location[2][i][2][0] > location[2][i][1][0]:
                large_value_x = location[2][i][2][0]
            else:
                large_value_x = location[2][i][1][0]
            if large_value_x > max_x:
                max_x = large_value_x

        for i in range(0, len(location[3])):
            # 首先两个对比取出较小值
            if location[3][i][0][0] < location[3][i][3][0]:
                smaller_value_x = location[3][i][0][0]
            else:
                smaller_value_x = location[3][i][3][0]
            if smaller_value_x < min_x:
                min_x = smaller_value_x

    region1 = image[0:max_y, x: x + w]
    region2 = image[min_y:height, x: x + w]
    region3 = image[y:y + h, 0:max_x]
    region4 = image[y:y + h, min_x:width]

    cv2.imwrite('region1',region1)
    cv2.imwrite('region2', region2)
    cv2.imwrite('region3', region3)
    cv2.imwrite('region4', region4)
    """

#图片旋转角度
def rotate_image(img_path):
    image_1 = cv2.imread(img_path[0])
    image_4 = cv2.imread(img_path[3])

    image_1 = cv2.transpose(image_1)    #转置图像
    image_1 = cv2.flip(image_1, 1)      #原图顺时针旋转90°
    cv2.imwrite('1.jpg', image_1)
    #cv2.imshow('1', image_1)
    #cv2.waitKey()

    image_4 = cv2.transpose(image_4)
    image_4 = cv2.flip(image_4, 1)
    cv2.imwrite('4.jpg', image_4)
    #cv2.imshow('4', image_4)
    #cv2.waitKey()
