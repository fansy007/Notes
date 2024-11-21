colima是docker的一套MAC ROSSETA的实现，使得docker win image的运行可以在MAC M系列CPU上
```sh
colima stop
colima start --arch x86_64 --memory 4
docker pull gvenzl/oracle-xe
docker run -d --name oracle -p 1521:1521 -e ORACLE_PASSWORD=198263 gvenzl/oracle-xe
（container stop后可用docker start oracle直接拉起来）
docker exec -it oracle sqlplus sys/198263@localhost:1521/XEPDB1 as sysdba
```


mirror
```sh
Docker 的配置文件位于 ~/.docker/config.json

{
  "registry-mirrors": ["https://01uinh3k.mirror.aliyuncs.com"]
}
```
# vscode plugin
Oracle Developer Tools for VS Code (SQL and PLSQL)

# 建立用户
```sh
docker exec -it oracle sqlplus sys/198263@localhost:1521/XEPDB1 as sysdba

CREATE TABLESPACE test
DATAFILE 'test.dbf'
SIZE 50M
AUTOEXTEND ON
NEXT 50M MAXSIZE UNLIMITED;

CREATE TEMPORARY TABLESPACE temp
TEMPFILE 'temp.dbf'
SIZE 50M
AUTOEXTEND ON
NEXT 50M MAXSIZE UNLIMITED;

-- 创建用户并设置密码
CREATE USER qjgeng IDENTIFIED BY 198263
DEFAULT TABLESPACE test
TEMPORARY TABLESPACE temp;

-- 授予基本权限
GRANT CONNECT, RESOURCE TO qjgeng;

-- 授予表空间使用权限
ALTER USER qjgeng QUOTA UNLIMITED ON test;
```

连接
docker exec -it oracle sqlplus qjgeng/198263@locahost:1521/XEPDB1

# 原理
这样用户qjgeng在PDB （XEPDB1）的表空间 test中建立起来了
例如再建用户Lee在PDB （XEPDB1）的表空间 test2

那么这两个用户在不同的表空间操作可以隔离开
而sys可以操纵所有的用户，所有的表空间

可以用sql查询每个user的default表空间名字
```sql
SELECT u.DEFAULT_TABLESPACE, u.* FROM user_users u;
```


