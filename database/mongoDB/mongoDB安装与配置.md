mongoDB安装与配置
===

### mongoDB文件介绍

- mongod：数据库执行程序
- mongo：连接数据库的客户端
- mongoimport和mongoexport：数据库导入导出工具
- mongodump和mongorestore：与上述导入导出类似，不同的是基于二进制数据，用作数据备份与恢复
- mongoooplog：操作日志的回放
- mongostat：查询mongo服务器的状态

### 搭建简单的mongoDB服务器

所有操作在私人工作目录下进行，如/MyMongoDB

首先在目录下创建四个子目录：bin, conf, data, log

在conf目录下创建`mongod.conf`配置文件：

```
port = 12345
dbpath = data
logpath = log/mongod.log
fork = true
```

将下载或者编译好的mongod可执行文件复制到bin/下

`./bin/mongod -f conf/mongod.conf`，即可在后台(由于mongod.conf里面配置fork=true)启动mongDB数据库服务

### 连接mongoDB服务器

简单地，使用编译生成的mongo客户端进行连接，将mongo复制到bin/

`./bin/mongo --help`查询帮助信息

连接本地test数据库`./bin/mongo 127.0.0.1:12345/test`

### 关闭mongoDB服务

客户端连接时，使用`db.shutdownServer()`命令行关闭, 使用前需`use admin`

或

使用`kill -15`删掉相应进程
