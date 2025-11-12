Thread::start ->
private native void start0();

进程 一个app就是一个进程
线程 一个进程中就有多个线程
管程 同步时，用来确保同步的Monitor对象

用户线程 和 守护线程（Daemon Thread）
例如垃圾回收线程 当所有用户进程都结束的时候，守护线程会自动退出

# Completable future

future task
![[Pasted image 20250908084700.png|450]]
传统代码
```java
public class FutureDemo {
    public static void main(String[] args) throws Exception{
        ExecutorService es = Executors.newFixedThreadPool(5);
        FutureTask future = new FutureTask(()->"hello world");
        FutureTask future2 = new FutureTask(()->"hello world2");
        es.submit(future);
        es.submit(future2);
        System.out.println(future.get());
        System.out.println(future2.get());
        es.shutdown();
    }
}

class SimpleCall implements Callable<String> {
    @Override
    public String call() throws Exception {
        return "hello world";
    }
}
```

默认的线程池folk join pool是守护线程，主线程结束时会自动关闭。（哪怕你的分线程还没运行！！！）
所以可以使用自定义的fixthreadpool解决这个问题，只有你手动关闭才会结束代码

# 悲观锁
悲观锁，在修改数据之前，直接把代码块锁起来，保证只有自己这个线程才能操作这个被锁的数据

修改之前不锁代码块，但是当写入之前，判断我写入之前有没有人改过，如果改过了，要么放弃写，要么从头再来一遍。 例子，tradeVersion 判定｜｜CAS

每个object都有一个objectMonitor
ObjectMonitor 有owner对象 ，当有owner时，别人无法持有锁

![[Pasted image 20250908140358.png]]
非公平锁cpu效率最高

可重入锁，对于同一个锁，同一个线程可以进入同一把锁的任何内部方法
synchronize内置的就是可重入锁
ObjectMonitor 有重入次数的记录 enter一次+1， exit一次-1，到0释放

ReentrantLock也是可重录锁
每个lock 要有一个unlock

# 死锁的排查
jps -l
jstack 进程号

jconsole 看看线程状况

# 中断协商
中断协商机制
一个线程不应该由其他线程也强制停止。应该由自己来停。

例如主线程要结束一个子线程，可以标记调用该子线程的interupt方法。
该子线程不断循环判断flag为true，自己写代码中断

使用 volatile boolean
使用 AtomicBoolean

当线程处在sleep wait等阻塞状态时，调用了interupt会抛出异常并推出阻塞状态
![[Pasted image 20250908153831.png]]

	Thread::interupted这是一个静态方法，1）判断当前线程是否中断 2）重置为没有中断

# 线程等待 唤醒
Object::wait Object::notify
用在synchronize的锁上


LockSupport.park();
LockSupport.unpark(t1);
一般只能使用一对

# JMM
![[Pasted image 20250909090908.png|275]]
JMM协调 cpu 和 内存之间沟通的问题

JMM的三大特性
多线程 的 原子性 可见性 有序性

## 可见性
所有的变量在主内存里， 线程读主内存变量load到线程的内存的副本上，在通过JMM写回主内存
![[Pasted image 20250909092141.png|400]]

在不保证原子性的时候，多线程有可能脏读

## 有序性
java指令 允许或者禁止重排序（异步时可能导致脏读）

happens before是对可见性有序性的约束 直白的说就是多个线程对于同一个共享数据读写的规范

# volatile
volatile是为了保证 可见性 有序性， 也是就是说这个变量是要被多线程读写的
加了vollatile 每次读写，JMM都会立即从主内存load或者写入主内存并且发通知

实现的要点 -- 内存屏障
但是不保证原子性
![[Pasted image 20250909102034.png|650]]

```java
    private static volatile Boolean isStop = false;

    public static void main(String[] args) throws Exception {
        new Thread(() -> {
            doPrint("start");
            while (!isStop) {
            }
            doPrint("end");
        }).start();
        Thread.sleep(500);
        isStop = true;
        doPrint("end");
    }

    private static void doPrint(String msg) {
        System.out.println(Thread.currentThread().getName() + ": " + msg);
    }
```
以上例子当不加volatile的时候，线程中的isStop得不到刷新，程序将无法停止

但是 volatile不能做保证原子性，例如i++之类的不能靠volatile保证原子性
有序性的例子 单例饿汉式

# CAS
compare and swap 

类似于乐观锁的原理
读取时，读一个版本
写入时，再一次读版本比较两个版本是否一致，如果一致，增加版本，如果不一致放弃从读（自旋）

本质上说CAS是cpu level的一条基本指令，保证了原子性

AtomicFeference 原子引用
自旋锁
```java
import java.util.concurrent.atomic.AtomicReference;

public class SpinLock {
    // 记录当前持有锁的线程
    private final AtomicReference<Thread> owner = new AtomicReference<>();

    // 加锁
    public void lock() {
        Thread current = Thread.currentThread();
        // 自旋尝试获取锁
        while (!owner.compareAndSet(null, current)) {
            // 自旋等待，不释放 CPU（可能需要 Thread.yield() 避免死等）
        }
    }

    // 解锁
    public void unlock() {
        Thread current = Thread.currentThread();
        // 只有持有锁的线程才能解锁
        if (!owner.compareAndSet(current, null)) {
            throw new IllegalMonitorStateException("Current thread does not hold the lock");
        }
    }
}
```
缺点
循环过久开销很大

无法识别ABA问题
解决ABA可以加版本号
AtomicStampedReference::compareAndSet

CountDownLauch::countDown
CountDownLauch::await

# ThreadLocal
如果线程池 线程会复用， 如果ThreadLocal不做remove，会带到下一个线程的计算去
![[Pasted image 20250910133427.png|800]]
每个Thread有一个ThreadLocal对象
然后ThreadLocal类有ThreadLocalMap的静态内部类，，保存了当前thread 中
threadLocal，值的map

引用
强 软 弱 虚

强引用指向一个变量时永远不回收，所以不用可以设null回收
软引用， 当指向变量时，内存够时不回收，不够了会被回收 （用于缓存）
弱引用， 只要gc，立刻回收掉
虚引用永远get到null，主要跟踪垃圾回收的状态和通知机制，虚引用被回收时ReferenceQueue会收到，从而可以通知


ThreadLocal的一个垃圾回收的困扰
由于每个线程都有一个threadLocal的Map，这个map的key是threadLocal的弱引用，value是threadlocal的value，当线程中的ThreadLocal指向null之后，`ThreadLocal`实例Map的key（也就是弱引用）随着垃圾回收也会置为null，那么在处理线程池的时候这个map中会有大量key=null的垃圾数据，若以需要ThreadLocal::remove显式的去除这个key

# 对象头
![[Pasted image 20250910145629.png|375]]

读写锁 ReentrantReadWriteLock
读读不互斥
读写，谢谢互斥

写锁降级： 锁写-》锁读-〉释放写-》释放读
StampedLock 乐观锁， 读没有完成写锁也能进入，不可重入的
读 写 乐观读