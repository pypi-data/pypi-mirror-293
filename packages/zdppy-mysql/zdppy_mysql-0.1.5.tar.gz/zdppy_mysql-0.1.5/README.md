# zdppy_mysql

使用python操作MySQL

项目开源地址：https://github.com/zhangdapeng520/zdppy_mysql

## 安装

```bash
pip install zdppy_mysql
```

## 使用教程

### 连接MySQL

```python
import zdppy_mysql
from config import host, username, password, database, port

# 连接数据库
db = zdppy_mysql.connect(
    host,
    username,
    password,
    database,
    port,
)
print(db)
```

### 添加数据库

```python
import zdppy_mysql
from config import host, username, password, database, port

# 连接数据库
db = zdppy_mysql.connect(
    host,
    username,
    password,
    database,
    port,
)

# 使用游标对象执行SQL语句
with db.cursor() as cur:
    # 创建数据库
    sql = "create database if not exists test"
    cur.execute(sql)

    # 查询所有数据库
    sql = "show databases"
    cur.execute(sql)
    print(cur.fetchall())
```

### 查询所有表

```python
import zdppy_mysql
from config import host, username, password, database, port

# 连接数据库
db = zdppy_mysql.connect(
    host,
    username,
    password,
    database,
    port,
    cursorclass=zdppy_mysql.cursors.DictCursor,
)

# 使用游标对象执行SQL语句
with db.cursor() as cur:
    # 查询所有数据库
    sql = "show tables"
    cur.execute(sql)
    print(cur.fetchall())
```

### 添加表

```python
import zdppy_mysql
from config import host, username, password, database, port

# 连接数据库
db = zdppy_mysql.connect(
    host,
    username,
    password,
    database,
    port,
    cursorclass=zdppy_mysql.cursors.DictCursor,
)

# 使用游标对象执行SQL语句
with db.cursor() as cur:
    # 查询所有数据库
    sql = "create table user(id int primary key auto_increment, name varchar(255))"
    cur.execute(sql)
    db.commit()
```

### 添加数据

```python
import zdppy_mysql
from config import host, username, password, database, port

# 连接数据库
db = zdppy_mysql.connect(
    host,
    username,
    password,
    database,
    port,
    cursorclass=zdppy_mysql.cursors.DictCursor,
)

# 使用游标对象执行SQL语句
with db.cursor() as cur:
    cur.execute("insert into user(name) values(%s)", ("张三1",))
    cur.execute("insert into user(name) values(%s)", ("张三2",))
    cur.execute("insert into user(name) values(%s)", ("张三3",))

    # 必须加commit才会提交到数据库保存
    db.commit()
```

### 查询所有数据

```python
import zdppy_mysql
from config import host, username, password, database, port

# 连接数据库
db = zdppy_mysql.connect(
    host,
    username,
    password,
    database,
    port,
    cursorclass=zdppy_mysql.cursors.DictCursor,
)

# 使用游标对象执行SQL语句
with db.cursor() as cur:
    # 查询所有数据库
    cur.execute("select * from user")
    print(cur.fetchall())
```

## 版本历史

- 0.1.1 解决mysql8初次连接报auth异常的问题
- 0.1.4 移除Database类及其他语法糖，全部移交mcrud处理

### v0.1.5

- 架构优化

## 注意事项

如果报权限异常错误，请手动执行依赖：

```bash
pip install cryptography
```
