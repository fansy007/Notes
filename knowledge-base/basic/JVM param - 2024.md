JVM param: -Dxxx=xxx
ENV param: export xxx=xxx
Java main function args: public static void main(String[] argv)

```sh
export env_param1=myenv  
javac TestProperty.java  
java -Dvm_prop1=abc -Dvm_prop2=123 TestProperty cmd_arg1 cmd_arg2
```

```java
public class TestProperty {  
    public static void main(String[] argv) {  
        // - 命令行参数  
        System.out.println(argv[0]);  
        System.out.println(argv[1]);  
  
        // - JVM虚拟机参数  
        System.out.println(System.getProperty("vm_prop1"));  
        System.out.println(System.getProperty("vm_prop2"));  
  
        // - 环境变量  
        System.out.println(System.getenv("env_param1"));  
    }  
}
```
