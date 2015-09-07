##Java进阶之输入输出系统

1.字节数据流：是最基础的流，输入输出的过程中，它以8位的字节为操作单元。所有的字节流都派生自InputStream类和OutputStream类。
```java
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;

public class ByteStreamTest{
	
	public class void main(String[] args){
		FileInputStream in = null;
		FileOutputStream out = null;

		String path = "xxx";

		try{
			in = new FileInputStream(path+"I/O文本.txt");
			out = new FileOutputStream("path+"I/O文件副本.txt");
			int c;
			while((c = in.read()) != -1){
				out.write(c);
			}
		} 
		catch(FileNotFound){
			e.printStackTrace();
		}
		catch(IOException){
			e.printStackTrace();
		}
		finally{
			try{
				if(in != null) in.close();
				if(out ! null) out.close();
			}
			catch(IOException e){
				e.printStackTrace();
			}
		}
	}
}
```
应该尽量避免使用字节流进行操作。字节流是一个比较低层次的流类型，并不适合针对性的流处理，以示例中的文件为例，因为包含着大量字符，更适合选择字符流进行处理

字节流是一个基础的流类型，其他的流类型都是基于字节流存在的。在一些非常原始的环境下字节流最管用，例如针对原始的硬件接口进行I/O操作

2.字符流：所有的字符流类都派生自Reader类和Writer类
```java
import java.io.FileReader;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;

public class CharacterStreamTest{
	
	public class void main(String[] args){
		FileReader in = null;
		FileWriter out = null;

		String path = "xxx";

		try{
			in = new FileReader(path+"I/O文本.txt");
			out = new FileWriter("path+"I/O文件副本.txt");
			int c;
			while((c = in.read()) != -1){
				out.write(c);
			}
		} 
		catch(FileNotFound){
			e.printStackTrace();
		}
		catch(IOException){
			e.printStackTrace();
		}
		finally{
			try{
				if(in != null) in.close();
				if(out ! null) out.close();
			}
			catch(IOException e){
				e.printStackTrace();
			}
		}
	}
}
```
单从表面上，与字节流太相似了。所有的操作都是以字符为操作单元进行，汉字可以作为一个整体一个一个地读入与写出，不会再和字节流一样需要拆分进行

将字节流转换为字符流：Java提供了两个类，来方便在取到字节流的时候，将其处理为字符流：InputStreamReader和OuputStreamWriter。在进行socket开发的时候，你们将体会这带来的好处

如何实现以行为单位的处理：
```java
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;

public class LineOrientedTest{
	
	public class void main(String[] args){
		BufferedReader in = null;
		PrintWriter out = null;

		String path = "xxx";

		try{
			in = new BufferedReader(path+"I/O文本.txt");
			out = new PrintWriter(path+"I/O文件副本.txt");
			int c;
			while((c = in.readLine()) != null){
				out.println(c);
			}
		} 
		catch(FileNotFound){
			e.printStackTrace();
		}
		catch(IOException){
			e.printStackTrace();
		}
		finally{
			try{
				if(in != null) in.close();
				if(out ! null) out.close();
			}
			catch(IOException e){
				e.printStackTrace();
			}
		}
	}
```

3.缓冲数据流：如果想要有效地提升性能，首要的就是减少对底层I/O的直接访问，所以java特意准备了缓冲流处理此种情况

缓冲流采取了缓冲策略来减少对底层I/O的访问，在读取数据的时，缓冲流优先从缓冲读取数据，只有当缓冲区没有数据时，才触发到底层的I/O访问;在写出数据时，缓冲流优先将数据写到缓冲z区，当缓冲区满时，才触发到底层I/O的访问。这样，就不至于在每回进行极少数据的输入输出时都引起对底层I/O的访问，提高了效率

java提供了四种缓冲流，分别对应字节与字符的输入输出：BufferedInputStream和BufferedOutputStream用于创建基于字节流的缓冲流;BufferedReader和BufferedWriter基于字符流的缓冲流

几乎所有的非缓冲流都可以被转换为缓冲流，方法就是：以非缓冲流为参数构造缓冲流：
```java
in = new BufferedReader(new FileReader(path+"xx.txt"));
out - new BUfferedWriter(new FileWriter(path+"xx.txt"));
```
对于输出的缓冲流：清空缓冲区的操作：`flush()`，目的是将已写入到缓冲区的输出数据提前写入物理目标中，无论缓冲区有没有满，同时将缓冲区的数据清空

4.命令行上输入和输出

标准流
```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class CommandLineTest{
	
	public class void main(String[] args){
		InputStreamReader stdin = new InputStreamReader(System.in);
		BufferedReader bufin = new BufferedReader(stdin);

		System.out.print("请输入： ");

		try{
			String str = bufin.readLine();
			System.out.println("你输入的是：" + str);
		} 
		catch(FileNotFound){
			e.printStackTrace();
		}
		catch(IOException){
			e.printStackTrace();
		}
	}
}
```

5.一步一步学文件操作：
```java
import java.io.File;

public class DirTest{
	
	public static void main(String[] args){
		String path = "xxx";
		File dir = new File(path);
		dir.mkdir();            //创建一个文件夹
		dir.delete();           //删除文件夹（如果有子文件夹和文件，不会被删除，也不会抛出异常）
		/*列出文件内的文件明细*/
		String[] childs = File.list();
		for(String name: childs){
			System.out.println(name); //循环输出文件名
		}
	}
}
```
6.Serializable接口的使用：当类实现了此接口，宣告了类的对象可被串行化，就是说可以被放入输入输出流中进行操作
```java
import java.io.Serializable;

class Dog implements Serializable{
	
	private static final long serialVersionUID = 20140614L;
	public String name;
	public String color;
	public transient String temp;   //此属性不会被串行化

	pubic Dog(String name, String color, String temp){
		...
	}
}

//把对象写到硬盘上
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOuputStream;

public class SerializableTest{
	
	public static void main(String[] args){
		Dog d = new Dog(...);
		String path = "xxx";
		FileOutputStream fos = null;
		ObjectOutputStream oos = null;
		FileInputStream fis = null;
		ObjectInputStream ois = null;
		try{
			fos = new FileOutputStream(path);
			oos = new ObjectOutputStream(fos);
			oos.writeObject(d);

			fis = new FileInputStream(path);
			ois = new ObjectInputStream(fis);

			Dog oi = (Dog)(ois.readObject());
		}
		catch(...){
			...
		}
	}
}
```



