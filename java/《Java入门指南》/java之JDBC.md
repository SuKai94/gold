###Java通向数据库的桥---JDBC
[参考戳这里](http://blog.csdn.net/cxwen78/article/details/6863696)

####1.JDBC简介

JDBC是一组比较核心的Java API，就两个方面对JDBC做简介，一方面是JDBC组成部分，另一方面是JDBC的架构

（1）JDBC组件：

- JDBC API：其提供了一套从Java语言中对关系数据库进行访问的办法。使用JDBC API，程序可以执行SQL指令，获取SQL查询结果，并且可以对关系型数据库中的数据进行修改与删除

- JDBC Driver Manager：JDBC在操作各种数据库时，会用数据库相应的驱动来进行实质性的操作

（2）JDBC与架构

Java是最喜欢讲架构的，说到架构就一定会有分层，此处列举一下JDBC在两层和三层的架构中处于什么位置

```
JAVA应用程序||JDBC <----DBMS访问协议----> DBMS
JAVA客户程序/web浏览器 <----HTTP/SOCKET...----> JAVA应用程序||JDBC <----DBMS访问协议----> DBMS
```

####2.正确获取JDBC驱动程序

下载[驱动程序](http://www.mysql.com/products/connector/)，将压缩包里面的Jar包提取出来（注意一定要是jar包，而不是任何格式的压缩包）

在Eclipse创建项目，并添加mysql驱动程序，创建的项目类型可以是java项目或者式java web项目，添加驱动程序可能添加不成功，要确保包被导入工程里面，这里注意：

- 如果是web工程，那么只需要把jar包拷贝到lib目录下

- 如果是java工程，那么将添加到工程的`build path`，`add external jars`

####3.使用JDBC API操作数据库

mysql建表如下：
```sql
create table student 
( 
id int not null,
name varchar(10) not null,
age int not null,
primary key (id) 
);
```

JDBC提供了不少好用的类，这些类满足数据库访问的所有需求，这使得程序们能够更加快捷地进行数据库编程

(1)打开数据库的Connection

通过加载指定的驱动创建连接---创建连接的第一步是要加载相应的驱动，加载相应驱动的代码是很简单的
`Class.forName("com.mysql.jdbc.Driver")`

`com.mysql.jdbc.Driver`是mysql数据库驱动类的类名，调用`Class.forName()`会创建一个驱动类的对象，并且将这个对象注册到DriverManager

在加载了驱动类之后，就着手创建连接
`conn = DriverManager.getConnection(url, "用户名", "密码")`

(2)执行指令的Statement

Statement对象用于将SQL语句发送到数据库中，并可以取得SQL语句在数据库中的执行的结果

- Statement：最常用的，用于执行不含任何参数的SQL语句，提供对数据的查询和更改操作

- PreparedStatement：继承字Statement，用于执行带参数的SQL语句

- CallableStatement：继承自PreparedStatement，用于调用数据库提供的存储过程

获得了Statement对象之后，可以用3种方式发送SQL语句

- executeQuery()：提供select语句相关功能

- executeUpdate()：提供对数据库的更改操作，比如：insert,update,delete

- execute()：较通用的执行方式，支持返回多个记录集

####4.实战代码---代码才是王道
```java
package test;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.ResultSet;

public class JDBCTest {
	
	//创建静态全局变量
	static Connection conn;
	static Statement st;
	
	public static void main(String[] args){
		insert();  //插入
		query();
		update();  //更新
		delete();  //删除
		query();   //查询记录
	}
	
	public static void insert(){
		conn = getConnection();
		try{
			String sql = "insert into person(id, name, age)" + "values(1, 'kaiyao', 22)";
			st = (Statement) conn.createStatement();
			int count = st.executeUpdate(sql);
			System.out.println("向person表中插入" + count + "条数据");
			conn.close();
		}catch(SQLException e){
			System.out.println("插入数据失败，" + e.getMessage());
		}
	}
	
	public static void update(){
		conn = getConnection();
		try{
			String sql = "update person set age = 23 where name = 'kaiyao'";
			st = (Statement)conn.createStatement();
			int count = st.executeUpdate(sql);
			System.out.println("person表中更新 " + count + "条数据");
			conn.close();
		}catch(SQLException e){
			System.out.println("更新数据失败");
		}
	}
	
	public static void query(){
		conn = getConnection();
		try{
			String sql = "select * from person";
			st = (Statement)conn.createStatement();
			ResultSet rs = st.executeQuery(sql);
			while(rs.next()){
				int id = rs.getInt("id");
				String name = rs.getString("name");
				int age = rs.getInt("age");
				System.out.println(id + " " + name + " " + age);
			}
			conn.close();
		}catch(SQLException e){
			System.out.println("查询数据失败");
		}
	}
	
	public static void delete(){
		conn = getConnection();
		try{
			String sql = "delete from person where name = 'kaiyao'";
			st = (Statement)conn.createStatement();
			int count = st.executeUpdate(sql);
			System.out.println("从person表中删除 " + count + "条数据");
			conn.close();
		}catch(SQLException e){
			System.out.println("删除数据失败");
		}
	}
	
	public static Connection getConnection(){
		Connection conn = null;
		try{
			Class.forName("com.mysql.jdbc.Driver");
		}catch(ClassNotFoundException e){
			e.printStackTrace();
		}
		
		try{
			conn = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/javatest", "sk", "12345");
		}catch(Exception e){
			e.printStackTrace();
		}
		return conn;
	}

}
```


