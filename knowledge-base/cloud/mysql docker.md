# 安装
```sh
docker pull mysql:5.7
docker run --name mysql -e MYSQL_ROOT_PASSWORD=198263 -v /home/hg26502/mysqldata:/var/lib/mysql -p 3306:3306 --restart always -d mysql:latest
```

# 建库
docker exec -it mysql bash
mysql -u username -p
CREATE DATABASE mydatabase;
exit

# Spring JDBC transactional control
==config bean 加注解==
@EnableTransactionManagement
public class SimpleTest

==事务方法加注解==
@Transactional  
public void doTransaction() {  
    doInsert("Edward",99).doInsert("Leo", 19).queryAll();  
    throw new RuntimeException("Error happen");  
}

==配置transaction management bean==
```sh
public class DatabaseConfig {

    @Bean
    public DataSource dataSource() {
        DriverManagerDataSource dataSource = new DriverManagerDataSource();
        dataSource.setDriverClassName("com.mysql.cj.jdbc.Driver");
        dataSource.setUrl("jdbc:mysql://192.168.31.88:3306/test?allowPublicKeyRetrieval=true&useSSL=false&serverTimezone=UTC");
        dataSource.setUsername("root");
        dataSource.setPassword("198263");
        return dataSource;
    }

    @Bean
    public JdbcTemplate jdbcTemplate(DataSource dataSource) {
        return new JdbcTemplate(dataSource);
    }

    @Bean
    public PlatformTransactionManager transactionManager(DataSource dataSource) { // here
        return new DataSourceTransactionManager(dataSource);
    }
}
```
