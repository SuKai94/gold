Python yield使用浅析
===

经常容易遗忘python的这些黑魔法，得慢慢记录积累才不会忘的快

### 从简单的Fibonacci数列入手

使用Python生成Fibonacci数列，版本一的代码：

```python
def fab(max):
	n, a, b = 0, 0 ,1
	L = []
	while n < max:
		L.append(b)
		a, b = b, a+b
		n = n+1
	return L
```

版本一简单暴力，但是缺点就是返回值List将随着max增加而增加，受到内存限制。下面采用yield对其进行修改

### 使用yield生成Fibonacci数列

```python
def fab(max):
	n, a, b = 0, 0 ,1
	yeild b
	while n < max:
		yield b
		a, b = b, a+b
		n = n+1
```

测试代码：

```python
for i in fab(10):
	print i
```

这样做，可以实现与版本一同样的效果

**解析**：简单的讲，yield就是将一个普通函数变成了一个generator，调用fab(10)不再执行fab函数，而是返回一个iterable对象！在for循环执行时，每次循环都会执行fab内部代码，执行到yield b时，fab就返回一个迭代值，下次迭代时，代码从yield b的下一条语句继续执行，而函数的本地变量看起来和中断执行前是一样的，于是，yield继续执行，直到遇到下一个yield

**注意：**如果函数中出现return，那么直接终止迭代
