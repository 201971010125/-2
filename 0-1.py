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


# =============================打印路径模块====================================
def path(position, num):
    endMidPath = []
    str1 = ''
    for i in range(len(profit[num])):
        endMidPath.append(position % 4)
        # print(position%4)
        position = int(position / 4)
    endMidPath.reverse()
    for i in range(len(endMidPath)):
        if i == 0:
            str1 = str1 + '开始选择--->'
            # print('从根节点开始')
        elif endMidPath[i] != 3:
            str1 = str1 + str(profit[num][i][endMidPath[i]]) + '--->'
            # print('第' + str(i) + '个背包选择' + str(profit[num][i][endMidPath[i]]))
        else:
            str1 = str1 + '不做选择--->'
            # print('第' + str(i) + '个背包不选任何元素')
    print(str1.strip('--->'))
    endPath.append(str1.strip('--->'))


# ===============================动态规划求解模块=================================
def dp(num, maxWeight):
    l = []
    profitArr = []
    profitArr = profit[num]
    weightArr = []
    weightArr = weight[num]
    for i in range(maxWeight + 1):
        l.append(0)
    for i in range(len(profit[num])):
        for j in range(maxWeight, -1, -1):
            for k in range(3):
                if j >= weightArr[i][k]:
                    l[j] = max(l[j], l[j - weightArr[i][k]] + profitArr[i][k])
    print('最大价值：' + str(l[maxWeight]))
    return str(l[maxWeight])

# ===============================贪心算法=================================
def dp(num, maxWeight):
    l = []
    profitArr = []
    profitArr = profit[num]
    weightArr = []
    weightArr = weight[num]
    for i in range(maxWeight + 1):
        l.append(0)
    for i in range(len(profit[num])):
        for j in range(maxWeight, -1, -1):
            for k in range(3):
                if j >= weightArr[i][k]:
                    l[j] = max(l[j], l[j - weightArr[i][k]] + profitArr[i][k])
    print('最大价值：' + str(l[maxWeight]))
    return str(l[maxWeight])

# =========================保存为txt=======================
def saveTxt(fileName, num, maxWeight, maxValue, sunTime):
    file = open('D:\study\python\pythonProject\实验二/查询结果.txt', 'a')
    file.write('文件名:\n' + fileName + '\n')
    file.write('第几组数据:\n' + str(num) + '\n')
    file.write('背包容量:\n' + str(maxWeight) + '\n')
    file.write('求解的最大价值:\n' + str(maxValue) + '\n')
    file.write('运行时间:\n' + str(sunTime) + 's\n')
    file.write('解向量:\n')
    for item in endPath:
        file.write(item + '\n')
    file.close()


# ========================主函数=======================
if __name__ == '__main__':
    fileName = getData()
    # 列表中包含若干个子列表，每个子列表包含一组数据的价值信息，每个子列表又包含若干个三元组列表，三元组列表记录了记录了该组数据每个项集
    print('数据读入完成！')
    print('价值信息：')
    for i in profit[0]:
        print(i)
    # 同价值信息，用于记录重量信息
    print('重量信息：')
    print(weight)
    # 列表包含若干子列表，一个子列表表示一组数据的价值-重量-价值重量比信息，子列表分为若干九元组。九元组记录了改组数据的价值-重量-价值重量比九条信息
    print('价值-重量-价值重量比信息：')
    print(prowei)
    while (True):
        x = int(input('请选择：\n1、画散点图\n2、非递增排序\n3、求解\n'))
        if x == 1:
            n = int(input('请选择对第几条数据做散点图'))
            show(n - 1)
            continue
        elif x == 2:
            n = int(input('请选择要对第几条数据进行排序'))
            sort(n - 1)
            continue
        elif x == 3:
            n = int(input('请选择算法\n1、回溯法\n2、动态规划算法\n3,贪心算法'))
            num = int(input('请输入要求解第几组数据'))
            maxWeight = int(input('请输入背包容纳的最大重量'))
            if n == 1:
                profit[num - 1] = [[0, 0, 0]] + profit[num - 1]
                weight[num - 1] = [[0, 0, 0]] + weight[num - 1]
                for i in profit[0]:
                    print(i)
                time1 = time.time()
                huisu(num - 1, maxWeight, 0, 0, 0, 0)
                time2 = time.time()
                endMax.sort(reverse=True)
                print('最大价值：' + str(endMax[0]))
                print('运行时间：' + str(time2 - time1) + 's')
                for item in range(len(pathList)):
                    if pathList[item] == endMax[0]:
                        path(item, num - 1)
                x = int(input('请选择：\n1.保存为txt\n2.不保存'))
                if x == 1:
                    saveTxt(fileName, num, maxWeight, endMax[0], time2 - time1)
                else:
                    pass
            elif n == 2:
                time1 = time.time()
                maxNum = dp(num - 1, maxWeight)
                time2 = time.time()
                print('运行时间：' + str(time2 - time1) + 's')
                x = int(input('请选择：\n1.保存为txt\n2.不保存'))
                if x == 1:
                    saveTxt(fileName, num, maxWeight, maxNum, time2 - time1)
            elif n == 3:
                    time1 = time.time()
                    maxNum = dp(num - 1, maxWeight)
                    time2 = time.time()
                    print('运行时间：' + str(time2 - time1) + 's')
                    x = int(input('请选择：\n1.保存为txt\n2.不保存'))
                    if x == 1:
                        saveTxt(fileName, num, maxWeight, maxNum, time2 - time1)

                else:
                    pass
        else:
            print('输入有误，请重新输入！')
            continue
