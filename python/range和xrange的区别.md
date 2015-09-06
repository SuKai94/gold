range()和xrange()的区别
===

```
# 版本一
for i in range(1000):
	pass

# 版本二
for i in xrange(1000): 
	pass
```

版本一会生成一个1000个元素的List；版本二则不会，而是在每次迭代的时候，返回下一个数值，内存空间占用很小，原理和yield一样
