第3章 Java程序优化
===

## 3.1 字符串优化处理

### 3.1.4 StringBuffer和StringBuilder

StringBuffer是线程安全的，StringBuilder无法保证线程安全。

#### 5.容量参数

无论是StringBuilder和StringBuffer，在初始化时都可以设置一个容量参数，在不指定容量参数时，默认是16字节 

```java
AbstractStringBuilder(int capacity) {
    value = new char[capacity]
}
```

在追加字符串时，如果容量超过实际char数组长度，则需要进行扩容：扩容策略是将容量翻倍，以新容量申请内存空间，建立新的char数组，再将原数组内容复制到新数组，因此，对于大对象的扩容会涉及大量内存复制操作。所以，如果能预先评估StringBuilder大小，能有效地节省操作，提升性能。

```java
StringBuffer sb = new StringBuffer(5888890);
StringBuilder sb = new StringBuilder(5888890);
```

## 3.2 核心数据结构

## 3.3 使用NIO提升性能

### 3.3.2 Buffer的基本原理

Buffer中三个重要参数：position, capacity, limit

```java
ByteBuffer b = ByteBuffer.allocate(15);
b.limit()
b.postion()
b.capacity()
```

### 3.3.3 Buffer的相关操作

#### 1.Buffer的创建
```java
//从堆中分配
ByteBuffer buffer = ByteBuffer.allocate(1024);
//从既有数组中创建
byte array[] = new byte[1024];
ByteBuffer buffer = ByteBuffer.wrap(array);
```

#### 2.重置和清空缓冲区

```java
rewind()：用于提取Buffer的有效数据
clear()：为重写Buffer做准备
flip()：读写模式转化
```

#### 3.读/写缓冲区

#### 4.标志缓冲区

```java
mark()：记录当前位置
reset()：恢复到mark所在位置
```

#### 5.复制缓冲区

`public ByteBuffer duplicate()`：新生成的缓冲区和原缓冲区共享相同的内存数据，新旧缓冲区独立维护各自的position, limit, mark，但新缓冲区对内存数据做写操作，原Buffer相同位置也会有相同变化

#### 6.缓存区分片

`slice()`：将在现有的缓冲区，创建新的子缓冲区，并与父缓冲区共享数据。在子缓冲区修改数据，读取父缓冲区会看到这些变化

#### 7.只读缓冲区

```java
ByteBuffer b = ByteBuffer.alllocate(15);
ByteBuffer readOnly = b.asReadOnlyBuffer();
```

只读缓冲区有效保证核心数据安全，试图对只读缓冲区做修改，会抛出java.nio.ReadOnlyBufferException。修改原缓冲区，只读缓冲区也会修改，因为是共享内存块

#### 8.文件映射到内存

NIO提供一种将文件映射到内存的方法进行I/O操作，它比常规的基于流I/O快很多，主要由`FileChannel.map()`实现

`MappedByteBuffer mbb = fc.map(FileChannel.MapMode.READ_WRITE, 0, 1024);`以上代码将文件前1024个字节映射到内存

#### 9.处理结构化数据

散射（Scattering）和聚集（Gathering）,散射是将数据读入一组Buffer，而不仅仅是一个，聚集是将数据写入一组Buffer中

例如，对一个格式固定的文件，可以构造若干个文件结构的Buffer，通过散射读可以一次将内容装配到各个对应的Buffer中;如果创建指定格式的文件，只要先构造好大小合适的Buffer对象，使用聚集写的方式，可以很快创建出文件

### 3.3.4 MappedByteBuffer性能评估

结论：使用MappedByteBuffer可以大大提高读取和写入文件的速度，实际开发中可以适当使用这种方式

### 3.3.5 直接访问内存

`DirectBuffer`：继承自ByteBuffer，直接分配在物理内存中，不占用堆空间，操作速度更快，但是创建和销毁DirectBuffer花费远高于ByteBuffer

申请DirectBuffer的方法如下：`ByteBuffer.allocateDirect()`，可以使用MaxDIrectMemorySize指定DirectBuffer最大可用空间，-Xmx指定最大堆空间（ByteBuffer）

## 3.4 引用类型

Java有四个级别的引用：强引用，软引用，弱引用和虚引用

### 3.4.1 强引用

强引用可直接访问目标对象，强引用所指对象在任何时候都不会被回收

### 3.4.2 软引用

一个持有软引用的对象，不会被JVM回收，JVM会根据当前堆的使用情况判断，堆使用率临近阀值就回收

### 3.4.3 软引用

在系统GC时，只要发现弱引用，不管堆空间是否足够，都会将对象回收。但是由于垃圾回收器的线程优先级较低，并不一定能很快发现持有弱引用对象

### 3.4.4 虚引用

一个持有虚引用的对象，和没有引用几乎是一样的，随时都可能被垃圾回收器回收

## 3.5 有助于改善性能的结构

### 3.5.1 慎用异常

一旦try-catch语句被用于循环之中，就会给系统带来极大的伤害，所以，尝试把try-catch放到循环之外

### 3.5.2 使用局部变量

调用方法时传递的参数以及在调用中创建的临时变量保存在Stack中，速度较快。其他变量，如静态变量，实例变量都在Heap中，速度较慢

### 3.5.3 位运算代替乘除法

`a<<1, a>>1`代替`a*=2, a/=2`

### 3.5.4 替换switch

尽量减少判断分支，比如用数组代替switch语句

### 3.5.5 一维数组代替二维数组

一维数组的访问速度优于二维数组，因此，可以尝试通过可靠的算法将二维数组转化为一维数组

### 3.5.6 提取表达式

程序员很容易有意无意地让代码做一些“重复劳动”，可以尝试提取重复代码中公共部分，尽可能减少程序的重复计算。尤其是在循环体内的代码，从循环体内提取重复的代码到循环体外，可以有效提升系统性能

### 3.5.7 展开循环

笔者认为展开循环是一种极端情况下使用的优化手段，因为展开循环可能会影响代码的可读性和可维护性

```java
for(int i=0; i<100; i++) {
    a[i]=i;
}
```

展开为

```java
for(int i=0; i<100; i+=3) {
    a[i]=i;
    a[i+1]=i+1;
    a[i+2]=i+2;
}
```

### 3.5.8 布尔运算代替位运算

布尔运算中，只要表达式的值可以确定，就会立即返回，而跳过剩余子表达式的计算

### 3.5.9 使用arrayCopy()

数组复制是一项使用频率很高的功能，JDK提供一个高效的API实现：

`public static native void arraycppy(Object src, int srcPos, Object dest, int destPos, int length)`

`System.arraycopy()`函数是native函数，通常native函数性能优于普通函数

### 3.5.10 使用Buffer进行I/O操作

除了NIO外，使用Java进行I/O操作的方式有两种基本方式：

- 使用给基于InputStream和OutputStream的方式
- 使用Writer和Reader

```bash
OutputStream --> FileOutputStream --> BufferedOutputStream
InputStream --> FileInputStream --> BufferedInputStream
Writer --> FileWriter --> BufferedWriter
Reader --> FileReader --> BufferedReader
```

无论对于读取还是写入文件，适当地使用缓存，可以提升性能

### 3.5.11 使用clone代替new

在Java中新建对象实例最常用的方法是new，使用new创建轻量级对象时，速度非常快。但是，对于重量级对象，由于可能在构造函数中进行一些复杂且耗时的操作，耗时较长，为了解决这个问题，可以使用Object.clone()，这可以绕过对象构造函数，快速复制一个对象实例，但是，默认情况下，clone()方法只是原对象的浅拷贝，如果需要深拷贝，则需要重现实现clone()方法

`Student stu2 = stu1.newInstance()`：克隆对象拥有和原始对象相同的引用，而不是值拷贝，即浅拷贝

### 3.5.12 静态方法代替实例方法

对于一些工具类，应该使用static方法实现，不仅可以加速函数调用的速度，也不需要生成类的实例，比调用实例更为方便，易用

