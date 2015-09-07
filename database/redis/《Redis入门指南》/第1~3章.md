[《Redis入门指南》](http://book.douban.com/subject/24522045/)
===

### 第一章 简介
#### 1.2 特性 
一款个人开发数据库

#### 1.2.1 存储结构
Redis是Remote Dictionary Server(远程字典服务器)的缩写，以字典结构存储数据，并允许其他应用通过TCP协议读写字典中的内容。字典中的键值除了字符串，还可以是其余数据类型。目前，Redis支持：
- 字符串类型
- 散列类型
- 列表类型
- 集合类型
- 有序集合类型

优势是查询数据库数据时，无需将几个相关表join在一起，字典结构的存储方式和对多种键值数据类型的支持使得开发者可以将程序中数据直接映射到Redis中，另一个优势是可以进行交集，并集这样的集合操作。

#### 1.2.2 内存存储与持久化
redis数据都存储在内存中，并且内存读写速度比硬盘快很多。但存在一个问题：程序退出后内存中的数据将会丢失，不过redis提供了持久化的支持，可以将内存中的数据异步写入到硬盘中，同时不影响继续提供服务。

#### 1.2.3 功能丰富
redis虽然是作为数据库开发的，但是由于其丰富的功能，更多人将其作为缓存，队列系统。redis可以为每个键设置生存时间(TTL)，生存时间到了就自动被删除，这一功能配合出色的性能让redis作为缓存系统使用，而且redis支持持久化和丰富数据类型，使其成为Memcached的有力竞争者。

但是Memcached支持多线程，redis是单线程模式，前者在多核服务器上性能更高。作为缓存系统，redis还可以限定数据占用的最大内存空间，在数据达到空间限制后，按照一定的规则自动淘汰不需要的键。

初次之外，redis的列表类型可以用来实现队列，并且支持阻塞式读取，可以很容易实现一个高性能的优先级队列。

#### 1.2.4 简单稳定
redis使用命令来读取数据，将相当于SQL语句。redis还提供了几十种不同编程语言的客户端库，这些库都很好地封装了redis命令，使得在程序中更好的和redis交互

### 第二章 准备
#### 2.1 安装
#### 2.2 启动和停止redis
安装完redis的下一步就是启动它，先来看看redis包含的可执行文件有哪些：
- redis-server：redis服务器
- redis-cli：redis命令行客户端
- redis-benchmark：redis性能测试工具
- redis-check-aof：AOF文件修复工具
- redis-check-dump：RDB文件检查工具

#### 2.2.1 启动redis
有：直接启动和初始化脚本启动两种方式，分为适用于开发环境和生产环境

1.直接启动：redis-server，默认端口是6379，可以通过redis-server --port 8888指定端口
2.初始化脚本启动redis，在redis源代码目录的utils文件夹下有一个名为redis_init_script的初始化脚本

#### 2.2.2 停止redis
考虑到redis有可能在将内存数据同步到硬盘，强制终止redis可能会造成数据丢失，正确的是发送shutdown命令：

```bash
redis-cli shutdown
```

当redis接受到shutdown之后，会先断开所有客户端连接，然后根据配置执行持久化，最后完成退出。redis也可以妥善处理sigterm信号，所以使用“kill redis进程id”也可以达到同样效果

#### 2.3 redis命令行客户端
是我们学习和测试redis的重要工具

#### 2.4 配置
我们之前通过redis-server的启动参数port设置了redis的端口号，除此之外，redis还支持其他配置选项，如是否开启持久化，日志级别等。由于配置的选项较多，通过启动参数设置这些选项并不方便，所以redis支持通过配置文件来设置这些选项。

```bash
redis-server /path/to/redis.conf
```

通过启动参数传递同名的配置文件选项会覆盖配置文件中相应的参数：

```bash
redis-server /path/th/redis.conf --loglevel warning
```

redis提供了配置文件的模板redis.conf，在源代码目录的根目录。除此之外，还可以在redis运行时通过config set命令在不重新启动redis的情况下动态修改redis配置。

#### 2.5 多数据库
实际上redis实例提供了多个用来存储数据的字典，客户端可以指定将数据存储在哪个字典中，与我们熟知的一个关系数据库实例可以创建多个数据库类似，所以可以将其中的每个字典都理解成一个独立的数据库。每个数据库从0开始递增数字命名，redis默认支持16个数据库。

然而，又和我们理解的数据库有区别：redis不支持自定义数据库名，也不支持为每个数据库设置密码，所以一个客户端要么可以访问全部数据，要么一个访问权限都没有。更重要的一点是，多个数据库之间并不是完全隔离的，不同的应用应该使用不同的redis实例，而非不同的数据库。

### 第三章 入门
#### 3.1 热身
#### 3.2 字符串类型
一个字符串类型键允许存储的数据最大容量是512MB。
#### 3.2.2 命令
1.赋值与取值

```bash
set key value
get key
```

2.递增数字

字符串类型可以存储任何形式的字符串，当存储的字符串是整数形式时，redis提供一个incr命令，让当前键值递增，并返回递增后的值：

`incr bar`

#### 3.2.3 实践
文章访问量统计需要生成自赠的ID，在关系型数据库里面，我们可以通过设置字段属性为auto_increment，redis中可以通过另一种模式实现：对于每一类对象使用名为对象类型(复数形式):count的键来存储当前类型对象的数量。

`$ postID = incr posts:count`

#### 3.2.4 命令拾遗
1.增加指定整数

`incrby key increment`

2.减少指定整数

`decr key`

`decrby key increment`

3.增加指定浮点数

`incrbyfloat key increment`

4.向尾部追加值

`append key value`

如果键不存在，就将键值设为value，返回值是追加后字符串的长度

5.获取字符串的长度

`strlen key`

6.同时获取/设置多个键值

`mset key1 v1 key2 v2 ...`

`mget key1 key2 ...`

7.位操作
- `getbit key offset`：获得一个字符串类型键指定位置(offset)的二进制位的值，索引从0开始;如果索引超过了键值的二进制位的实际长度，则默认位值为0
- `setbit key offset value`：设置字符串类型键指定位置的二进制位的值，返回值是该位置的旧值。如果设置的位置超过了键值二进制位的长度，setbit命令将自动将中间的二进制位设置为0，同理设置一个不存在键的指定二进制位的值，将自动将其前面的位赋值为0。
- `bitcount key`：获得字符串类型键中值是1的二进制位个数，可以通过参数限制统计的字节范围，如果只希望统计前两个字节：`bitcount key 0 1`
- `bitop or res key1 kye2`：将字符串key1和key2执行位或操作，将结果存放在res键中。总结就是bitop可以对多个字符串类型键进行位操作，有and,or,xor,not。

利用位操作可以很紧凑地存储布尔值

#### 3.3 散列类型
#### 3.3.1 介绍
散列类型适合存储对象：使用对象类别和ID构成键名，使用字段表示对象属性，而字段值则存储属性值。

![redis散列数据类型举例](https://raw.githubusercontent.com/su-kaiyao/record/master/others/imgs/redis%E6%95%A3%E5%88%97%E7%B1%BB%E5%9E%8B%E4%B8%BE%E4%BE%8B.png)

提示：散列类型和其他数据类型不支持数据类型嵌套，比如散列类型字段值只能是字符串，不支持其他数据类型。

redis并不要求每个键都依据某种结构存储，我们完全可以自由地为任何健增减字段而不影响其他键，如下图为ID为1的汽车增加日期属性。

![redis散列类型增减属性](https://raw.githubusercontent.com/su-kaiyao/record/master/others/imgs/redis%E6%95%A3%E5%88%97%E7%B1%BB%E5%9E%8B%E5%A2%9E%E5%8A%A0%E5%B1%9E%E6%80%A7.png)

#### 3.3.2 命令

1.赋值与取值

```bash
hset key field value
hget key field
hmset key field1 value1 [field2 value2]
hmget key field1 [field2]
hgetall key
```

hset命令是有则更新，并返回0;无则插入，并返回1

2.判断字段是否存在

`hexists key field`，有则返回1，无则0

3.当字段不存在时赋值

`hsetnx key field value`，如果字段已经存在，hsetnx将不执行任何操作。而且这操作是原子性的，不存在竞态条件。

4.增加数字

`hincrby key field increment`：使字段增加指定的整数

5.删除字段

`hdel key field [field...]`，返回值是被删除字段的个数

#### 3.3.3 实践

#### 3.3.4 命令拾遗

1.只获取字段名或字段值

```bash
hkeys key
hvals key
```

2.获得字段数量

`hlen key`

#### 3.4 列表类型
#### 3.4.1 介绍
列表类型可以存储一个有序的字符串列表，常用的操作是向列表两端添加元素，或获得列表的某一个片段。列表内部使用双向链表实现，所以向列表两端添加元素时间复杂度为O(1)，越接近两端的元素获取速度越快。

#### 3.4.2 命令

1.向列表两端增加元素

```bash
lpush key value[ value ...]
rpush key value[ value ...]
```

2.从列表两端弹出元素

```bash
lpop key
rpop key
```

3.获取列表元素的个数

```bash
llen key
```

4.获得列表片段

```bash
lrange key start stop
```
当然也支持负索引，`lrange key -2 -1`，表示从右边开始计算序数，-1表示右边第一个，-2表示右边第二个

如果stop范围大于索引范围，则会返回列表最右边的元素

5.删除列表中指定的值

`lrem key count value`：lrem会删除列表中前count值为value的元素，返回值是实际删除的元素个数。
- 当count>0时，lrem会从列表左边开始删除前count个值为value的元素;
- 当count<0时，lrem会从列表右边开始删除前|count|个值为value的元素;
- 当count=0时，lrem会删除所有值为value的元素;

#### 3.4.5 命令拾遗

1.获得/设置指定索引的元素值

```bash
lindex key index
lset key index value
```

2.只保留列表指定片段
`ltrim key start end`

3.向列表中插入元素
`linsert key before|after pivot value`：linsert首先会在列表中从左到右查找值为pivot的元素，然后更具第二个参数是before还是after来决定将value插到该元素前面还是后面。

4.将元素从一个列表转到另一个列表R
`poplpush source destination`

#### 3.5 集合类型
#### 3.5.2 命令

1.增加/删除元素

```bash
sadd key member [member ...]
srem key member [member ...]
```

2.获得集合中的元素

`smembers key`

3.判断元素是否在集合中

`sismember key member`

4.集合间运算

```bash
#差集
sdiff key [key ...]
#交集
sinter key [key ...]
#并集
sunion key [key ...]
```

#### 3.5.3 命令拾遗

1.获取集合中元素个数

`scard key`

2.进行集合运算，并将结果存储

```
sdiffstore destination key [key ...]
sinterstore destination key [key ...]
sunionstore destination key [key ...]
```

3.随机获取集合中的元素

`srandmember key [count]`

- 当count为正数：会随机从集合里获取count个不重复的元素，如果count值大于集合元素
- 当count为负数：会随机从集合里获取|count|个元素，这些元素有可能相同

4.从集合中弹出一个元素

`spop key`

#### 3.6 有序集合类型
#### 3.6.1 介绍

在集合类型基础上，有序集合类型为集合中每个元素都关联了一个分数。有序集合和列表有些相似，但是二者仍有很大的区别：
- 列表通过链表实现，获取靠近两端的数据速度极快，当元素增多后，访问中间数据的速度就较慢，所以更加适合实现如“新鲜事”和“日志”这样很少访问中间元素的应用。
- 有序集合采用散列表和跳跃表实现，所以即使读取中间位置的元素，速度也很快。
- 列表不能简单调整某个元素的位置，但是有序集合可以。
- 有序集合要比列表更耗费内存。

#### 3.6.2 命令

1.增加元素

`zadd key score member [score member]`

其中+inf和-inf表示正无穷和负无穷

2.获取元素的分数

`zscore key member`

3.获得排名在某个范围的元素列表

`zrange key start stop [withscores]`：按照元素分数从小到大的顺序返回索引从start到stop之间的所有元素(包含两端元素);如果需要同时获得元素的分数的话，就可以在命令尾部加上withscores参数。如果两个元素分数相同，就按照字典顺序排列。

`zrevrange key start stop [withscores]`：唯一不同在于，zrevrange命令是按照从大到小的顺序给出结果的。

4.获得指定分数范围的元素

`zrangebyscore key min max [withscores] [limit offset count]`：该命令按照元素分数从小到大顺序返回分数在min和max之间(包含min和max)的元素;如果希望分数范围不包含断点值，可以在分数前加上“(”符号;在本命令中limit offset count就是指在获得元素的基础上向后偏移offset个元素，并且只获取前count个元素。

`zrevrangebyscore key min max [withscores] [limit offset count]`：不仅是按照元素分数从大到小的顺序给出结果的，而且它的min和max参数顺序也是相反的

5.增加某个元素的分数

`zincrby key increment member`

#### 3.6.4 命令拾遗

1.获得集合中元素的数量

`zcard key`

2.获得指定分数范围内元素的个数

`zcount key min max`

3.删除一个或多个元素

`zrem key member [member ...]`

4.按照排名范围删除元素

`zremrangebyrank key start stop`

5.按照分数范围删除元素

`zremrangebyscore key min max`

6.获得元素的排名

```bash
zrank key member #按照元素从小到大顺序获得指定元素的排名，从0开始
zrevrank key member #相反
```

7.计算有序集合的交集

`zinterstore destination numkeys key [key ...] [weights weight [weight ...]] [agregate sum[min][max]]`

- (1)当aggregate是sum时（默认值），destination键中元素的分数是每个参与计算的集合中该元素的分数之和
- (2)min,就是各个参与计算元素分数的最小值
- (3)max,............................大.





