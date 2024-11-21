#basic
# 变量
a='123' // 等号两边不能空格 因为空格会把输误当作linux指令
unset a // 清空变量

全局变量，局部变量
export a='123' -- 全局，子shell也能拿到

env --查看当前bash的全局变量
set --局部变量

. hello.sh
source hello.sh -- shell的内置命令，仍然使用==当前shell执行==，局部变量仍然有效，其他指令会使用新的子shell

readonly a=5 --只读不可写

---
# 数组
[[#数组与Hash数组]]
```sh
#!/bin/bash
a=( 1 3 5 7 )
for value in ${a[@]};do
    echo $value
done
```
---
# 参数
./hello.sh var1

$n
$0 脚本名本身(不包含参数)  -- ./hello.sh
$1 ... $9 九个参数 -- var1($1)

$# 参数个数

---
$* 所有参数的一个字符串
$@ 所有参数数组

---
$? 最后执行的命令的返回值，0没错，1报错

# 运算
expr 1 + 2 (必须空格)
expr 5 \\* 2

简化写法
**$((5\*2))
$\[5\*2\]**

单括号把输出的值给变量a (命令替换), 单引号同样的效果
a=$(expr 5 \\* 2)
a=\`expr 5 \\* 2\`

a=$(ls -al)

---
add.sh
```sh
#!/bin/bash
echo $(($1+$2))
```

./add.sh 1 2
输出3

# 条件判断
test condition
**\[ condition\ ] -- 注意空格**

```sh
[ 1 = 1 ]&&echo 'True'||echo 'False' #True
[ 1 -lt 2 ]&&echo 'True'||echo 'False' #True
[ 1 = 2 ]&&echo 'True'||echo 'False' #False
```

因为> < linux中有别的用处，必须用以下符号判断大于 小于
![[Pasted image 20231111203134.png|450]]

---
-r -w -x  判定文件读写执行权限
```sh
[ -x hello.sh ]&&echo 'True'||echo 'False'
```

---
-e -f -d 判定文件或目录存在 是文件(非目录) 是目录

# 流程控制
; 可以吧多个命令放到一行中
hello.sh
```sh
#!/bin/bash
if [ $(($1+$2)) -gt 100 ];then
	echo 'Big number'
else
	echo 'Small nunber'
fi
```

运行 ./hello.sh 50 60 -- 输出 Big number

单行；写法
```sh
[root@192 shell]# if [ $((5+6)) -gt 10 ];then echo 'big';else echo 'small';fi
big
[root@192 shell]# if [ $((5+6)) -gt 100 ];then echo 'big';else echo 'small';fi
small
```

if else 以及连接的一些方法，以及参数防空的办法 ==$1x==  elif(艾里夫)
```sh
#!/bin/bash
#if [ "$1x" = "hellox" ] || [ "$1x" = "hix" ];then
if [ "$1x" = "hellox" -o "$1x" = "hix" ];then
    echo "hello, my friend"
elif [ "$1x" = "88x" ];then
    echo "byebye"
else 
    echo "Sorry"
fi
```

也可以用双括号简化表达
```sh
#!/bin/bash
if (( $1>60 && $1<100 ));then
    echo 'good marks'
else
    echo 'bad marks'
fi
```

打印当前目录的所有文件名
```sh
#!/bin/bash
for name in $(ls -al)
do
    if [ -e $name ];then
        echo $name
    fi
done
```
# case
```sh
#!/bin/bash
case $1 in
100)
    echo "full score"
    ;; #break
0)
    echo "zero scroe"
    ;;
*)
    echo "others"
esac
```

# for
```sh
#!/bin/bash
sum=0
for ((i=0;i<=$1;i++)) --双括号中才能用数学运算符号，其他地方还是要用 -lt -gt等等
do
    #echo $i
    sum=$(($sum+$i))
done
echo $sum
```
./add.sh 100 --输出5050

---
```sh
#!/bin/bash
for param in $@;do
    echo $param
done
```
./add.sh 60 61 62
--输出
60
61
62

---
在linux中 {1..100}表示一个范围
```sh
#!/bin/bash
sum=0
for num in {1..100}
do
    sum=$(( $num + $sum ))
done
echo $sum
```

---
对于input param可省略in
```sh
#!/bin/bash
for arg; do
    echo "This  is input arges: "$arg
done
```

使用printf -v 传出变量
```sh
for ((i=1; i<=5; i++))
do
    printf -v filename "file_%d.txt" "$i"
    touch "$filename"
done
```

## tricks
```sh
for pic in $(find . -name '*.jpg')
```
# while
```sh
#!/bin/bash
i=0
sum=0
while (( $i<=$1 ))
do
    sum=$(( $sum+$i ))
    i=$(( $i+1 ))
done
echo $sum
```


# read
读取用户输入
```sh
#!/bin/bash
read -p "Please enter your name: " name
echo "hello, $name"
```


```sh
#!/bin/bash
declare -A hMap #hash map
while read word count;do
    let hMap[$word]+=$count
done

for key in ${!hMap[@]};do # !是要取key， hMap[@]是取值
    echo key=$key value=${hMap[$key]}
done

```
# 内置函数
basename 去除一个文件的前缀路径后缀文件类型
例如 ``basename /home/hello.txt .txt``
输出 hello

---
```sh
#!/bin/bash
for name in $(ls -al)
do
    if [ -f $name ];then
        echo $(basename $name '.sh')_$(date +%s).bak
    fi
done
```

当前文件夹的 ==add.sh==将输出==add_1699544733.bak==

dirname 获得路径前缀
dirname /home/a.txt
输出 /home

# 自定义函数
函数体必须在调用前写。因为linux不会预编译。
参数还是$1 $2等等获得

==因为linux传递结果不易，可以在函数体内 echo 结果，调函数时用$()获取==
也可以用全局·变量去接函数的结果

两数相加
```sh
#!/bin/bash
function sum() {
    sum=$(( $1+$2 ))
    echo $sum
}

read -p "Input num1: " num1
read -p "Input num2: " num2

sumValue=$( sum $num1 $num2 )
echo $sumValue
```

# archive shell
```sh
#!/bin/bash
# 把/home/hg26502/shell 目录的所有文件归档保存到 /home/hg26502/archiveShell_$(date)_tar.gz
# 指令 tar -czf /home/hg26502/archiveShell_123.tar.gz /home/hg26502/shell
# 查看可用 tar -tzvf your_archive.tar.gz
# 解压缩指令 tar -xzf /home/hg26502/archiveShell_123.tar.gz -C /home/hg26502/
archiveFileName=''
function generateFileNameByDate() {
    archiveFileName=$1_$(date +%s).tar.gz 
}
cd /home/hg26502
generateFileNameByDate archiveShell
echo $archiveFileName

tar -czf $archiveFileName /home/hg26502/shell
echo "********show archieved files********"
ls -al /home/hg26502/archiveShell*
```

# 正则
grep -E 是正则
![[Pasted image 20240503114441.png|475]]

. 匹配任意字符
\* 0次或多次
\[\] 字符区间 \[0-9a-zA-Z\]

\\转义 用单引号静止转义 

# 文本处理
## cut
简单的裁剪获取==列==

以 ：做分隔符，截取1，6，7列
```sh
cat /etc/passwd|grep bash|cut -f 1,6,7 -d ':'
cat /etc/passwd|grep bash|cut -f 1-4 -d ':'  #截取1-4列
```

切ip地址用两次切割法
原始
```sh
        inet 172.18.0.1  netmask 255.255.0.0  broadcast 172.18.255.255
        inet 172.17.0.1  netmask 255.255.0.0  broadcast 172.17.255.255
        inet 192.168.31.88  netmask 255.255.255.0  broadcast 192.168.31.255
        inet 127.0.0.1  netmask 255.0.0.0
```

因为开头有空格，先用i 切掉，然后再用空格继续切
```sh
ifconfig|grep mask|cut -f 2 -d 'i'|cut -f 2 -d ' '
```

## awk
行列同时选取

以：分割，开头打印 begin，中间的以正则root选取第一第七列，最后打印end
```sh
cat /etc/passwd|awk -F ':' 'BEGIN{print "start"} /^root/{print $1","$7} END{print "end"}'
```

输出
```sh
start
root,/bin/bash
end
```

-v 可以引入一个变量

awk 切空格比cut智能
切ip代码
```sh
ifconfig | awk -F ' ' '/mask/{print $2}'
```

查询ipv4地址
```sh
ifconfig|awk -F ' ' '/[0-9]{2,3}\./{print $2}'
```

## sed
s/表示替换
-i 换文件里内容， 而非打印
-r 使用拓展正则

 sed -i -r 's/^a/XXX/g' a.txt

# 数组与Hash数组

数组的处理
```shell
#!/bin/bash
array=(a b c d)
echo ${array[@]}
echo ${array[*]}
echo ${#array[@]}
echo ${array[-1]}
echo ${!array[@]}
for va in ${array[@]};do
 echo $va
done
```

输出
```ssh
[root@192 shell]# ./hello.sh  
a b c d
a b c d
4
d
0 1 2 3
a
b
c
d
```

等价的两个写法取最后一个元素
```sh
echo ${a[-1]}
echo ${a[${#a[*]}-1]} # #a[*]是数组长度
```

```sh
#!/bin/bash
function String_Join {
    local delimiter="$1"
    local first_element="$2"
    shift 2 # 去除了参数1 参数2 ${@} 剩下了  b c
    printf '%s' "$first_element" "${@/#/$delimiter}" # /#/$delimiter把间隔符换成了$1 --
    # Print first element, then reuse the '%s' format to display the rest of
    # the elements (from the function args $@), but add a prefix of $delimiter
    # by "replacing" the leading empty pattern (/#) with $delimiter.
}
String_Join $*
```
输入 ./hello.sh -- a b c
输出 a--b--c

---
```sh
a=(a b c d)
echo ${a[@]}  #输出 a b c d
echo ${!a[@]} #输出下标 1 2 3 4
```

---
```sh
#!/bin/bash
declare -A mylist=([a]="foo" [b]="bar")
echo ${#mylist[@]}
for i in ${mylist[@]};do
    echo $i
done
echo ${mylist[b]}
```


# Param
:-XXX 设置默认值，如果用户不input就用默认的

```sh
input=${1:-no input}
echo $input
```

读取参数的例子
```sh
while getopts ':v:q' VAL;do 
#第一个：表示出错时忽略， v：表示 -v后面有args，q表示接受-q不带参数
case $VAL in 
v )
    v=${OPTARG} # OPTARG读取值
    ;;
q )
    mode='quite'
    ;;
esac
done
echo $v "***" $mode
```
输出
```sh
[root@192 shell]# ./hello.sh -v 2.0 -q
2.0 *** quite
```


# 2ways print escape 
```sh
next=$'\n' --这是linux的一个特定用法这里会产生一个换行符号而不是\n字符
echo "hello${next}${next2}world"
```
output:
hello
world

---
# ssh

用户/.ssh/autherized_keys
远程服务器存储客户端公钥的地址，客户端生成公钥私钥对，把公钥提供给服务器

创建公钥 私钥
ssh -keygen

-> /用户/.ssh/id_rsa

生成了
id_rsa
id_rsa.pub

echo 'id_rsa.pub的内容'>>authorized_keys

注意各路径权限
本地
chmod 600 ~/.ssh/id_rsa

远程
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys

# printf
```sh
printf -v a "hello, %s\n" Tom
a=$(echo "hello, Tom")
```
output -- ``hello, Tom``

脚本开头
==#!/bin/bash==

# 执行脚本
bash hello.sh -- 用这个跑不用x权限，用bash解析的文件
./hello.sh    /home/hg26502/hello.sh -- 相对路径绝对路径执行

直接打hello.sh无法执行，因为linux把这个当作一个命令，你的bin目录中没有这个命令

---

ps -f --查看进程

```sh
UID          PID    PPID  C STIME TTY          TIME CMD
root       75893    4430  0 14:25 pts/16   00:00:00 /bin/bash --init-file /root/.vscode-server/bin/f1b07bd25df
root       78128   75893  0 15:01 pts/16   00:00:00 bash
root       78157   78128  0 15:01 pts/16   00:00:00 ps -f
```

父shell子shell
子shell能用父shell的变量但是改变不会影响到父shell