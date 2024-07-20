import  numpy

def transfer(txts):    #将一维的列表转换成二维的
    print("当前列表为：")
    print(txts)

    name = []    #先声明两个空列表，一个为name，一个为num
    num = []
    for text in txts:
        if text.isdigit():      #判断是否是数字
            num.append(text)
        else:
            name.append(text)

    print("引脚名和引脚号分别为：")
    print(num)
    print(name)

    double_dimension = list(zip(num,name))   #生成一个二维的列表
    print("\n二维列表为：")
    print(double_dimension)

    return double_dimension