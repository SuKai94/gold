mongoDB基本使用
===

### 数据写入与查询

```
show dbs
use xxx
db.dropDatabase()
```

mongoDB表亦称为集合，插入操作传参是json格式参数

```
db.xxx.insert({x: 1})
```

查询所有集合（亦或称为表）

```
show collections(tables)
```

数据查询

```
db.xxx.find()
db.xxx.find({x: 1})
db.xxx.find().count()
```

查询结果过滤前三条，显示2条，按照x值正向/逆向排序

```
db.xxx.find().skip(3).limit(2).sort({x: 1})
db.xxx.fing().skip(3).limit(2).sort({x: -1})
```

### 数据更新

```
db.xxx.update({x: 1}, {x: 999})
```

```
db.xxx.insert({x: 100, y: 100, z: 100})
```

将z为100的数据中的y变为2：

```
db.xxx.update({z: 100}, {$set: {y: 2}})
```

更新不存在数据，默认不会插入该数据，除非：

```
db.xxx.update({y: 1000}, {y: 9}, true)
```

更新多条数据时，默认只会更新第一条找到的数据，若想同时更新所有符合条件数据：

```
db.xxx.update({c: 1}, {$set: {c: 2}}, false, true)
```

### 数据删除

remove()函数必须传入参数

```
db.xxx.remove({c: 2})
```

删除表

```
db.xxx.drop()
```

### 创建索引

查看当前索引情况

```
db.xxx.getIndexes()
```

创建索引

```
db.xxx.ensureIndex({x: 1})
```

1表示正向创建索引，-1表示逆向创建索引



