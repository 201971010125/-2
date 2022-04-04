import numpy as np
import matplotlib.pyplot as plt
import time
import openpyxl

# =========================数据定义开始============================
# 三维列表，存放整个文件各组数据价值的列表，该列表分为若干子列表，每个子列表用于存储一组价值数据，每个子列表的数据又按照三个一组分为若干个列表
global profit
profit = []
# 三维列表，存放整个文件各组数据重量的列表，同profit
global weight
weight = []
# 三维列表，存放整个文件各组数据价值-重量-价值重量比的列表，该列表分为若干子列表，每个子列表用于存储一组价值-重量-价值重量比数据,每个子列表
# 的数据为一个九元组，包含三条价值数据-三条重量数据-三条价值重量比信息
global prowei
prowei = []
# 存放价值初始数据，即刚读入并且仅对结尾做了处理的字符串
global profitData
profitData = []
# 存放重量初始数据，即刚读入并且仅对结尾做了处理的字符串
global weightData
weightData = []
global endMax
endMax = []
global pathList
pathList = []
global endPath
endPath = []
# =========================数据定义结束============================


# =======================文件读取和处理函数=========================
def getData():
    # -------打开指定文件，读入数据-------
    fileName = str(input('请输入文件名'))
    file = open(fileName, 'r')
    line = file.readline()
    while (line):
        # 读入一行数据1
        line = file.readline()
        # 如果匹配到profit关键字，则读入下一行的价值信息
        if line.__contains__("profit"):
            # 去除结尾的换行符，逗号，原点，便于分割
            line = file.readline().strip('\n').strip('.').strip(',')
            # 将该行数据存入列表
            profitData.append(line)
        # 如果匹配到weight关键字，则读入下一行的重量信息
        elif line.__contains__("weight"):
            # 去除结尾的换行符，逗号，原点，便于分割
            line = file.readline().strip('\n').strip('.').strip(',')
            # 将该行数据存入列表
            weightData.append(line)
    # ------------数据读取完成---------------
    # ------------profitData存放初始价值信息---------------
    # ------------weightData存放初始重量信息---------------

    # 处理数据，外层遍历profitData和weightData的每一组数据，将profitData和weightData的数据进一步划分为三元组和九元组
    for group in range(len(profitData)):
        # 临时数据，价值三元组
        three_P_List = []
        # 临时数据，重量三元组
        three_W_List = []
        # 临时数据，价值重量比三元组
        three_PW_List = []
        # 存放一组价值数据
        group_P_List = []
        # 存放一组重量数据
        group_W_List = []
        # 存放一组价值+重量构成的数据
        group_PW_List = []
        # 临时变量，计数器
        n = 0

        # 将每一组价值/重量数据按照逗号分组,两个列表分别用于存放每一组价值/重量数据分组后的结果
        proList = str(profitData[group]).split(',')
        weiList = str(weightData[group]).split(',')

        # 内层循环遍历上述分组后的每一组数据，将每组数据按照三元组/九元组进行存储
        for p in range(len(proList)):
            # 将该组价值/重量/价值重量比数据的一个放入三元组列表
            three_P_List.append(int(proList[p]))
            three_W_List.append(int(weiList[p]))
            three_PW_List.append(int(proList[p]) / int(weiList[p]))
            # 三元组中数量+1
            n = n + 1
            # 如果三元组已有三条数据
            if n == 3:
                # 将价值/重量三元组放入该组列表
                group_P_List.append(three_P_List)
                group_W_List.append(three_W_List)
                # 构造九元组，并将价值-重量-价值重量比九元组放入该组列表
                group_PW_List.append(three_P_List + three_W_List + three_PW_List)
                # 将三个临时三元组/九元组变量置空，为下一次做准备
                three_P_List = []
                three_W_List = []
                three_PW_List = []
                # 计数器置0
                n = 0
        # 将内层循环处理完成的一组数据（列表）放入最终结果列表
        profit.append(group_P_List)
        weight.append(group_W_List)
        prowei.append(group_PW_List)
        global flagList
        flagList = profit
    return fileName


# ===========================绘制散点图函数开始===========================
def show(n):
    # 将初始数据的第n组按照逗号分割，作为存放(X,Y)坐标的列表
    pointXList = str(weightData[n]).split(',')
    pointYList = str(profitData[n]).split(',')
    # 设置X-Y轴表示的含义
    plt.xlabel = ('weight')
    plt.ylabel = ('profit')
    # 设置X-Y坐标轴的范围
    plt.xlim(0, 3000)
    plt.ylim(0, 3000)
    # 设置散点图点的颜色
    color = '#6c3466'
    # 设置点的大小
    area = np.pi * 1 ** 1
    # 绘制
    for point in range(len(pointXList)):
        plt.scatter(int(pointXList[point]), int(pointYList[point]), s=area, color=color)
    plt.show()


# ============================非递增排序函数开始===========================
def sort(n):
    # 将第n组数据按照第三项的价值重量比做非递增排序
    prowei[n].sort(key=lambda x: x[8], reverse=True)
    for item in prowei[n]:
        print(item)


# ============================回溯求解模块=================================
# ==========num:待求解数据下标  maxWeight ：背包最大容量 x y totalP当前已经访问的节点总价值 total : 总重量
def huisu(num, maxWeight, x, y, totalP, totalW):  # 访问一个节点   x,y 计算当前价值
    if y != 3:
        totalP = totalP + profit[num][x][y]
        totalW = totalW + weight[num][x][y]
    if x == len(profit[num]) - 1:
        # 总价值和总重量
        if totalW > maxWeight:
            # print(totalP)
            pathList.append(totalP)
            return 0
        else:
            endMax.append(totalP)
            pathList.append(totalP)
        return 0
    else:
        for i in range(4):
            huisu(num, maxWeight, x + 1, i, totalP, totalW)
    return 0


