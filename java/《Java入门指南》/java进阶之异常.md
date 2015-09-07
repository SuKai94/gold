##Java进阶之异常

1.异常

1）直接抛出去的throws关键字

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

class AddMachine{
	
	public int performAdd(){
		int firstNUm = 0, secondNum = 0;
		try{
			firstNUm = getDigFromConsole();
			secondNum = getDigFromConsole();
		}catch(IOException e){
			e.printStackTrace();
		}
		return firstNUm + secondNum;
	}
	
	private int getDigFromConsole() throws IOException{
		InputStreamReader stdin = new InputStreamReader(System.in);
		BufferedReader bufin = new BufferedReader(stdin);
		System.out.print("请输入数字：  ");
		String str = bufin.readLine();
		int ret = Integer.parseInt(str);
		return ret;
	}		
}

public class Main{
	public static void main(String[] args){
		AddMachine a = new AddMachine();
		System.out.println(a.performAdd());
	}
}
```

2）负责任的try...catch...语句

将上述的getDigFromConsole()改为：
```java
private int getDigFromConsole() throws IOException{
	InputStreamReader stdin = new InputStreamReader(System.in);
	BufferedReader bufin = new BufferedReader(stdin);
	System.out.print("请输入数字：  ");
	String str = null;
	try{
		str = bufin.readLine();
	}catch(IOException e){
	    e.printStackTrace();
	}	
	int ret = Integer.parseInt(str);
	return ret;
}
```
抓异常的策略：java中异常分为unchecked和checked两种，另一种叫法是错误和异常，这不同的类别代表着不同的处理方式。

checked异常：

- 表示无效，不是程序中可以预测的。比如无效的用户输入，文件不存在，网络或者数据库链接错误。这些都是外在的原因，都不是程序内部可以控制的。

- 必须在代码中显式地处理。比如try-catch块处理，或者给所在的方法加上throws说明，将异常抛到调用栈的上一层。

- 继承自java.lang.Exception（java.lang.RuntimeException除外）。

unchecked异常：

- 表示错误，程序的逻辑错误。是RuntimeException的子类，比如IllegalArgumentException, NullPointerException和IllegalStateException。

- 不需要在代码中显式地捕获unchecked异常做处理。

- 继承自java.lang.RuntimeException（而java.lang.RuntimeException继承自java.lang.Exception）。

1）抓了不管的unchecked异常：例如上面的语句`int ret = Integer.parseInt(str);`有可能抛出`NumberFormatException`异常。像这种异常的待遇和IOException的待遇是不一样的，因为`NumberFormatException`是一个unchecked异常,我们要以更严谨的态度补完这段代码：

```java
while(true){
	System.out.print("请输入数字：  ");
	try{
		str = bufin.readLine();
	}
	catch(IOException e){
		e.printStackTrace();
	}
			
	if(!Pattern.matches("\\d+", str)){
		System.out.println("输入的必须为数字：");
	}
	else{
		break;
	}
}		
ret = Integer.parseInt(str);
return ret;
```
还有一种利用异常处理达到同样效果的：
```java
while(true){
			System.out.print("请输入数字：  ");
			try{
				str = bufin.readLine();
			}
			catch(IOException e){
				e.printStackTrace();
			}
			try{
				ret = Integer.parseInt(str);
				break;
			}
			catch(NumberFormatException e){
				System.out.println("输入的必须是数字：");
			}
		}
		return ret;
```
但是，注意：这种利用异常处理虽然达到同样的效果，但是不建议这么做。因为每个异常的产生与抛出，java都会对资源消耗很大的操作，切忌用异常来进行流程控制

2.自定义异常：一般要求自定义的异常类必须为checked异常，所以应该继承自Exception
```java
class AppException extends Exception{
	
	public AppException(){
	}
	
	public AppException(String arg0){
		super(arg0);
	}
	
	public AppException(Throwable arg0){
		super(arg0);
	}
	
	public AppException(String arg0, Throwable arg1){
		super(arg0, arg1);
	}
}
```

3.清理异常现场之finally使用

```java
try{
	str = bufin.readLine();
}
catch(IOException e){
	e.printStackFrace();
}
finally{
	try{
		stdin.close();
		bufin.close();
	}
	catch(IOException e){
		e.printStackFrace();
	}
}
```
释放资源的操作都务必放在finally代码块中