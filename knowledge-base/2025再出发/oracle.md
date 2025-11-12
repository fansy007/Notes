# 虚拟机环境设定
sudo systemctl stop firewalld
sudo systemctl disable firewalld
sudo systemctl status firewalld

systemctl stop NetworkManager
systemctl start NetworkManager

# 性能问题的定位
1. sql （看看执行计划）
2. 会话层 （看看哪个client造成问题）V\$SESSION  V\$SESSSTAT V&LOCK V\$SEESION_WAIT
看看会话数，进程数等等，lock情况
3. 系统层 AWR OSTool PROMESUS 优化器

优化器重写sql，不见得是好事情 （集合如何整合的优化，数学的层面）
高效的sql来自于对业务的理解 和SQL本身的理解

OVR PARTITION
```sql
SELECT 
    salesperson,
    sale_date,
    amount,
    SUM(amount) OVER (
        PARTITION BY salesperson 
        ORDER BY sale_date 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_amount
FROM sales_records;
```

```sql
SELECT 
    employee_id,
    employee_name,
    manager_id,
    LEVEL AS hierarchy_level, -- 当前行在树中的层级（根节点为1）
    LPAD(' ', (LEVEL - 1) * 4) || employee_name AS visual_tree, -- 用于可视化层级缩进
    SYS_CONNECT_BY_PATH(employee_name, ' -> ') AS full_path, -- 从根到当前节点的路径
    CONNECT_BY_ISLEAF AS is_leaf_node -- 是否为叶节点（1表示是，0表示否）
FROM 
    employees
START WITH 
    manager_id IS NULL -- 指定根节点：从没有经理的员工（即顶层）开始
CONNECT BY 
    PRIOR employee_id = manager_id -- 定义父子关系：父节点的employee_id等于子节点的manager_id
ORDER SIBLINGS BY employee_id; -- 在同级节点内排序
```
# sql扫描方式
全表扫描 FTS
索引范围扫描 Index range scan 
```sql
SELECT name FROM employees WHERE dept_id = 10 AND salary > 50000;
-- 若 dept_id 在索引的最左侧，会使用 index range scan
```
索引快速全扫描
```sql
-- 假设索引 emp_idx(idx_col1, idx_col2) 包含了查询所需列
SELECT idx_col1, idx_col2 FROM employees WHERE idx_col1 IS NOT NULL;
-- 可能触发 index fast full scan 而不回表
```

# 锁的分类
Enqueue 队列锁，业务相关
Latch 系统资源锁

TM锁 锁DDL操作
TX锁 锁会话


# 执行计划
## 直接表的访问
并行方式
多数据块读取

## 数据的关联
nested loop
merge join (排序后loop)
hash join （两表等值条件）

并行处理
PX

# Oracle 优化器
CBO 优化 -- 收集数据库表，列的统计信息，为了优化执行计划 成本的估算（cost）

selectivity 这个列的值有70000个不同的值，选择性高，适合做b-tree索引
cardinality 输出的值的条数
clustering factor 统计index查数据时在不同的数据块中的跳跃

AWR监控，Promesus监控
进程数 会话数 sql_time db_cpu_time cache-hit-ratio wait_time tablespace_bytes 

# RAC
实例部分 数据库部分 组成oracledb

RAC 多实例，一个db 组成rac
数据的传递，锁定的等待

RAC + DataGuard来确保健壮性

# 事务隔离级别











