写入 用super， 读出用 extends
```java
<R> Stream<R> map(Function<? super T, ? extends R> mapper);
```

这是一个写入，接收的是Person或者Person的父类，因为Developer可以向上转型所以可以传入
```java
public void doCS(Function<? super Person, String> converter, Developer obj) {  
	String result = converter.apply(obj);  
	System.out.println(result);  
}

// 调用的例子

```

写入数组
```java
public static void fill(List<? super Number> numLst) {  
    numLst.add(1);  
    numLst.add(1.1d);  
    numLst.add(new BigDecimal("1.2"));  
    numLst.stream().forEach(System.out::println);  
}
```

---

这是一个读出，因为converter转换出来的是Person的子类，所以可以用Person result来接
```java
public void doPE(Function<String, ? extends Person> converter, String name) {  
	Person result = converter.apply(name);  
	System.out.println(result.sayHello2());  
}

// 调用的例子， Developer::new返回的是一个Person的子类， 
doPE(Developer::new, "Lee");
```

读取数组
```java
    public static void use(List<? extends Number> numLst) {  
        numLst.stream().map(Number::intValue).forEach(System.out::println);  
    }
```
