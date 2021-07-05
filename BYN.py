import Data
import  pandas as pd
import random
import sklearn
import matplotlib.pyplot as plt
import seaborn as sns
from pgmpy.models import BayesianModel
from pgmpy.estimators import BayesianEstimator
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
trainseq=Data.Trainseq()#给出训练数据集donorsite附近七个碱基序列
testadd=Data.Testadd()
traintxt=Data.Traintxt()
testtxt=Data.Testtxt()
X_train=[[]]
for i in range(len(trainseq)):#添加正数据
    seq=list(trainseq[i][1])
    seq.append(1)
    X_train.append(seq)
for i in range(len(X_train)):#添加负数据
    m=random.randint(1,len(traintxt)-1)
    n=random.randint(3, (len(traintxt[m]) - 4))
    seq=list(traintxt[m][(n-3):(n-3+7)])
    if "n" in seq or "y" in seq or "r" in seq or "b" in seq:
        continue;
    else:
        seq.append(0)
        X_train.append(seq)
X_train=X_train[1:]
X_train=pd.DataFrame(X_train,columns=["一","二","三","四","五","六","七","是否位点"])
Y_train=X_train["是否位点"]
X_train=X_train.drop(["是否位点"],axis=1)
X_train=pd.get_dummies(X_train)
cor=X_train.corr()
sns.heatmap(cor)
plt.title("训练数据特征热图")
plt.savefig("BYN_train_heatmap.png")
plt.show()
train_feature=["三_a","四_g","五_g","六_t"]
X_train=X_train[train_feature]
X_train['donor']=Y_train
#测试数据的准备
X_test=[[]]
for i in range(len(testadd)):#添加正数据
    add=testadd[i]
    seq=list(testtxt[add[0]][(add[1]-3):(add[1]-3+7)])
    seq.append(1)
    X_test.append(seq)
for i in range(len(X_test)):#添加负数据
    m=random.randint(1,len(testtxt)-1)
    n=random.randint(3, (len(testtxt[m]) - 4))
    seq=list(testtxt[m][(n-3):(n-3+7)])
    if "n" in seq or "y" in seq or "r" in seq or "b" in seq:
        continue;
    else:
        seq.append(0)
        X_test.append(seq)
X_test=X_test[1:]
X_test=pd.DataFrame(X_test,columns=["一","二","三","四","五","六","七","是否位点"])
Y_test=X_test["是否位点"]
X_test=X_test.drop(["是否位点"],axis=1)
X_test=pd.get_dummies(X_test)
cor=X_test.corr()
sns.heatmap(cor)
plt.title("测试数据特征热图")
plt.savefig("BYN_test_heatmap.png")
plt.show()
test_feature=["三_a","四_g","五_g","六_t"]
X_test=X_test[test_feature]
#数据打乱
X_train,Y_train= sklearn.utils.shuffle(X_train,Y_train)
X_test,Y_test= sklearn.utils.shuffle(X_test,Y_test)
model = BayesianModel([('三_a', 'donor'), ('四_g', 'donor'),('五_g','donor'),('六_t','donor')])
model.fit(X_train, estimator=BayesianEstimator, prior_type="BDeu")
#模型预测
Y_predict = model.predict(X_test)
pre=Y_predict.values
pre=pre.tolist()
test=Y_test
test=test.tolist()
TP,FP,TN,FN=0,0,0,0
for i in range(len(pre)):
    if pre[i][0]==1 and test[i]==1:
        TP+=1
    elif pre[i][0]==1 and test[i]==0:
        FP+=1
    elif pre[i][0] == 0 and test[i] == 0:
        TN+=1
    elif pre[i][0] == 0 and test[i] == 1:
        FN+=1
Sn = TP / (TP + FN)
Sp = TP / (TP + FP)



