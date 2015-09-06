Python中的json，dict，str的操作
===

### json到字典的转化

使用标准库simplejson

```python
dictinfo = simplejson.loads(json_str)
```

### 字典到json的转化：

```python
jsoninfo = simplejson.dumps(dict)
```

### 将字符串转换成字典dict类型

```python
dict = eval(str)
```
