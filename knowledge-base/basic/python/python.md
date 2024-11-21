anaconda -- lauch Jupter
![[Pasted image 20240830104854.png]]

# type
type(a)
检查类型

# String

倒序
![[Pasted image 20240831092722.png|263]]

![[Pasted image 20240831094656.png|400]]

![[Pasted image 20240831094618.png|600]]
![[Pasted image 20240831095840.png|500]]

# List

append, pop


>[!note]+ List, Set, Dictionary, Tuple
[1,2,3]
{1,2,3}
{'key1':1, 'key2':2}
(1,2,3)

# 文件读写
```python
with open('a.txt', mode='a+') as myfile:
    myfile.writelines('are u ok\n')
    myfile.seek(0)
    print(myfile.read())
```
# statement
## if else
```python
a=3
if a==1:
    print('one')
elif a==2:
    print('two')
else:
    print('other')
```
## for
```python
words = ['Tom','Tim','Johnson']
for word in words:
    print(word)
```

String can be iterate as list also

tupple upacking
```python
tupLst = [(1,2),(3,4)]
for a,b in tupLst:
    print(f'a={a} b={b}')

# result
# a=1 b=2
# a=3 b=4
```

continue break pass(do nothing as a place holder)

## range
range(0,11,2)  -- 2 is step
list(range(10))
![[Pasted image 20240831191304.png|275]]
## enumerate zip
```python
myMap = {'key1':'Tom','key2':'Jason'}
for key, value in enumerate(myMap):
    print(f'key={key}, value={value}')
```

![[Pasted image 20240831191642.png|375]]
## check a word in a list or is the key of dictionary (in)
(0,'a') in tupLst
--output True

## random
```python
from random import *
lst = list(range(10))
print(lst)
shuffle(lst)
print(lst)

randint(0,2)
```

## list comprehension
![[Pasted image 20240831193419.png|725]]

## lamda
![[Pasted image 20240831212930.png|450]]
---
# function

```python
def sum(num1, num2):
    return num1 + num2
print(sum(5,6))
```

## \*args
传入n个参数，组成一个 args 的tupple
![[Pasted image 20240831205417.png|400]]

## \*\*kwargs

传入n个 xxx='aaa',xxx='bbb'组成一个kwargs的 dictionary
![[Pasted image 20240831210434.png|475]]

## global variable
![[Pasted image 20240831214702.png|450]]

# class

```python
class Circle:
    pi = 3.14
    
    def __init__(self, radius=1):
        self.radius = radius
        self.area = radius**2*Circle.pi
        
    def get_circonference(self):
        return self.radius*self.pi*2
    
circle = Circle(4)
print(circle.get_circonference())
print(circle.area)
```


## 继承
```python
class Animal:
    def __init__(self,name):
        print('ANIMAL CREATED')
        self.name= name

	def __str__(self):
	return f"name: {self.name}"
    
    def __len__(self):
        return 10    
        
    def who_am_i(self):
        print("I'm animal")
        
    def eating(self):
        print("I'm eating")
    
    def speak(self):
        raise NotImplementedError("Sub Class should implement it")

class Dog(Animal):
    def __init__(self,name):
        Animal.__init__(self,name)
        print("DOG CREATED")
    
    def who_am_i(self):
        print("I'm Dog")
        
    def speak(self):
        print(f"Woof!! My name is {self.name}")
        
class Cat(Animal):
    def __init__(self,name):
        Animal.__init__(self,name)
        print("CAT CREATED")
    
    def who_am_i(self):
        print("I'm Cat")
        
    def speak(self):
        print(f"Meow!! My name is {self.name}")

###################
dog = Dog("Tom")
cat = Cat("Jerry")

for pet in [dog,cat]:
    pet.speak()
```

# package module

package is folder name
module is file name


simple_main.py is a file in folder com.fansy.simple.mainpackage

we can import a class||function in simple_main.py 
we can import simple_main file also and use the file name to get others
```python
from com.fansy.simple.mymodule import sayHello  
from com.fansy.simple.mainpackage.simple_main import Person  
from com.fansy.simple.mainpackage import simple_main  
  
sayHello()  -- mymodule's function
person = Person("Frank")  --  
person.sayHi()  
  
person2 = simple_main.Person("Jack")  
person2.sayHi()

```

## check the py is imported or run directly
```python
if __name__ == "__main__":
    print("main")
else:
    print(f"main is imported: {__name__}")
```

## exception
```python
try:
    result = add(100,100)
except TypeError:
    print('add wrong!!')
    result = None
except:
    print('other wrong!!')
    result = None
else:
    print("No exception!!")
finally:
    print(result)
```


# unit test

pip insall pylint

```python
import unittest
from com.fansy.simple.mainpackage import simple_main


class MainTest(unittest.TestCase):
    def test_person(self):
        person = simple_main.Person("Johnson")
        self.assertEqual(person.name, "Johnson")


if __name__ == "__main__":
    unittest.main()
```


# Decorate
```python
def logDecorator(func):
    def wrapFun():
        print(f"func name is {func.__name__}")
        func()
        print("func run successfully!")
    return wrapFun;

@logDecorator
def sayHello():
    print("hello")
    
sayHello()
```


# yield
yield can store thing in a iterator and create things lator

```python
def gen():
    yield "hello"
    yield "your name is Tom"
    yield 100

for word in gen():
    print(word)

it = gen()
print(next(it))
```


list, string can also call iter function get its iterator
```python
lst = [1,2,3]
next(iter(lst))
```

# collections
## Counter
```python
from collections import Counter

lst = [12,12,25,24,48]
c = Counter(lst)

for item in c.items():
    print(type(item))
    print(f"key: {item[0]}, value: {item[1]}")
```

## defaultdict
```python
from collections import defaultdict
d = defaultdict(lambda: 0)
d['key1'] =100
d['key2']
```

## namedtupple
像一个class

```python
from collections import namedtuple

Dog = namedtuple('Dog', ['age','name'])
dog = Dog(5,'Sammy')
dog  

Dog(age=5, name='Sammy')
```

---
# number

```python
print (float(9)//2) #4.0
print(round(2.5)) #2 五舍六入
print(pow(2,10)) #1024

import math
print(math.ceil(2.8)) #3
```



# string

```python
word = "hello"
print(word[len(word)-1])
print(word.capitalize())
```

# list tuple map

```python
list1 = [1,2,3,4,5]
print(list1[0])

tuple1 = (1,2,3,4)
print(tuple1)

mp1 = {"key1":"value1","key2":"value2"}
print(mp1)
print(mp1.get("key2"))

set1 = {1,2,2,3}
print(set1)
```

# condition

```python
age = 20

if(age<18):
    print("child")
elif(age<30):
    print("young man")
else:
    print("adult")
```

# loop

```python
i = 1
sum2=0
while i<=100:
    sum2 = sum2 + i
    i = i + 1
print(sum2)

sum3=0
for ix in range(1,101):
    sum3 = sum3 + ix
print(sum3)
```

# module

```python
from sys import path
for item in path:
    print(item)
```



