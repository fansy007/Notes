#basic #python
ndarray 多维数组类型
```python
import numpy as np
arr = np.array([1,2,3])
arr.ndim
```

属性
shape, ndim, size, dtype

arr.T 转置

# 构造方法
![[Pasted image 20251110094423.png]]
copy 输入ndarray
array 输入普通数组

# 切片
```python
arr = np.array([[1,2,3],[4,5,6],[7,8,9]])
arr[arr>5]
---
array([6, 7, 8, 9])


arr[2,:]
---
array([7, 8, 9])
```

两个矩阵做数学上的乘法应该用
a@b

# 常用操作
![[Pasted image 20251110103912.png]]

