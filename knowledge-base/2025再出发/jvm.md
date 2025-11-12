垃圾回收 G1 JDK17默认垃圾回收

jvm
hotspot, Jrockit, Graal VM
HotSpot 使用JIT，会编译出一些本地代码，提高效率

![[Pasted image 20250911091334.png]]

JIT二次编译把class编译成机器指令并缓存，提高了效率


JVM生命周期

bootstrap class loader 创建一个初始类

![[Pasted image 20250911095824.png|313]]

![[Pasted image 20250911102954.png|500]]
程序计数器 -- 锁定程序执行到的行号
![[Pasted image 20250911104536.png|550]]
栈里有 本地变量表，常量池，方法链接


堆 -- 存对象
方法区 -- 类信息 类常量池 运行时常量池 （meta space就是这个的实现）
![[Pasted image 20250911110035.png|700]]

# 垃圾回收
可达性分析算法 来判断堆内存是否还在被使用 看有没有引用 到达 GCRoots

![[Pasted image 20250911132459.png]]
GC是在新生代查看，反复地淘汰回收，长期没有回收掉的，就放到老年代（老年代回收频率较低）
Minor GC 新生代GC （频率高）
Major GC 老年代GC（频率低）
Full GC 整个堆内存回收

-XX：printGCDetails

PSN +PO收集器 jdk1.8默认
![[Pasted image 20250911135555.png]]


CMS
![[Pasted image 20250911135722.png]]
垃圾标记和清理可以和用户线程并发运行了
但是会产生大量内存碎片，会增加full gc

G1
![[Pasted image 20250911150223.png]]
每个快不再连续，按需调配新生代 老年代，以及特殊大容量数据 Humongous

具体回收步骤类似CMS

