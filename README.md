
### 功能描述
这是一个安全的Python代码执行工具，通过MCP服务器提供安全的执行环境。用户可以通过该工具执行Python代码片段，并获取执行结果。该工具禁用了危险的内置函数和模块，以防止恶意代码执行。

### 支持的标准库
- **math**: 数学计算
- **statistics**: 统计计算
- **decimal**: 高精度小数
- **fractions**: 分数运算
- **functools**: 函数工具
- **random**: 随机数生成
- **string**: 字符串处理
- **time**: 时间相关
- **datetime**: 日期时间
- **json**: JSON处理
- **re**: 正则表达式

### 禁用功能
以下内置函数被禁用：
- `eval`, `exec`, `open`, `input`, `globals`, `locals`
- `breakpoint`, `compile`, `delattr`, `setattr`
- `exit`, `quit`, `help`, `memoryview`, `vars`, `dir`

### 使用示例
调用该工具的MCP函数名为`python_exec`，参数为字符串类型的Python代码。

```python
# 计算1+1
print(1+1)
```

返回结果：
```
输出:
2
```

如果定义了变量：
```python
a = 10
b = 20
c = a + b
c
```

返回结果：
```
输出:
30

定义的变量/函数:
a = 10
b = 20
c = 30
```

### 注意事项
1. 代码必须是字符串类型
2. 代码不能为空
3. 该工具不能执行文件操作、网络请求等危险操作
4. 如果代码执行出错，将返回错误信息

