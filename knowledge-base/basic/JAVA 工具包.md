commons-cli 解析命令行
commons-codec 密码相关


# commons-lang3

```java
    @Test
    public void stringTest() {
        String input = "123456789";
        String output = StringUtils.left(input,3)+"***"+StringUtils.right(input,3);
        System.out.println(output);

        String output2 = StringUtils.rightPad(input, 12, '*');
        System.out.println(output2);
    }
```
123\*\*\*789
123789\*\*\*

---

```java
        System.out.println(NumberUtils.isDigits("12"));
        System.out.println(NumberUtils.isDigits("12.3"));
        System.out.println(NumberUtils.isParsable("12.3"));
```
true
false
true

---
```java
		String[] arrays = Stream.of("hello","world").toArray(String[]::new);
        String[] arrays2 = ArrayUtils.addAll(arrays,"my", "friend");
        Stream.of(arrays,arrays2).flatMap(Stream::of).forEach(System.out::println); 
```

hello
world
hello
world
my
friend