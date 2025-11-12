#程序 #basic 
# Series
```python
s =pd.Series(['Jan','Feb','Mar'],index=[1,2,3],name='month')
---
1    Jan
2    Feb
3    Mar
Name: month, dtype: object

# 摘取部分index
s2 = pd.Series(s, index=[1,2])
---
1    Jan
2    Feb
Name: month, dtype: object

# 用dictinary创建
s3 = pd.Series({'1':'Mon','2':'Tues','3':'Wedn'},name='Week')
```

![[Pasted image 20251110110718.png]]
像ndarray一样可以用
s['index']
s[s>xxx]取值

044待续