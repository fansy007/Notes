# Basic
保持out能够答应
==SET SERVEROUTPUT ON;==
## 基本格式

```sql
DECLARE
    v_name VARCHAR2(20):='Lee';
    v_sal LONG;
    v_address VARCHAR2(200);

BEGIN
    SELECT 20000,'Shanghai' INTO v_sal,v_address FROM DUAL;
    dbms_output.put_line(v_name||','||v_sal||','||v_address );
END;
/
```

## 类型变量
%TYPE
%ROWTYPE
```sql
DECLARE
    v_ename EMP.ENAME%TYPE;
    v_sal   EMP.SAL%TYPE;
BEGIN
    SELECT ENAME, SAL INTO v_ename, v_sal FROM EMP WHERE ROWNUM=1;
    dbms_output.put_line('*****');
    dbms_output.put_line(v_ename||' '||v_sal);
END;
/
```

```sql
DECLARE
    v_emp EMP%ROWTYPE;
BEGIN
    SELECT * INTO v_emp FROM EMP WHERE ROWNUM=1;
    dbms_output.put_line('*****');
    dbms_output.put_line(v_emp.ename||' '||v_emp.sal);
END;
/
``` 

## 条件
```sql
DECLARE
    v_cnt NUMBER;
BEGIN
    SELECT count(*) into v_cnt FROM EMP;
    IF v_cnt > 20 
        THEN 
            dbms_output.put_line('>20');
    ELSIF v_cnt > 10
        THEN 
            dbms_output.put_line('>10');
    ELSE
        dbms_output.put_line('<=10');
    END IF;
END;
/
```

```sql
DECLARE
    v_cnt NUMBER:=1;
    v_sum NUMBER:=0;
BEGIN
    LOOP
        v_sum:=v_sum+v_cnt;
        v_cnt:=v_cnt+1;
        EXIT WHEN v_cnt>10;
    END LOOP;
    
    dbms_output.put_line(v_sum);
END;
/
```

## 游标

decalre
open
fetch into
close
```sql
DECLARE
    CURSOR c_emp IS SELECT * FROM EMP;
    v_emp EMP%ROWTYPE;
BEGIN
    OPEN c_emp;
    
    LOOP
        FETCH c_emp INTO v_emp;
        dbms_output.put_line(v_emp.ENAME||' '||v_emp.SAL);
        EXIT WHEN c_emp%NOTFOUND;
    END LOOP;
    
    CLOSE c_emp;
END;
/
```
### 2.1. 什么是游标

用于临时存储一个查询返回的多行数据（结果集,类似于Java的Jdbc连接返回的ResultSet集合），通过遍历游标，可以逐行访问处理该结果集的数据。

游标的使用方式：声明--->打开--->读取--->关闭

### 2.2. 语法

游标声明：

CURSOR 游标名[(参数列表)] IS 查询语句;

游标的打开：

OPEN 游标名;

游标的取值：

FETCH 游标名 INTO 变量列表;

游标的关闭：

CLOSE 游标名;

### 2.3. 游标的属性

|游标的属性|返回值类型|说明|
|---|---|---|
|%ROWCOUNT|整型|获得FETCH语句返回的数据行数|
|%FOUND|布尔型|最近的FETCH语句返回一行数据则为真，否则为假|
|**%NOTFOUND**|布尔型|与%FOUND属性返回值相反|
|%ISOPEN|布尔型|游标已经打开时值为真，否则为假|

其中 %NOTFOUND是在游标中找不到元素的时候返回TRUE,通常用来判断退出循环

## 有表传参数
查询薪水大于有表传参的记录

```sql
DECLARE
    CURSOR c_emp(v_low number) IS SELECT * FROM EMP WHERE SAL>v_low;
    v_emp EMP%ROWTYPE;
BEGIN
    OPEN c_emp(2500);
    
    LOOP
        FETCH c_emp INTO v_emp;
        dbms_output.put_line(v_emp.ENAME||' '||v_emp.SAL);
        EXIT WHEN c_emp%NOTFOUND;
    END LOOP;
    
    CLOSE c_emp;
END;
/
```

# Procedure

```sql
create or REPLACE PROCEDURE p_hello is
    v_msg varchar2(20):='test';
BEGIN
    dbms_output.put_line('hello '||v_msg);
END p_hello;
/
```

## 调用
两种调用办法
```sql

exec p_hello;


BEGIN
    p_hello;
END;
/
```

## !!!带输入输出变量的procedure

这样写可以使no data found 时不会抛错
```sql
create or REPLACE PROCEDURE queryByNo(in_num IN NUMBER, out_name OUT EMP.ENAME%TYPE ) is

BEGIN
    SELECT ENAME INTO out_name FROM EMP WHERE EMPNO=in_num;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        out_name:='NO DATA FOUND';
END queryByNo;
/
```

调用
```sql
DECLARE
v_out EMP.ENAME%TYPE;
BEGIN
    queryByNo(1002, v_out);
    dbms_output.put_line('hello '||v_out);
END;
/
```

## !!! sample query objType arrayType Cursor
```sql
-- 名称       空值?      类型           
-- -------- -------- ------------ 
-- EMPNO    NOT NULL NUMBER(4)    
-- ENAME             VARCHAR2(10) 
-- JOB               VARCHAR2(9)  
-- MGR               NUMBER(4)    
-- HIREDATE          DATE         
-- SAL               NUMBER(7,2)  
-- COMM              NUMBER(7,2)  
-- DEPTNO            NUMBER(2) 
create or replace TYPE empObj AS OBJECT (
    empno NUMBER(4),
    ename VARCHAR2(10),
    sal   NUMBER(7,2)
);
/

create or replace TYPE empArray AS TABLE OF empObj;
/

create or replace procedure queryEmp(p_empno IN EMP.EMPNO%TYPE, emps OUT empArray) is
    CURSOR c_emp is
        select * FROM EMP where EMPNO>p_empno;
    v_emp EMP%ROWTYPE;
BEGIN
    emps:=empArray();
    OPEN c_emp;
    LOOP
    FETCH c_emp INTO v_emp;
    if (c_emp%FOUND) then
        emps.extend();
        dbms_output.put_line('do extend');
        emps(emps.count):=empObj(v_emp.empno,v_emp.ENAME,v_emp.SAL); -- table type index start with 1 not 0 
    end if;
    EXIT WHEN c_emp%NOTFOUND;
    END LOOP;
    
    CLOSE c_emp;
END;
/

DECLARE 
    emps empArray;
    i INTEGER;
BEGIN
    queryEmp(1,emps);
    i:=emps.FIRST;
    WHILE i is not NULL LOOP
        dbms_output.put_line(emps(i).empno||' '||emps(i).ename||' '||emps(i).sal);
        i:=emps.NEXT(i);
    END LOOP;

END;
/
```

# Java代码调用
```java
public void queryByEmpId(Long empNo) throws Exception {  
    Connection conn = oracleTemplate.getDataSource().getConnection();  
    String sql = "{call queryByNo(?,?)}";  
    CallableStatement call = conn.prepareCall(sql);  
    call.setLong(1, empNo);  
    call.registerOutParameter(2, OracleTypes.VARCHAR);  
    call.execute();  
    String rsp = call.getString(2);  
    System.out.println(rsp);  
}
```

```gradle
implementation 'com.oracle.database.jdbc:ojdbc8:19.3.0.0'  
implementation 'org.springframework:spring-jdbc'
```

```java
@Configuration  
public class OracleDbConfig {  
    @Bean("oracleDS")  
    public DataSource dataSource() {  
        DriverManagerDataSource dataSource = new DriverManagerDataSource();  
        dataSource.setDriverClassName("oracle.jdbc.driver.OracleDriver");  
        dataSource.setUrl("jdbc:oracle:thin:@//localhost:1521/XEPDB1");  
        dataSource.setUsername("qjgeng");  
        dataSource.setPassword("198263");  
        return dataSource;  
    }  
  
    @Bean("oracleTemplate")  
    public JdbcTemplate jdbcTemplate(@Qualifier("oracleDS") DataSource dataSource) {  
        return new JdbcTemplate(dataSource);  
    }  
}
```


# Function
function will return a value
```sql
SET SERVEROUTPUT ON;

CREATE or REPLACE FUNCTION fetchSalaryByName(ename EMP.ENAME%TYPE) RETURN EMP.SAL%TYPE IS
CURSOR cursor_sal is SELECT SAL FROM EMP WHERE ENAME=ename;
v_sal EMP.SAL%TYPE;
v_sal_summary EMP.SAL%TYPE;

BEGIN
    v_sal_summary:=0;
    OPEN cursor_sal;
    LOOP
        fetch cursor_sal INTO v_sal;
        IF cursor_sal%FOUND THEN
            v_sal_summary:=v_sal_summary+v_sal;
        END IF;
        EXIT WHEN cursor_sal%NOTFOUND;
    END LOOP;

    CLOSE cursor_sal;
    return v_sal_summary;
END fetchSalaryByName;
/

DECLARE
sal EMP.SAL%TYPE;
BEGIN
--SELECT fetchSalaryByName('BLAKE') INTO sal FROM DUAL;
sal:=fetchSalaryByName('BLAKE');
DBMS_OUTPUT.put_line(sal);
END;
/
```

# Package

CREATE OR REPLACE PACKAGE fansy007 IS
CREATE OR REPLACE PACKAGE BODY fansy007 IS

```sql
SET SERVEROUTPUT ON;
CREATE OR REPLACE PACKAGE fansy007 IS
    PROCEDURE sayHello(input_word IN OUT VARCHAR2);
    FUNCTION sayHelloFun(input_word VARCHAR2) return VARCHAR2;
END;
/

CREATE OR REPLACE PACKAGE BODY fansy007 IS
    PROCEDURE sayHello(input_word IN OUT VARCHAR2) IS

    BEGIN
        input_word:=sayHelloFun(input_word);
    END sayHello;    

    FUNCTION sayHelloFun(input_word VARCHAR2) return VARCHAR2 IS
        o_word VARCHAR2(30);
    BEGIN
        o_word:='Hello, '||input_word;
        RETURN o_word;
    END sayHelloFun;
END;
/

SELECT fansy007.sayHelloFun('TOM') FROM dual;


DECLARE
    v_word VARCHAR2(30);
BEGIN
    v_word:='Lee';
    fansy007.sayHello(v_word);
    DBMS_OUTPUT.PUT_LINE(v_word);
END;
```

26讲19分钟 待续