import Data
import numpy as np
import pandas as pd
import math
import operator
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
trainseq=Data.Trainseq()
testadd=Data.Testadd()
testtxt=Data.Testtxt()

#计算位点的碱基概率,概率顺序为atcg
trainpro1=np.zeros(4)
trainpro2=np.zeros((6,16))
for i in range(len(trainseq)):
    seq=trainseq[i][1]#位点上游7个碱基
    if seq[0] == "a":
        trainpro1[0] += 1
    elif seq[0] == "t":
        trainpro1[1]+= 1
    elif seq[0] == "c":
        trainpro1[2]+=1
    elif seq[0] == "g":
        trainpro1[3]+=1
    for j in range(1,len(seq)):
        if seq[j-1]=="a" and seq[j]=="a":
            trainpro2[j-1][0]+=1
        elif seq[j-1]=="a" and seq[j]=="t":
            trainpro2[j-1][1]+=1
        elif seq[j-1]=="a" and seq[j]=="c":
            trainpro2[j-1][2]+=1
        elif seq[j-1]=="a" and seq[j]=="g":
            trainpro2[j-1][3] += 1
        elif seq[j-1]=="t" and seq[j]=="a":
            trainpro2[j-1][4] += 1
        elif seq[j-1]=="t" and seq[j]=="t":
            trainpro2[j-1][5] += 1
        elif seq[j-1]=="t" and seq[j]=="c":
            trainpro2[j-1][6] += 1
        elif seq[j-1]=="t" and seq[j]=="g":
            trainpro2[j-1][7] += 1
        elif seq[j-1]=="c" and seq[j]=="a":
            trainpro2[j-1][8] += 1
        elif seq[j-1]=="c" and seq[j]=="t":
            trainpro2[j-1][9] += 1
        elif seq[j-1]=="c" and seq[j]=="c":
            trainpro2[j-1][10] += 1
        elif seq[j-1]=="c" and seq[j]=="g":
            trainpro2[j-1][11] += 1
        elif seq[j-1]=="g" and seq[j]=="a":
            trainpro2[j-1][12] += 1
        elif seq[j-1]=="g" and seq[j]=="t":
            trainpro2[j-1][13] += 1
        elif seq[j-1]=="g" and seq[j]=="c":
            trainpro2[j-1][14] += 1
        elif seq[j-1]=="g" and seq[j]=="g":
            trainpro2[j-1][15] += 1
trainpro1=trainpro1/sum(trainpro1)#计算概率
for i in range(len(trainpro2)):
    for j in range(len(trainpro2[i])):
        if (j+1)%4==0 and j>0:#根据ppt四个为一组计算概率
            sum=trainpro2[i][j]+trainpro2[i][j-1]+trainpro2[i][j-2]+trainpro2[i][j-3]
            if sum!=0:
                trainpro2[i][j] = trainpro2[i][j] / sum
                trainpro2[i][j - 1] = trainpro2[i][j - 1] / sum
                trainpro2[i][j - 2] = trainpro2[i][j - 2] / sum
                trainpro2[i][j - 3] = trainpro2[i][j - 3] / sum

#计算背景碱基概率
backpro1=[0.262,0.272,0.231,0.236]
back=[0.299,0.234,0.187,0.28,
      0.188,0.309,0.222,0.28,
      0.311,0.322,0.293,0.0743,
      0.259,0.221,0.228,0.292]
backpro2=[[]]
for i in range(6):
    backpro2.append(back)
backpro2=backpro2[1:]
result=[[]]
for i in range(len(testtxt)):
    for j in range(3,(len(testtxt[i])-4)):
        seq=testtxt[i][(j-3):(j-3+7)]
        if "n" in seq or "y" in seq or "r" in seq or "b" in seq:
            continue;
        else:
            if seq[0] == "a":
                p1 = trainpro1[0]
            elif seq[0] == "t":
                p1 = trainpro1[1]
            elif seq[0] == "c":
                p1 = trainpro1[2]
            elif seq[0] == "g":
                p1 = trainpro1[3]
            p2_6 = [0] * 6
            for n in range(1, len(seq)):
                if seq[n - 1] == "a" and seq[n] == "a":
                    p2_6[n - 1] = trainpro2[n - 1][0]
                elif seq[n - 1] == "a" and seq[n] == "t":
                    p2_6[n - 1] = trainpro2[n - 1][1]
                elif seq[n - 1] == "a" and seq[n] == "c":
                    p2_6[n - 1] = trainpro2[n - 1][2]
                elif seq[n - 1] == "a" and seq[n] == "g":
                    p2_6[n - 1] = trainpro2[n - 1][3]
                elif seq[n - 1] == "t" and seq[n] == "a":
                    p2_6[n - 1] = trainpro2[n - 1][4]
                elif seq[n - 1] == "t" and seq[n] == "t":
                    p2_6[n - 1] = trainpro2[n - 1][5]
                elif seq[n - 1] == "t" and seq[n] == "c":
                    p2_6[n - 1] = trainpro2[n - 1][6]
                elif seq[n - 1] == "t" and seq[n] == "g":
                    p2_6[n - 1] = trainpro2[n - 1][7]
                elif seq[n - 1] == "c" and seq[n] == "a":
                    p2_6[n - 1] = trainpro2[n - 1][8]
                elif seq[n - 1] == "c" and seq[n] == "t":
                    p2_6[n - 1] = trainpro2[n - 1][9]
                elif seq[n - 1] == "c" and seq[n] == "c":
                    p2_6[n - 1] = trainpro2[n - 1][10]
                elif seq[n - 1] == "c" and seq[n] == "g":
                    p2_6[n - 1] = trainpro2[n - 1][11]
                elif seq[n - 1] == "g" and seq[n] == "a":
                    p2_6[n - 1] = trainpro2[n - 1][12]
                elif seq[n - 1] == "g" and seq[n] == "t":
                    p2_6[n - 1] = trainpro2[n - 1][13]
                elif seq[n - 1] == "g" and seq[n] == "c":
                    p2_6[n - 1] = trainpro2[n - 1][14]
                elif seq[n - 1] == "g" and seq[n] == "g":
                    p2_6[n - 1] = trainpro2[n - 1][15]
            P1 = p1 * p2_6[0] * p2_6[1] * p2_6[2] * p2_6[3] * p2_6[4] * p2_6[5]
            if seq[0] == "a":
                n1 = backpro1[0]
            elif seq[0] == "t":
                n1 = backpro1[1]
            elif seq[0] == "c":
                n1 = backpro1[2]
            elif seq[0] == "g":
                n1 = backpro1[3]
            n2_6 = [0] * 6
            for n in range(1, len(seq)):
                if seq[n - 1] == "a" and seq[n] == "a":
                    n2_6[n - 1] = backpro2[n - 1][0]
                elif seq[n - 1] == "a" and seq[n] == "t":
                    n2_6[n - 1] = backpro2[n - 1][1]
                elif seq[n - 1] == "a" and seq[n] == "c":
                    n2_6[n - 1] = backpro2[n - 1][2]
                elif seq[n - 1] == "a" and seq[n] == "g":
                    n2_6[n - 1] = backpro2[n - 1][3]
                elif seq[n - 1] == "t" and seq[n] == "a":
                    n2_6[n - 1] = backpro2[n - 1][4]
                elif seq[n - 1] == "t" and seq[n] == "t":
                    n2_6[n - 1] = backpro2[n - 1][5]
                elif seq[n - 1] == "t" and seq[n] == "c":
                    n2_6[n - 1] = backpro2[n - 1][6]
                elif seq[n - 1] == "t" and seq[n] == "g":
                    n2_6[n - 1] = backpro2[n - 1][7]
                elif seq[n - 1] == "c" and seq[n] == "a":
                    n2_6[n - 1] = backpro2[n - 1][8]
                elif seq[n - 1] == "c" and seq[n] == "t":
                    n2_6[n - 1] = backpro2[n - 1][9]
                elif seq[n - 1] == "c" and seq[n] == "c":
                    n2_6[n - 1] = backpro2[n - 1][10]
                elif seq[n - 1] == "c" and seq[n] == "g":
                    n2_6[n - 1] = backpro2[n - 1][11]
                elif seq[n - 1] == "g" and seq[n] == "a":
                    n2_6[n - 1] = backpro2[n - 1][12]
                elif seq[n - 1] == "g" and seq[n] == "t":
                    n2_6[n - 1] = backpro2[n - 1][13]
                elif seq[n - 1] == "g" and seq[n] == "c":
                    n2_6[n - 1] = backpro2[n - 1][14]
                elif seq[n - 1] == "g" and seq[n] == "g":
                    n2_6[n - 1] = backpro2[n - 1][15]
            N1 = n1 * n2_6[0] * n2_6[1] * n2_6[2] * n2_6[3] * n2_6[4] * n2_6[5]
            if (P1 / N1) == 0:
                S = 0
            else:
                S = math.log((P1 / N1), math.e)
                co=[i]
                co.append(j)
                co.append(S)
                result.append(co)
result=result[1:]
result=pd.DataFrame(result,columns=["文件号","位置","S值"])
TP=0
C=np.arange(2,6.5,0.5)
score=[[]]
for i in range(len(C)):
    res=result[result["S值"]>C[i]]
    res=res.drop("S值",axis=1)
    res=res.values
    res=res.tolist()
    TP=0
    for m in range(len(testadd)):
        for n in range(len(res)):
            if operator.eq(testadd[m],res[n]):
                TP+=1
    FP=len(res)-TP
    FN=len(testadd)-TP
    Sn=TP/(TP+FN)
    Sp=TP/(TP+FP)
    co=[Sn,Sp,C[i]]
    score.append(co)
score=score[1:]
score=pd.DataFrame(score,columns=["Sn","Sp","C"])
plt.plot(score["Sp"],score["Sn"],marker='^',markeredgecolor='black')
plt.title("Sp-Sn折线图")
plt.xlabel("Sp值")
plt.ylabel("Sn值")
plt.savefig("WAM_Sn_Sp.png")
plt.show()
plt.plot(score["C"],score["Sp"],marker='^',markeredgecolor='black')
plt.title("C-Sp折线图")
plt.xlabel("C阈值")
plt.ylabel("Sp值")
plt.savefig("WAM_C_Sp.png")
plt.show()
plt.plot(score["C"],score["Sn"],marker='^',markeredgecolor='black')
plt.title("C-Sn折线图")
plt.xlabel("C阈值")
plt.ylabel("Sn值")
plt.savefig("WAM_C_Sn.png")
plt.show()

