通过property 文件传参数
```java
@Configuration
@PropertySource({"classpath:/db.properties"})
public class DatabaseConfig {
    @Value("${jdbc.driver}")
    String driver;
```


