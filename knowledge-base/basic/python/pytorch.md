# numpy
build np array

```python
import numpy as np
arr = np.array([[5,10,15],[20,25,30],[35,40,45]])
arr2 = np.array(range(0,10))
arr.shape
```

## select a range of np array
[start:end:step]

```python

array([[ 5, 10, 15],
       [20, 25, 30]])

arr[:2,1:]

#output
array([[10, 15],
       [25, 30]])
```


## broadcase
```python
arr>20

#output
array([[False, False, False],
       [False,  True,  True],
       [ True,  True,  True]])

arr[arr>25]
#output
array([30, 35, 40, 45])
```

## sum rows columns
axis=0 sum by row
axis=1 sum by column

![[Pasted image 20240907200140.png|475]]


## generate matrixs
np.arange(9).reshape(3,3)
array([[0, 1, 2],
       [3, 4, 5],
       [6, 7, 8]])

np.eye(3)
array([[1., 0., 0.],
       [0., 1., 0.],
       [0., 0., 1.]])

np.random.randn(25).reshape(5,5)
array([[ 1.01759906, -1.37630242, -0.52189072,  1.49589861,  0.39343685],
       [-0.63067222, -1.69252685, -0.92267584,  0.6100594 ,  0.76127473],
       [-2.16502382, -0.72028519, -0.12736635,  1.79848195,  0.4819558 ],
       [-0.83446886,  0.59556591, -1.13219992, -0.38858924,  0.09827136],
       [ 2.83581351,  0.24337261,  0.05126133, -0.78186919,  0.78654376]])

np.linspace(0,1,20) -- 20 numbers between 0->1
array([0.        , 0.05263158, 0.10526316, 0.15789474, 0.21052632,
       0.26315789, 0.31578947, 0.36842105, 0.42105263, 0.47368421,
       0.52631579, 0.57894737, 0.63157895, 0.68421053, 0.73684211,
       0.78947368, 0.84210526, 0.89473684, 0.94736842, 1.        ])

## Get sub matrixs or value from a matrics
array([[ 1,  2,  3,  4,  5],
       [ 6,  7,  8,  9, 10],
       [11, 12, 13, 14, 15],
       [16, 17, 18, 19, 20],
       [21, 22, 23, 24, 25]])

mat[3,4]
20

mat[-1,:] -- -1 拿最后一行， ：拿所有
array([21, 22, 23, 24, 25])

## matrix sum std
sum 求和
std 标准差

# Pandas
## Series
![[Pasted image 20240908082330.png]]

## DataFrame

generate DF

index first, column second
![[Pasted image 20240908084740.png|500]]

find a sub frame
![[Pasted image 20240908084848.png|475]]
```python
df.iloc[0]['marital'] #iloc find by numindex
```

add new column, new row
![[Pasted image 20240908084928.png|425]]

drop column, index
![[Pasted image 20240908085030.png|425]]

根据条件筛选
```python
df[(df['b']>15) | (df['e']==15)]
```
![[Pasted image 20240908091743.png|400]]

重设index
df.reset_index(inplace=True)
df.set_index(df['f']）用f列的数据来做index

df.drop(columns='index',inplace=True) 删除一列index
![[Pasted image 20240910073753.png|325]]


```python
df['job'].value_counts() # check how many person for each job
```


```python
married = df['marital'].value_counts()['married']
married = len(df[df['mrital']=='married'])

total = len(df)


```
### group
```python
data1 = 'APPLE GOOGLE APPLE GOOGLE'.split()
data2 = [100,50,500,80]

dictionary1 = {'Comp':data1,'Money':data2}
df = pd.DataFrame(data=dictionary1)
df

df.groupby('Company').mean()
```
![[Pasted image 20240908093720.png|400]]

df2 = df.groupby('Comp').describe().transpose() --获取所有group之后的方法
的结果


## other functions
![[Pasted image 20240908095913.png|173]]
apply a function
```python
def do(num):
    return (num -100)*2

my_df2.apply(do)
```

unique value of a series
my_df2['a'].unique()

sort
my_df2.sort_values(by='a',ascending=False)


## read & write
my_df2.to_excel('output.xlsx',sheet_name='my_sheet',index=False)
pd.read_excel('output.xlsx',sheet_name='my_sheet')

# torch tensor
t3 = tor.randint(high=10,low=1,size=(5,5))

tensor.type(torch.int64) 改变tensor数据类型

向量得到二维点积
```python
a = torch.tensor([[1, 2, 3], 
                  [4, 5, 6]])

b = torch.tensor([[1, 2], 
                  [3, 4], 
                  [5, 6]])
```

a.mm(b)
a @ b
是同一个意思

a的第一行 乘 b第一列 22， a的第一行 乘 b第二列 28
a的第二行 乘 b第一列 49， a的第二行 乘 b第二列 64

结果
```python
tensor([[22., 28.],
        [49., 64.]])
```


# torch 梯度下降模型
```python
import torch  
import matplotlib.pyplot as plt  
import torch.nn as nn  
  
x = torch.linspace(1, 50, 50).reshape(-1, 1)  
torch.manual_seed(71)  
e = torch.randint(-8, 9, (50, 1))  
y = x * 3 + e  
  
  
class Model(nn.Module):  
def __init__(self, in_features, out_features):  
super().__init__()  
self.linear = nn.Linear(in_features, out_features)  
  
def forward(self, x):  
return self.linear(x)  
  
  
def draw_predict(_model, axis_x, color):  
weight = _model.linear.weight.item()  
bias = _model.linear.bias.item()  
predict_y = axis_x * weight + bias  
plt.plot(axis_x.numpy(), predict_y.numpy(), color)  
  
  
model = Model(1, 1) ##模型的输入的维度 输出的维度  
  
criteria = nn.MSELoss()  
optimizer = torch.optim.SGD(model.parameters(), lr=0.001)  
  
epochs = 20  
draw_predict(model, x, 'y')  
for i in range(epochs):  
y_pre = model.forward(x)  
loss = criteria(y_pre, y)  
print("epoch: ", i, " loss: ", loss.item())  
optimizer.zero_grad()  
loss.backward()  
optimizer.step()  
  
draw_predict(model, x, 'g')  
  
plt.scatter(x.numpy(), y.numpy())  
plt.show()
```

# torch data prepare

torch TensorDataset
```python
from torch.utils.data import TensorDataset, DataLoader  
import torch  
import pandas as pd  
raw = {  
'feature1': [5.1, 4.9, 4.7, 4.6, 5.0],  
'feature2': [3.5, 3.0, 3.2, 3.1, 3.6],  
'feature3': [1.4, 1.4, 1.3, 1.5, 1.4],  
'feature4': [0.2, 0.2, 0.2, 0.2, 0.3],  
'target': [0, 0, 0, 0, 1] # 假设目标标签是分类标签  
}  
  
df = pd.DataFrame(raw)  
print(df)  
data = df.drop('target',axis=1).values  
labels = df['target'].values  
  
iris = TensorDataset(torch.FloatTensor(data),torch.LongTensor(labels))  
  
  
iris_loader = DataLoader(iris, batch_size=2, shuffle=True)  
for i, data in enumerate(iris_loader):  
print(i)  
print(data)
```

sk_learn devided data
```python
from sklearn.model_selection import train_test_split  
import torch  
import pandas as pd  
raw = {  
'feature1': [5.1, 4.9, 4.7, 4.6, 5.0],  
'feature2': [3.5, 3.0, 3.2, 3.1, 3.6],  
'feature3': [1.4, 1.4, 1.3, 1.5, 1.4],  
'feature4': [0.2, 0.2, 0.2, 0.2, 0.3],  
'target': [0, 0, 0, 0, 1] # 假设目标标签是分类标签  
}  
  
df = pd.DataFrame(raw)  
train_X, test_X, train_y, test_y = train_test_split(df.drop('target',axis=1).values,  
df['target'].values, test_size=0.2,  
random_state=33)  
  
X_train = torch.FloatTensor(train_X)  
X_test = torch.FloatTensor(test_X)  
y_train = torch.LongTensor(train_y).reshape(-1, 1)  
y_test = torch.LongTensor(test_y).reshape(-1, 1)  
print(f"X_train:{X_train}")  
print(f"X_test:{X_test}")  
print(f"y_train:{y_train}")  
print(f"y_test:{y_test}")
``