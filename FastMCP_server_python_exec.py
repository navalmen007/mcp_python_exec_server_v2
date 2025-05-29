import builtins
import math
import statistics
import decimal
import fractions
import functools
import random
import string
import time
import datetime
import json
import re
import io
import sys
import traceback
from contextlib import redirect_stdout, redirect_stderr

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as e:
    print(f"Error importing FastMCP: {e}", file=sys.stderr)
    print("Please install mcp: pip install mcp", file=sys.stderr)
    sys.exit(1)

# Create an MCP server
mcp = FastMCP("python_exec")

# 危险的内置函数黑名单
DANGEROUS_BUILTIN_NAMES = [
    'eval',
    'exec',
    'open',
    'input',
    'globals',
    'locals',
    'breakpoint',
    'compile',
    'delattr',
    'setattr',
    'exit',
    'quit',
    'help',
    'memoryview',
    'vars',
    'dir',
]

# 创建安全的内置函数白名单
SAFE_BUILTINS = {}
for name, obj in builtins.__dict__.items():
    if name not in DANGEROUS_BUILTIN_NAMES:
        SAFE_BUILTINS[name] = obj

@mcp.tool()
def python_exec(pycode: str) -> str:
    """
    执行Python代码的安全沙箱
    
    可用标准库：
    - math, statistics, decimal, fractions  # 数学计算
    - random, string                       # 随机/字符串
    - time, datetime                       # 时间日期
    - json, re                             # 数据解析
    - functools                            # 函数工具
    
    禁用内置功能：
    - 文件/网络操作（open等）
    - 动态代码执行（eval/exec/compile）
    - 环境访问（globals/locals）
    - 系统调试（breakpoint）
    - 动态导入（__import__）
    
    Args:
        pycode: 要执行的Python代码字符串
    
    Returns:
        执行结果的字符串表示，包含输出和返回值
    """
    if not isinstance(pycode, str):
        return "错误: 代码必须是字符串类型"
    
    if not pycode.strip():
        return "错误: 代码不能为空"
    
    # 设置执行环境的全局变量
    execution_globals = {
        '__builtins__': SAFE_BUILTINS,  # 使用安全的内置函数白名单
        'math': math,                   # 数学功能计算
        'statistics': statistics,       # 统计功能计算
        'decimal': decimal,            # 精确的浮点数运算
        'fractions': fractions,        # 分数运算
        'functools': functools,        # 函数工具
        'random': random,              # 随机数生成
        'string': string,              # 字符串相关
        'time': time,                  # 时间相关
        'datetime': datetime,          # 日期时间相关
        'json': json,                  # json相关
        're': re,                      # 正则表达式
    }
    
    # 创建空的局部变量字典
    execution_locals = {}
    
    try:
        # 捕获标准输出和标准错误
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
            # 使用exec执行代码，同时传入globals和locals
            # 将locals设置为globals以支持函数定义和递归调用
            exec(pycode, execution_globals, execution_globals)
        
        # 获取输出内容
        stdout_content = stdout_capture.getvalue()
        stderr_content = stderr_capture.getvalue()
        
        # 构建返回结果
        result_parts = []
        
        if stdout_content:
            result_parts.append(f"输出:\n{stdout_content.rstrip()}")
        
        if stderr_content:
            result_parts.append(f"错误输出:\n{stderr_content.rstrip()}")
        
        # 检查是否有新定义的变量或函数
        user_defined = {}
        for key, value in execution_globals.items():
            # 只显示用户定义的变量（不是预设的模块）
            if key not in ['__builtins__', 'math', 'statistics', 'decimal', 
                          'fractions', 'functools', 'random', 'string', 
                          'time', 'datetime', 'json', 're'] and not key.startswith('_'):
                user_defined[key] = value
        
        if user_defined:
            vars_info = []
            for key, value in user_defined.items():
                if not key.startswith('_'):  # 忽略私有变量
                    try:
                        # 对于函数，只显示函数名和类型
                        if callable(value):
                            vars_info.append(f"{key} = <function>")
                        else:
                            value_str = repr(value)
                            # 限制单个变量的显示长度
                            if len(value_str) > 200:
                                value_str = value_str[:200] + "..."
                            vars_info.append(f"{key} = {value_str}")
                    except Exception:
                        vars_info.append(f"{key} = <无法显示>")
            
            if vars_info:
                result_parts.append(f"定义的变量/函数:\n" + "\n".join(vars_info))
        
        # 如果没有任何输出，返回执行成功的消息
        if not result_parts:
            result_parts.append("代码执行成功，无输出")
        
        return "\n\n".join(result_parts)
        
    except SyntaxError as e:
        return f"语法错误: 第{e.lineno}行: {e.msg}"
    except Exception as e:
        # 获取详细的错误信息
        error_type = type(e).__name__
        error_msg = str(e)
        
        # 获取简化的堆栈跟踪
        tb_lines = traceback.format_exc().splitlines()
        # 只显示用户代码相关的错误行
        relevant_lines = []
        for line in tb_lines:
            if 'exec(pycode' in line or 'line ' in line:
                relevant_lines.append(line.strip())
        
        if relevant_lines:
            return f"执行错误: {error_type}: {error_msg}\n详情: {' '.join(relevant_lines[-2:])}"
        else:
            return f"执行错误: {error_type}: {error_msg}"



def main():
    """主函数，启动MCP服务器"""
    try:
        mcp.run()
    except KeyboardInterrupt:
        print("\n服务器已停止", file=sys.stderr)
    except Exception as e:
        print(f"服务器启动失败: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
