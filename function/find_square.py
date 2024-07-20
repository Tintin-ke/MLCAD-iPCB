# -*- coding:utf-8 -*-
import cv2
import numpy as np
from function import whether_contain_information as wci
from PIL import Image
from function import preprocessing

def auto_(img_path, type, chip_name):
    #image = cv2.imread('16.png')
    image = cv2.imread(img_path)

    # 灰度图
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 二值化
    ret, thresh = cv2.threshold(img, 230, 255, cv2.THRESH_BINARY_INV)

    # cv2.findContours() 函数来查找物体轮廓
    #   cv2.RETR_EXTERNAL 只检测外轮廓
    # 	cv2.CHAIN_APPROX_SIMPLE 压缩水平方向 ，垂直方向，对角线方向的元素，只保留该方向的终点坐标，例如一个矩形轮廓只需要4个点来保存轮廓信息
    # 返回两个值，一个是轮廓本身，一个是每条轮廓对应的属性
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    dot = []  # 用来保存所有轮廓返回的坐标点。
    for c in contours:
        # 找到边界坐标
        min_list = []  # 保存单个轮廓的信息，x,y,w,h,area。 x,y 为起始点坐标
        x, y, w, h = cv2.boundingRect(c)  # 计算点集最外面的矩形边界
        min_list.append(x)
        min_list.append(y)
        min_list.append(w)
        min_list.append(h)
        min_list.append(w * h)  # 把轮廓面积也添加到 dot 中
        dot.append(min_list)

    # 找出最大矩形的 x,y,w,h,area
    max_area = dot[0][4]  # 把第一个矩形面积当作最大矩形面积
    for inlist in dot:
        area = inlist[4]
        if area >= max_area:
            x = inlist[0]
            y = inlist[1]
            w = inlist[2]
            h = inlist[3]
            max_area = area
    # 在原图上画出最大的矩形

    #print(dot[0])
    #print(dot[1])
    #print(dot[2])
    #print(dot[3])

    #ori_image = image
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)

    # cv2.namedWindow('img',cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('img', 1000,900)
    # cv2.imshow('img',image)
    cv2.imwrite('square.jpg', image)
    #img = cv2.line(image, (0, 0), (500, 500), (255, 0, 0), 3)
    cv2.waitKey(0)

    # 截图
    # from PIL import Image
    # img = Image.open('64.jpg')
    # 距离图片左边界距离x， 距离图片上边界距离y，距离图片左边界距离+裁剪框宽度x+w，距离图片上边界距离+裁剪框高度y+h
    # region = img.crop((x, y, x + w, y + h))
    # region.save('result.jpg')


    # 如果图片中存在芯片的名字，实现识别芯片的名字，然后将这一部分从图片中删除
    name = []
    ori_image = cv2.imread(img_path)
    midpoint = (x + (w / 2), y + (h / 2))  # 图片中心点
    image_withoutname = preprocessing.find_name(midpoint, ori_image, name)

    #if name[0] == '':
    #    print("芯片没有名字")
    #else:
    #    print("芯片名字：", name[0])
    #    chip_name.append(name[0])


    #ori_image = cv2.imread(img_path)
    # 获取图片的宽和高
    size = image.shape
    width = size[1]  # 宽度
    height = size[0]  # 高度
    channels = size[2]
    print(size)
    print('图片的宽：', width)
    print('图片的高：', height)
    print('图片的通道：', channels)

    print('\n矩形的宽：', w)
    print('矩形的高：', h)

    '''
    #判断这个图片是两排引脚的还是四排引脚的，三排引脚与四排引脚操作相同
    #首先截取图片，为矩形之外的四张图片
    region1 = ori_image[0:y, x:x + w]            #上
    region2 = ori_image[y + h:height, x:x + w]   #下
    region3 = ori_image[y: y + h, 0:x]           #左
    region4 = ori_image[y: y + h, x + w:width]   #右

    respond1 = wci.judge(region1)
    respond2 = wci.judge(region2)
    respond3 = wci.judge(region3)
    respond4 = wci.judge(region4)
    print(respond1)
    print(respond2)
    print(respond3)
    print(respond4)
    '''





    #对于不同的两排引脚和四排引脚的图片有不同的处理方式
    new_imgpath = []   #存放图片分割之后的图片名字
    up_down = 0

    #两排引脚,左右两排
    if type == 'two_side_leftright':
        print("two_side_leftright")

        #img = cv2.line(ori_image, (x, 0), (x, height), (0, 255, 0), 2)
        #img = cv2.line(img, (int(width / 2), 0), (int(width / 2), height), (0, 255, 0), 2)
        #img = cv2.line(img, (int(x + w), 0), (int(x + w), height), (0, 255, 0), 2)
        #cv2.imwrite("img1.jpg", img)

        result_1 = ori_image[0:height, 0:int(width / 2)]
        result_2 = ori_image[0:height, int(width / 2):width]
        # cv2.imshow("1", result_1)
        # cv2.imshow("2", result_2)
        # cv2.waitKey()
        cv2.imwrite("1.jpg", result_1)
        cv2.imwrite("2.jpg", result_2)
        new_imgpath.append('1.jpg')
        new_imgpath.append('2.jpg')
        up_down = 0

    #两派引脚，上下两排
    elif type == 'two_side_updown':
        print('two_side_updown')
        result_1 = ori_image[0: int(height / 2), 0:width]
        result_2 = ori_image[int(height / 2):height, 0:width]
        # cv2.imshow("1", result_1)
        # cv2.imshow("2", result_2)
        # cv2.waitKey()
        cv2.imwrite("1.jpg", result_1)
        cv2.imwrite("2.jpg", result_2)
        new_imgpath.append('1.jpg')
        new_imgpath.append('2.jpg')
        up_down = 1


    elif type == 'four_side':
        print('four_side')
        # 坐标分别为(x,y),(x+w,y+h); (x+w,y),(x,y+h)
        k1 = h / w  # 对角线的斜率   y=k1(x-x1)+y1，为向下的方向   x1,y1为对角线上的点   y1 = k1 * (x1 - x) + y
        k2 = (-h) / w  # 向上的方向    y=k2(x-x1)+y1    y2 = k2 * (x2 - x - w) + y

        point_x = []  # 顺序为 ↘ ↗ ，对角线与边界的的交点共有4个，每一个交点都有三种可能↘↗
        point_y = []
        point = []

        y0 = k1 * (0 - x - w / 2) + y + h / 2
        x0 = (0 - y - h / 2) / k1 + x + w / 2
        # x0 = (0 - y) / k1 + x
        if 0 <= y0 and y0 < height:
            point_x.append(0)
            point_y.append(y0)
            point.append((0, y0))
        else:
            point_y.append(0)
            point_x.append(x0)
            point.append((x0, 0))

        y1 = k1 * (width - x - w / 2) + y + h / 2
        x1 = (height - y - h / 2) / k1 + x + w / 2
        if 0 <= y1 and y1 < height:
            point_x.append(width)
            point_y.append(y1)
            point.append((width, y1))
        else:
            point_y.append(height)
            point_x.append(x1)
            point.append((x1, height))

        y2 = k2 * (0 - x - w / 2) + y + h / 2
        x2 = (height - y - h / 2) / k2 + x + w / 2
        if 0 <= y2 and y2 < height:
            point_x.append(0)
            point_y.append(y2)
            point.append((0, y2))
        else:
            point_y.append(height)
            point_x.append(x2)
            point.append((x2, height))

        y3 = k2 * (width - x - w / 2) + y + h / 2
        x3 = (0 - y - h / 2) / k2 + w / 2 + x
        if 0 <= y3 and y3 < height:
            point_x.append(width)
            point_y.append(y3)
            point.append((width, y3))
        else:
            point_y.append(0)
            point_x.append(x3)
            point.append((x3, 0))
        print('point:')
        print(point)

        # 四块mask需要分成不同的情况
        # 第一种情形，需要选取的截取点为
        situation_1 = [[point[0], (0, 0), (x + (w / 2), y + (h / 2)), (width, 0), point[3]],
                       [point[0], (x + (w / 2), y + (h / 2)), point[2]],
                       [point[1], (x + (w / 2), y + (h / 2)), point[3]],
                       [point[1], (x + (w / 2), y + (h / 2)), point[2], (0, height), (width, height)]]
        situation_2 = [[point[0], (x + (w / 2), y + (h / 2)), point[3]],
                       [point[0], (0, 0), (0, height), point[2], (x + (w / 2), y + (h / 2))],
                       [point[1], (x + (w / 2), y + (h / 2)), point[3], (width, 0), (width, height)],
                       [point[1], (x + (w / 2), y + (h / 2)), point[2]]]

        situation_1 = [[point[0], (0, height), (width, height), point[3], (x + (w / 2), y + (h / 2))],
                       [point[0], (0, 0), (width, 0), (width, height), (0, height), point[2],
                        (x + (w / 2), y + (h / 2))],
                       [point[1], (width, height), (0, height), (0, 0), (width, 0), point[3],
                        (x + (w / 2), y + (h / 2))],
                       [point[1], (x + (w / 2), y + (h / 2)), point[2], (0, 0), (width, 0)]]
        situation_2 = [
            [point[0], (x + (w / 2), y + (h / 2)), point[3], (width, 0), (width, height), (0, height), (0, 0)],
            [point[0], (x + (w / 2), y + (h / 2)), point[2], (width, height), (width, 0)],
            [point[1], (x + (w / 2), y + (h / 2)), point[3], (0, 0), (0, height)],
            [point[1], (x + (w / 2), y + (h / 2)), point[2], (0, height), (0, 0), (width, 0), (width, height)]]
        # print(situation_1)
        # situation_1.append()

        # 截取四块图片，顺序为（0，3）、（0，2）、（1，3）、（1，2）

        for i in range(1, 5):
            print(i)
            # mask = np.zeros(size, dtype=np.uint8)
            # 输入点的坐标
            # 这里需要判断以下是属于什么情形
            if 0 < point_y[i - 1] < height:
                roi_corners = np.array([situation_1[i - 1]], dtype=np.int32)
            else:
                roi_corners = np.array([situation_2[i - 1]], dtype=np.int32)
            # roi_corners = np.array([situation_2[1]], dtype=np.int32)
            # channel_count = channels
            # ignore_mask_color = (255,) * channel_count
            # 创建mask层，掩模图像
            masked_image = ori_image.copy()
            # ori_image.copyTo(masked_image)
            # cv2.imshow("ori",ori_image)
            # cv2.imshow("source", masked_image)
            # cv2.waitKey()
            cv2.fillPoly(masked_image, roi_corners, (255, 255, 255))  # 多个多边形填充
            # 为每个像素进行与操作，除mask区域外，全为0
            # masked_image = cv2.bitwise_and(ori_image, mask)
            # masked_image = mask
            # cv2.imshow(f"{i}", masked_image)
            # cv2.waitKey()

            # 截图操作
            if i == 1:
                masked_image = masked_image[0:int(y + (h / 2)), x:x + w]
            elif i == 2:
                masked_image = masked_image[y:y + h, 0:int(x + (w / 2))]
            elif i == 3:
                masked_image = masked_image[y:y + h, int(x + (w / 2)):width]
            elif i == 4:
                masked_image = masked_image[int(y + (h / 2)):height, x:x + w]
            new_imgpath.append(f"{i}.jpg")
            cv2.imwrite(f"{i}.jpg", masked_image)


    elif type == 'BGA':
        print('BGA')

    """
    #两排引脚,左右两排
    if respond1 == 0 and respond2 == 0:
        result_1 = ori_image[0:height, 0:int(width / 2)]
        result_2 = ori_image[0:height, int(width / 2):width]
        #cv2.imshow("1", result_1)
        #cv2.imshow("2", result_2)
        #cv2.waitKey()
        cv2.imwrite("1.jpg", result_1)
        cv2.imwrite("2.jpg", result_2)
        new_imgpath.append('1.jpg')
        new_imgpath.append('2.jpg')
        up_down = 0

    #两排引脚，方向不同，上下两排
    elif respond3 == 0 and respond4 == 0:
        result_1 = ori_image[0: int(height / 2), 0:width]
        result_2 = ori_image[int(height / 2):height, 0:width]
        #cv2.imshow("1", result_1)
        #cv2.imshow("2", result_2)
        #cv2.waitKey()
        cv2.imwrite("1.jpg", result_1)
        cv2.imwrite("2.jpg", result_2)
        new_imgpath.append('1.jpg')
        new_imgpath.append('2.jpg')
        up_down = 1

    #剩下的情况，都为else
    else:
        # 坐标分别为(x,y),(x+w,y+h); (x+w,y),(x,y+h)
        k1 = h / w  # 对角线的斜率   y=k1(x-x1)+y1，为向下的方向   x1,y1为对角线上的点   y1 = k1 * (x1 - x) + y
        k2 = (-h) / w  # 向上的方向    y=k2(x-x1)+y1    y2 = k2 * (x2 - x - w) + y

        point_x = []  # 顺序为 ↘ ↗ ，对角线与边界的的交点共有4个，每一个交点都有三种可能↘↗
        point_y = []
        point = []

        y0 = k1 * (0 - x - w / 2) + y + h / 2
        x0 = (0 - y - h / 2) / k1 + x + w / 2
        # x0 = (0 - y) / k1 + x
        if 0 <= y0 and y0 < height:
            point_x.append(0)
            point_y.append(y0)
            point.append((0, y0))
        else:
            point_y.append(0)
            point_x.append(x0)
            point.append((x0, 0))

        y1 = k1 * (width - x - w / 2) + y + h / 2
        x1 = (height - y - h / 2) / k1 + x + w / 2
        if 0 <= y1 and y1 < height:
            point_x.append(width)
            point_y.append(y1)
            point.append((width, y1))
        else:
            point_y.append(height)
            point_x.append(x1)
            point.append((x1, height))

        y2 = k2 * (0 - x - w / 2) + y + h / 2
        x2 = (height - y - h / 2) / k2 + x + w / 2
        if 0 <= y2 and y2 < height:
            point_x.append(0)
            point_y.append(y2)
            point.append((0, y2))
        else:
            point_y.append(height)
            point_x.append(x2)
            point.append((x2, height))

        y3 = k2 * (width - x - w / 2) + y + h / 2
        x3 = (0 - y - h / 2) / k2 + w / 2 + x
        if 0 <= y3 and y3 < height:
            point_x.append(width)
            point_y.append(y3)
            point.append((width, y3))
        else:
            point_y.append(0)
            point_x.append(x3)
            point.append((x3, 0))
        print('point:')
        print(point)

        # 四块mask需要分成不同的情况
        # 第一种情形，需要选取的截取点为
        situation_1 = [[point[0], (0, 0), (x + (w / 2), y + (h / 2)), (width, 0), point[3]],
                       [point[0], (x + (w / 2), y + (h / 2)), point[2]],
                       [point[1], (x + (w / 2), y + (h / 2)), point[3]],
                       [point[1], (x + (w / 2), y + (h / 2)), point[2], (0, height), (width, height)]]
        situation_2 = [[point[0], (x + (w / 2), y + (h / 2)), point[3]],
                       [point[0], (0, 0), (0, height), point[2], (x + (w / 2), y + (h / 2))],
                       [point[1], (x + (w / 2), y + (h / 2)), point[3], (width, 0), (width, height)],
                       [point[1], (x + (w / 2), y + (h / 2)), point[2]]]

        situation_1 = [[point[0], (0, height), (width, height), point[3], (x + (w / 2), y + (h / 2))],
                       [point[0], (0, 0), (width, 0), (width, height), (0, height), point[2], (x + (w / 2), y + (h / 2))],
                       [point[1], (width, height), (0, height), (0, 0), (width, 0), point[3], (x + (w / 2), y + (h / 2))],
                       [point[1], (x + (w / 2), y + (h / 2)), point[2], (0, 0), (width, 0)]]
        situation_2 = [[point[0], (x + (w / 2), y + (h / 2)), point[3], (width, 0), (width, height), (0, height), (0 , 0)],
                       [point[0], (x + (w / 2), y + (h / 2)), point[2], (width,  height), (width, 0)],
                       [point[1], (x + (w / 2), y + (h / 2)), point[3], (0, 0), (0, height)],
                       [point[1], (x + (w / 2), y + (h / 2)), point[2], (0, height), (0, 0), (width, 0), (width, height)]]
        # print(situation_1)
        # situation_1.append()

        # 截取四块图片，顺序为（0，3）、（0，2）、（1，3）、（1，2）

        for i in range(1, 5):
            print(i)
            #mask = np.zeros(size, dtype=np.uint8)
            # 输入点的坐标
            # 这里需要判断以下是属于什么情形
            if 0 < point_y[i - 1] < height:
                roi_corners = np.array([situation_1[i - 1]], dtype=np.int32)
            else:
                roi_corners = np.array([situation_2[i - 1]], dtype=np.int32)
            # roi_corners = np.array([situation_2[1]], dtype=np.int32)
            #channel_count = channels
            #ignore_mask_color = (255,) * channel_count
            # 创建mask层，掩模图像
            masked_image = ori_image.copy()
            #ori_image.copyTo(masked_image)
            #cv2.imshow("ori",ori_image)
            #cv2.imshow("source", masked_image)
            #cv2.waitKey()
            cv2.fillPoly(masked_image, roi_corners, (255, 255, 255))      #多个多边形填充
            # 为每个像素进行与操作，除mask区域外，全为0
            #masked_image = cv2.bitwise_and(ori_image, mask)
            #masked_image = mask
            #cv2.imshow(f"{i}", masked_image)
            #cv2.waitKey()

            #截图操作
            if i == 1:
                masked_image = masked_image[0:int(y + (h / 2)),x:x + w]
            elif i == 2:
                masked_image = masked_image[y:y + h, 0:int(x + (w / 2))]
            elif i == 3:
                masked_image = masked_image[y:y + h, int(x + (w / 2)):width]
            elif i == 4:
                masked_image = masked_image[int(y + (h / 2)):height, x:x + w]
            new_imgpath.append(f"{i}.jpg")
            cv2.imwrite(f"{i}.jpg", masked_image)
    """

    #对1和4顺时针旋转90°
    #if len(new_imgpath) == 4:
    #    print('new_img_path:', new_imgpath)
    #    preprocessing.rotate_image(new_imgpath)

    image_path = []
    #print('new_imgpath:', new_imgpath)
    image_path = preprocessing.split_numandname(x, y, w, h, width, height, new_imgpath, up_down)[:]
    print('image_path', image_path)


    return image_path   #返回分割之后的图像路径
    #return new_imgpath
#chip_name = ''
#auto_('C:/Users/gaosh/Desktop/chip/0111.png', chip_name)