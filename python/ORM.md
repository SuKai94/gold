ORM
===

### ORM背景知识

Object Relational Mapping, 对象关系映射

ORM，随着面向对象的软件开发方法发展而产生的；关系数据库是企业级应用环境中永久存放数据的主流数据存储系统。对象和关系数据是业务实体的两种表现形式，业务实体在内存中表现为对象，在数据库中表现为关系数据。内存中的对象存在关联和继承关系，而在数据库中，关系数据库无法直接表达多对关联和继承关系。因此，对象-关系映射(ORM)则一般以中间件的形式存在，主要实现程序对象到关系数据库数据的映射。


### [QuickORM](https://github.com/2shou/QuickORM)源码剖析

这是一个100行代码实现的ORM，使用Mysqldb库对Mysql进行操作

#### `Database`类

三个类方法(@classmethond)`：

- `connect(cls, **db_config)`：连接到数据库
- `get_conn(cls)`：返回一条与数据库的连接
- `execute(cls, *args)`：执行SQL操作

一个实例方法：

- `__del__(self)`：在实例对象销毁时，关闭数据库连接

#### `execute_raw_sql(sql, params=None)`函数

最终还是调用`Database.execute(sql, params)`

#### `Field`类

pass

#### 元类`MetaModel`

元类有两个属性`db_table = None`, `fields = {}`

元类控制所有Model子类的创建，使得最终形成的类均有fields属性，fields里面存放键值对，键是Model子类的属性名，值是属性对应的值(全是Field类的对象，否则元类会过滤掉该属性)

#### `Model`类

一个对象方法：

- `save(self)`：进行插入操作

一个类方法：

- `where(cls, **kwargs)`：返回`Expr(cls, kwargs)`

#### `Expr`类

构造函数

- `__init__(self, model, kwargs)`：model是一个Model子类，赋值给self.model；kwargs是实际需要使用的各类参数，self.params = kwargs.values()；最终生成self.where_expr，即where a = %s and b = %s and ....

三个实例方法：

终于元类的作用体现了，会用到元类生成的fields属性

- `select(self)`：查询操作，根据查询结果的多少返回Model子类对象们的列表
- `count(self)`：计数操作
- `update(self, **kwargs)`：更新操作

#### Over

还是很易懂的

[寥雪峰老师](http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001402228705570c9506d546a3349c6b7d64135127672fe000)也编写过ORM，代码量虽较QuickORM多，但功能绝对更强大，代码写的也很骚

---

参考链接

- 百度百科
- [Github QuickORM](https://github.com/2shou/QuickORM)
