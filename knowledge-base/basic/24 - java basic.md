#java 

# use UUID class
```javascript
UUID id = UUID.randomUUID();
System.out.println(id.toString());
```

# int Integer
int not set value will be 0
Integer will be null

在一个大的loop中，使用int效率高很多。

# Date

yyyy年
MM ->01
MMM -> Jan
dd -> 日
HH ->小时 23
hh ->小时 11
mm ->分钟 59
ss ->秒 01
SSS ->豪秒
a -> AM PM

```java
    public static void playDate() {
        LocalDate firstDate = LocalDate.of(2024, Month.APRIL, 22);
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("MM/dd/yyyy");
        System.out.println(formatter.format(firstDate));

        LocalDate secondDate = LocalDate.parse("06/01/2024",formatter);
        System.out.println(secondDate);
    }

    public static void playZoneDateTime() {
        Instant nowUtc = Instant.now(); // instant 是utc的一个时刻不带时区
        System.out.println(nowUtc);

        ZonedDateTime nowLocalTimeZone = ZonedDateTime.now();
        System.out.println("local time: " + nowLocalTimeZone);

        ZonedDateTime newYork = ZonedDateTime.now(TimeZone.getTimeZone("America/New_York").toZoneId());
        System.out.println("new york time: " + newYork.format(DateTimeFormatter.ISO_ZONED_DATE_TIME));
    }
```

# lamda

## bound reference vs unbound reference
```java
String name = "Tom, Great";  
Supplier<String> nameL = name::toLowerCase;  // this is a bound reference, bound to variable "Tom, Great"  
System.out.println(nameL.get());  
  
Predicate<String> testStartWith = name::startsWith;  
System.out.println(testStartWith.test("To"));

// unbound function
Function<String,String> nameL2 = String::toLowerCase;  // unbound
System.out.println(nameL2.apply("Tom"));

BinaryOperator<String> bi = (s1,s2)-> s1.concat(s2); // the same as BinaryOperator<String> bi = String::concat; 
System.out.println(bi.apply("Tom","Mary"));
```

# static method reference
```java
Consumer<List<Integer>> sortI = Collections::sort;  
List<Integer> myLst = Arrays.asList(5,9,7,4);  
sortI.accept(myLst);  
System.out.println(myLst);
```

## constructor reference
```javascript
Supplier<StringBuilder> sb = StringBuilder::new;  
System.out.println(sb.get().append("Hello").append(" world").toString());

Supplier<ArrayList<String>> ss = ArrayList::new;  
ArrayList<String> sampleLst = ss.get();  
sampleLst.add("Tom");  
System.out.println(sampleLst);
```


the same lamda with diffrent function interface, compiler know how to pass in params accordingly
```javascript
public static int howMany(String... stuffs) {  
    return stuffs.length;  
}  
  
public static void playLamda() {  
    Supplier<Integer> fun1 = Lamda::howMany;  
    Function<String, Integer> fun2 = Lamda::howMany;  
    BiFunction<String,String,Integer> fun3 = Lamda::howMany;  
  
    System.out.println(String.format("%s,%s,%s",fun1.get()  
            ,fun2.apply("Tom")  
            ,fun3.apply("Tom","Mary")));  
}
```