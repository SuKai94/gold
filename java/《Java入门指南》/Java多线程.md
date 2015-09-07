###Java榨干CPU之多线程

####1.线程起步

单核系统在给定的时间里只能进行一项任务，但这不影响它的工作，因为它采用时分复用的技术进行多任务的操作

（1）进程：通常每一个程序在开始运行时，都意味这产生了一个进程

（2）线程：轻量级进程，线程从属于进程，每一个进程都至少有一个线程。同一个进程下的线程们，共享进程资源。

####2.怎么创造线程

（1）通过继承Thread类创建线程

```java
import java.util.Date;

public class ThreadTest extends Thread{
	int pauseTime;  //线程睡眠时间
	String name;    //线程名字
	
	public ThreadTest(int x, String n){
		pauseTime = x;
		name = n;
	}
	
	//必须覆写的父类方法，线程的入口方法
	public void run(){
		while(true){
			try{
				System.out.println(name + ":" + new Date(System.currentTimeMillis()));
				Thread.sleep(pauseTime);
			}catch(Exception e){
				System.out.println(e);
			}
		}
	}
	
	public static void main(String args[]){
		ThreadTest tp1 = new ThreadTest(3000, "慢的线程");
		tp1.start();
		ThreadTest tp2 = new ThreadTest(1000, "快的线程");
		tp2.start();
	}
}
```

(2)通过实现Runnable接口创建线程
```java
//注意这里是implements
public class ThreadTest implements Runnable{
	int pauseTime;  //线程睡眠时间
	String name;    //线程名字
	
	public ThreadTest(int x, String n){
		pauseTime = x;
		name = n;
	}
	
	//必须覆写的父类方法，线程的入口方法
	public void run(){
		while(true){
			try{
				System.out.println(name + ":" + new Date(System.currentTimeMillis()));
				Thread.sleep(pauseTime);
			}catch(Exception e){
				System.out.println(e);
			}
		}
	}
	
	public static void main(String args[]){
		//注意这里只能用Thread类来new一个线程对象
		Thread tp1 = new Thread(new ThreadTest(3000, "慢的线程"));
		tp1.start();
		Thread tp2 = new Thread(new ThreadTest(1000, "快的线程"));
		tp2.start();
	}
}
```
（3）如何选择最符合的创建方式

两者不同在于一个用继承，一个用接口。这只是导致了new线程的时候的小小不同：对于继承而言，直接用自己的类名new就行，但是接口只能用Thread类new一个线程对象

最好选择Runnable---因为java的单根继承

####3.我想排到前面去

java通过给各个任务分等级的机制，以便控制线程在排队大战中得到一个好位置。这个休闲级式1～10之间的一个数字，数字越大表示任务的优先级越高

线程的优先级指定是通过调用`setPriority()`实现的，如：`tp1.setPriority(10);`

看下面代码的执行顺序：
```java
public class ThreadTest implements Runnable{
	String name;    //线程名字
	
	public ThreadTest(String n){
		name = n;
	}
	
	//必须覆写的父类方法，线程的入口方法
	public void run(){
		try{
			System.out.println(name + ": 正在执行！");
		}catch(Exception e){
			System.out.println(e);
		}
	}
	
	public static void main(String args[]){
		Thread tp1 = new Thread(new ThreadTest("第一个线程"));
		tp1.start();
		Thread tp2 = new Thread(new ThreadTest("第二个线程"));
		tp2.start();
		Thread tp3 = new Thread(new ThreadTest("第三个线程"));
		tp3.start();
		Thread tp4 = new Thread(new ThreadTest("第四个线程"));
		tp4.start();
	}
}
```
上面代码的执行顺序是不可知的，因为他们同属一个优先级，java运行同一优先级的任务比较随意

请记住，虽然java支持10个优先级，但是并不代表这10个优先级一定会起作用，因为最终依赖于各操作系统的运行策略，所以优先级并不是一个可靠的工具，在任何情况下，都不赞成这种做法

####4.维持线程秩序---线程的控制

（1）中断线程

- 发出中断：调用线程的`interrupt()`方法，告诉线程中断运行，如：`tp1.interrupt()`

- InterruptedException：处于不同状态的线程，得到的信号也会不一样。当一个线程正处于调用sleep()后的睡眠期或者wait()方法后的等待时期，线程会捕捉到一个InterruptedException的异常，因此需要对中断处理的代码写在catch区块内，
```java
try{
	Thread.sleep(4000);
}catch(InterruptedException e){
	//在此处理中断信号，一般是退出线程的执行
	return;
}
```

- Thread.interrupted()：并不是所有的方法调用和代码都会抛出InterruptedException，所以：
```java
if(Thread.Interrupted){
	//如果中断标志为true，写上处理代码
	return;
}
```
如果没有InterruptedException异常，就可以使用Thread.Interrupted()方法判断是否被指示要中断执行

(2)join方法---让线程更有序
```java
public class ThreadTest implements Runnable{
	String name;    //线程名字
	
	public ThreadTest(String n){
		name = n;
	}
	
	//必须覆写的父类方法，线程的入口方法
	public void run(){
		try{
			System.out.println(name + ": 正在执行！");
		}catch(Exception e){
			System.out.println(e);
		}
	}
	
	public static void main(String args[]){
		Thread tp1 = new Thread(new ThreadTest("第一个线程"));
		tp1.start();
		try{
			tp1.join();
		}catch(InterruptedException e){
			e.printStackTrace();
		}
		Thread tp2 = new Thread(new ThreadTest("第二个线程"));
		tp2.start();
		try{
			tp2.join();
		}catch(InterruptedException e){
			e.printStackTrace();
		}
		Thread tp3 = new Thread(new ThreadTest("第三个线程"));
		tp3.start();
		try{
			tp3.join();
		}catch(InterruptedException e){
			e.printStackTrace();
		}
		Thread tp4 = new Thread(new ThreadTest("第四个线程"));
		tp4.start();
		try{
			tp4.join();
		}catch(InterruptedException e){
			e.printStackTrace();
		}
	}
}
```
(3)sleep()

(4)yield()---当线程调用此方法，意为暂停运行，并自动降低优先级，以便让于自己同等级的线程得到运行

####5.守护线程

- 用户线程：所有用户线程结束后，JVM才会退出

- 守护线程：一种服务线程，为用户线程提供服务。当所有用户线程结束后，守护线程随着JVM一起退出

将用户线程转化为守护线程：`setDaemon()`，将tp1线程设置为守护线程:`tp1.setDaemon(true)`，可以用`isDaemon()`检查

`setDaemon()`只能在`start()`前使用，若在之后使用，则会返回一个SecurityException异常

####6.线程的同步

（1）直接上代码
```java
//银行帐号类
public class Account{
	String holderName;
	float amount;

	public Account(String name, float amt){
		holderName = name;
		amount = amt;
	}
	//存款，加了同步限制
	public synchronized void deposit(float amt){
		amount += amt;
	}
	//取款，加了同步限制
	public synchronized void withdraw(float amt){
		amount -= amt;
	}
}
```
加了synchronized，该关键字的作用是创建一把同步锁，在锁的作用下，同一个时间只能被一个线程所访问，有效地避免了多个线程同时读取修改产生的混乱

（2）给代码块加锁

```java
public void deposit(float amt){
	synchronized(amount){
		amount += amt;
    }
}
```
这将加锁的范围缩的更细微一点， 锁性能损耗便越小，这是最好的做法。synchronized关键字用来锁代码块时，需要指定一个对象（不可以是非对象）