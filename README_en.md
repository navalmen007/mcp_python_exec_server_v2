# English Documentation

### Description
This is a secure Python code execution tool that provides a safe execution environment via an MCP server. Users can execute Python code snippets and get the results. The tool disables dangerous built-in functions and modules to prevent malicious code execution.

### Supported Standard Libraries
- **math**: Mathematical functions
- **statistics**: Statistical calculations
- **decimal**: Decimal floating point arithmetic
- **fractions**: Rational numbers
- **functools**: Higher-order functions
- **random**: Generate random numbers
- **string**: String operations
- **time**: Time-related functions
- **datetime**: Date and time handling
- **json**: JSON encoder and decoder
- **re**: Regular expressions

### Disabled Features
The following built-in functions are disabled:
- `eval`, `exec`, `open`, `input`, `globals`, `locals`
- `breakpoint`, `compile`, `delattr`, `setattr`
- `exit`, `quit`, `help`, `memoryview`, `vars`, `dir`

### Usage Example
The MCP function name of this tool is `python_exec`, and the parameter is a string of Python code.

```python
# Calculate 1+1
print(1+1)
```

Return result:
```
Output:
2
```

If variables are defined:
```python
a = 10
b = 20
c = a + b
c
```

Return result:
```
Output:
30

Defined variables/functions:
a = 10
b = 20
c = 30
```

### Notes
1. The code must be a string
2. The code cannot be empty
3. The tool cannot perform dangerous operations such as file operations or network requests
4. If code execution fails, an error message will be returned

