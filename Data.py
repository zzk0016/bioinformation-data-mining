import os
import re
path1="C:/Users/12849/Desktop/PYTHON/sjwj/dataset/trainset"#训练数据集文件夹地址
path2="C:/Users/12849/Desktop/PYTHON/sjwj/dataset/testset"#测试数据集文件夹地址
files1=os.listdir(path1)
files2=os.listdir(path2)

def Trainseq():
    txts1=[]
    for file in files1:  # 循环读取文件夹下所有文件
        position = path1 + '/' + file
        with open(position, "r", encoding='utf8') as f:
            data = f.read()
            txts1.append(data)
    donorseq = [[]]  # 地址矩阵包括两列，一列是txts编号，一列是位点位置
    for j in range(len(txts1)):#读取位置
        kuohao = re.search(r"\(", txts1[j]).span()
        str = txts1[j][kuohao[0]:]
        position = re.findall(r"\d+", str)
        for i in range(len(position)):
            if (i % 2) == 0 and i!=(len(position)-2):  # 位置为一对
                co = [j]
                donorseqsite = int(position[i+1]) - 1  # fasta中从1开始计位置,需要减一
                donorseqsite = donorseqsite - 3  # 前移三个碱基
                co.append(donorseqsite)
                donorseq.append(co)
    donorseq = donorseq[1:]#除去空的第一行
    for j in range(len(txts1)):  # 除去序列文件换行符和头两行
        avg = 0
        for i in range(len(txts1[j])):
            if txts1[j][i] == "\n":
                avg += 1
            if avg == 2:  # 此时i为第二行末尾
                txts1[j] = txts1[j][i + 1:]  # txts为从第三行开始的部分
                txts1[j] = txts1[j].replace("\n", "")  # 除去全部换行符
                break
    for j in range(len(donorseq)):  # 将donorseq中位置一列转换为对应的七个碱基序列
        txt = txts1[donorseq[j][0]]
        seq = txt[donorseq[j][1]:(donorseq[j][1] + 7)]
        donorseq[j][1] = seq.lower()
    return donorseq

def Testadd():
    txts2=[]
    for file in files2:  # 循环读取文件夹下所有文件
        position = path2 + '/' + file
        with open(position, "r", encoding='utf8') as f:
            data = f.read()
            txts2.append(data)
    address = [[]]  # 地址矩阵包括两列，一列是txts编号，一列是位点位置
    for j in range(len(txts2)):#读取位置
        kuohao = re.search(r"\(", txts2[j]).span()
        str = txts2[j][kuohao[0]:]
        position = re.findall(r"\d+", str)
        for i in range(len(position)):
            if (i % 2) == 0 and i!=(len(position)-2):  # 位置为一对
                co = [j]
                donorseqsite = int(position[i+1]) - 1  # fasta中从1开始计位置,需要减一
                co.append(donorseqsite)
                address.append(co)
    address = address[1:]#除去空的第一行
    return address

def Traintxt():
    txts1=[]
    for file in files1:  # 循环读取文件夹下所有文件
        position = path1 + '/' + file
        with open(position, "r", encoding='utf8') as f:
            data = f.read()
            txts1.append(data)
    for j in range(len(txts1)):  # 除去序列文件换行符和头两行
        avg = 0
        for i in range(len(txts1[j])):
            if txts1[j][i] == "\n":
                avg += 1
            if avg == 2:  # 此时i为第二行末尾
                txts1[j] = txts1[j][i + 1:]  # txts为从第三行开始的部分
                txts1[j] = txts1[j].replace("\n", "")  # 除去全部换行符
                txts1[j]=txts1[j].lower()
                break
    return txts1

def Testtxt():
    txts2=[]
    for file in files2:  # 循环读取文件夹下所有文件
        position = path2 + '/' + file
        with open(position, "r", encoding='utf8') as f:
            data = f.read()
            txts2.append(data)
    for j in range(len(txts2)):  # 除去序列文件换行符和头两行
        avg = 0
        for i in range(len(txts2[j])):
            if txts2[j][i] == "\n":
                avg += 1
            if avg == 2:  # 此时i为第二行末尾
                txts2[j] = txts2[j][i + 1:]  # txts为从第三行开始的部分
                txts2[j] = txts2[j].replace("\n", "")  # 除去全部换行符
                txts2[j]=txts2[j].lower()
                break
    return txts2
