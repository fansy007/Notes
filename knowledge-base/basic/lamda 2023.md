#java
# Stream
Array是数组，Collection是集合，Arrays.asList转出来的List是一个固定长度的List本质还是数组
## How to create Stream
### Stream::of(T.. values)

Stream::of  是把 T.. values转Stream
Arrays::stream 是吧 Array转Stream

```java
    // Arrays::stream
	public static<T> Stream<T> of(T... values) {
        return Arrays.stream(values);
    }
```

```java
String result = Stream.of("one","two","three").collect(Collectors.joining(","));
```

### Stream::iterator

根据一个初始值，和变形函数生成Stream

```java
Stream.iterate(2L, num -> num*num).limit(10).forEach(System.out::println);
```



### Stream::generator

根据supplier函数生成stream

```java
Stream.generate(()-> new Random().nextInt(100)).limit(10).forEach(System.out::println);
```
### IntStream, LongStream::range
```java
System.out.println(IntStream.rangeClosed(1,100).sum());
```
# Box

IntStream不能直接转数组，需要box之后转

```java
List<Integer> numbers = IntStream.of(1,3,5,7,9).boxed().collect(Collectors.toList());
```



也可以map to object 对于IntStream类，输入int输出Object

```java
IntStream.of(1,3,5,7,9).mapToObj(Integer::valueOf).collect(Collectors.toList());
```



或者放弃转List直接转数组

```java
int[] intArray = IntStream.of(1,3,5,7,9).toArray();
```



### Conver array of the type you want

toArray(size -> new CompletableFuture[size]) 注意这个是一个套路

```java
        CompletableFuture[] futures = IntStream.rangeClosed(1,10).mapToObj(i->
                CompletableFuture.runAsync(System.out::println)
        ).toArray(size -> new CompletableFuture[size]); //也可写成 CompletableFuture[]::new
        
        CompletableFuture.allOf(futures).join();
```



### Reduce

==reduce的含义是对一个stream进行归并操作，这样输入是一组值，最终返回一个值==

返回0

```java
System.out.println(IntStream.rangeClosed(1,100).reduce(-5050, (x,y) -> x + y));
```



可以使用一些static方法使reduce更漂亮

```java
IntStream.rangeClosed(1,100).reduce(Integer.MIN_VALUE, Integer::max)
```

```java
Stream.of("This","is","a","cat").reduce(String::concat).orElse(null)
```



### reduce复杂用法

[go to head](#Stream)

==init，accumulator，combinor==



三个参数， 第一个提供变化后的对象，第二个accumulator bifunction 输入变化后对象，变化前对象，你提供转换方法

第三个是 combinor bifunction，要把变化后对象合并

```java
        Stream.of("This", "is", "a", "cat").reduce(new ArrayList<String>(), (lst, v) -> {
                    lst.add(v);
                    return lst; // accumulator
                }
                , (lst1, lst2) -> {
                    lst1.addAll(lst2);
                    return lst1; // combiner
                });
```



和 Stream::collect方法相似，但不完全相同 (这里都是不反回的BI consumer，reduce是要返回 BI function)

```java
ArrayList<String> words = Stream.of("This", "is", "a", "cat").collect(ArrayList<String>::new,(lst, v) -> lst.add(v),(lst1,lst2)
->lst1.addAll(lst2));

```


# Wrap exception in Fun interface
```java
@FunctionalInterface  
public interface FunctionWithExceptions<I, R, E extends Exception> {  
    R apply(I input) throws E;  
}

public class ExceptionFunWrapper {  
    public static <I, R, E extends Exception> Function<I,R> wrap(FunctionWithExceptions<I,R,E> fe) {  
        return input -> {  
            try {  
                return fe.apply( input);  
            } catch (Exception e) {  
                throw new RuntimeException(e);  
            }  
        };  
    }

public static  void main(String args[]) {  
        List<String> sampeStrings = Arrays.asList("a=4","http://aaa.com?a=123&b=456");  
        sampeStrings.stream().map(wrap(input -> URLEncoder.encode(input,"UTF-8"))).forEach(System.out::println);  
    }  
}
```

---
# String::codePoints

create a IntStream with codePoints
```java
"Hello world !@#$@$#@$中文".
codePoints().mapToObj(Character::getName).forEach(System.out::println);
```

```java
public boolean isPalidrome(String s) {  
	s = s.codePoints().filter(Character::isLetterOrDigit)
	.map(Character::toLowerCase)  
	.collect(StringBuilder::new,StringBuilder::appendCodePoint,StringBuilder::append).toString();  
	  
	return s.equals(new StringBuilder(s).reverse().toString());  
}
```
---
# FlatMap
![[Draw flat map]]
```Java
Master m1 = new Master("Zhang", new String[]{"Java","C++"});  
Master m2 = new Master("Wang", new String[]{"Python","C++"});  
Stream.of(m1,m2).flatMap(master -> Stream.of(master.getSkills())).distinct().forEach(System.out::println);
```

## concat streams
```java
public <T> Stream<T> concatStream(Stream<T> ...streams) {  
	return Stream.of(streams).flatMap(Function.identity());  
}
```