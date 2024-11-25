# LLMER: 一个化繁为简的大模型（LLM）应用开发者神器

`llmer` 是一个轻量级的 Python 库，旨在简化大型语言模型（LLMs）应用中的复杂过程。它提供了用于并行处理、运行时管理、文件处理和Prompt格式化等常用的高级 API 和实用工具，从而不用每次都需要重复开发相关代码，简化工作。

## 功能特点
- **模型调用**: 支持OpenAI风格和Azure模型调用。
- **并行处理**: 支持线程池并发、多线程并发、异步函数异步并发、非异步函数异步并发。
- **运行时管理**: 提供timeout装饰器用于超时控制，并发安全锁装饰器保证并发过程中对数据修改的正确性。
- **文件工具**:  提供对 YAML读取、文件转List（尤其适用jsonl）、List存文件、 图像转 Base64 编码的工具。
- **提示管理**: 将 message 转成 ChatML 格式。
- **更多功能**: 敬请期待...

## 安装
要安装 `llmer`，使用以下命令：
```bash
pip install llmer
```

## 快速开始

```python
from llmer.parallel.thread_pool import ThreadPool


@ThreadPool(parallel_count=4)
def square(num):
  return num ** 2


tasks = [{"num": i} for i in range(10)]
results = square(tasks)
print(results)  # Output: [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```
## 功能模块概览
LLMER主要包括以下功能，更多通用功能正在开发中，敬请期待：

### 1. 模型调用
- **`Azure`**: 用于调用托管于 Microsoft Azure 的语言模型。
- **`OpenAI`**: 用于调用 GPT 系列模型以及按 OpenAI 风格部署的模型。

### 2. 并行处理
- **`ThreadPool`**: 使用线程池进行并发。
- **`MultiThread`**: 使用多线程进行并发。
- **`AsyncParallel`**: 针对异步函数的异步并行。
- **`AsyncExecutor`**: 针对非异步函数的异步并行。

### 3. 运行管理
- **`timeout`**: 函数timeout装饰器（包括生成器也可以直接使用）。
- **`parallel_safe_lock`**: 支持自定义超时设置的并行安全锁。

### 4. 文件工具
- 提供对 YAML读取、文件转List（尤其适用jsonl）、List存文件、 图像转 Base64 编码的工具。

### 5. 提示词管理
- 将openai格式的message转成ChatML格式。

## API 文档

## 1. 模型调用

`llmer` 的 `model` 模块提供了两个类**`Azure`**和**`OpenAI`**，分别支持Azure模型和OpenAI风格模型（GPT和按openai风格部署的模型）调用

### 1.1 Azure

Azure 可支持chat和函数调用。


**使用举例**:

```python
from llmer.model import Azure

openai_api_key = "xxxx"
openai_model_name = "gpt-4o"
openai_api_version = 'xxxx'
openai_api_base = "xxxx"

headers = {}

gpt4o = Azure(
  headers=headers,
  api_key=openai_api_key,
  api_version=openai_api_version,
  endpoint=openai_api_base,
  timeout=10,
  retry=2
)

gpt_response = gpt4o.chat(
  model=openai_model_name,
  temperature=0.1,
  stream=True,
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Can you tell me the weather today?"},
  ],
  response_format=None,
)

for chunk in gpt_response:
  print(chunk)
```


### 1.2 OpenAI

同样支持Chat和函数调用（function call）


**使用举例**:

```python
from llmer.model import Azure, OpenAI

claude_api_key = "xxxx"
claud_model_name = "anthropic.claude-3-5-sonnet-20240620-v1:0"
claude_api_base = "xxxx"

headers = {}

claude = OpenAI(
  headers=headers,
  api_key=claude_api_key,
  endpoint=claude_api_base,
  timeout=10,
  retry=2
)

response = claude.chat(
  model=claud_model_name,
  temperature=0.1,
  stream=True,
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Can you tell me the weather today?"},
  ],
  response_format=None,
)
for chunk in response:
  print(chunk)
```



## 2. 并行执行

### 2.1 ThreadPool
使用线程池方式实现并行。

**使用举例**:

```python
from llmer.parallel.thread_pool import ThreadPool


@ThreadPool(parallel_count=3)
def add_one(num):
  return num + 1


tasks = [{"num": i} for i in range(5)]
results = add_one(tasks)
print(results)  # Output: [1, 2, 3, 4, 5]
```

### 2.2 MultiThread
使用多线程方式实现并行。

**使用举例**:

```python
from llmer.parallel.multi_thread import MultiThread


@MultiThread(parallel_count=2)
def multiply(num):
  return num * 2


tasks = [{"num": i} for i in range(4)]
results = multiply(tasks)
print(results)  # Output: [0, 2, 4, 6]
```

### 2.3 AsyncParallel
对异步函数实现异步并发。

**使用举例**:

```python
import asyncio
from llmer.parallel.async_parallel import AsyncParallel


@AsyncParallel(parallel_count=2)
async def async_task(num):
  await asyncio.sleep(1)
  return num * 10


tasks = [{"num": i} for i in range(4)]
results = asyncio.run(async_task(tasks))
print(results)  # Output: [0, 10, 20, 30]
```


### 2.4 AsyncExecutor
对非异步函数实现异步并发

**使用举例**:

```python
import asyncio
import time
from llmer.parallel.async_executor import AsyncExecutor


@AsyncExecutor(parallel_count=2)
def async_task(num):
  time.sleep(1)
  return num * 5


tasks = [{"num": i} for i in range(4)]
results = asyncio.run(async_task(tasks))
print(results)  # Output: [0, 5, 10, 15]
```


## 3. 运行管理

### 3.1 timeout装饰器

`timeout` 装饰器允许为函数设置执行的时间限制。如果函数超出了指定的时间，将引发 `ExecutionTimeoutError` 异常。

对于生成器函数（使用了`yield`的函数）同样无缝支持。

**使用举例**:

```python
import time
from llmer.runtime.context import timeout
from llmer.runtime.exceptions import ExecutionTimeoutError


@timeout(3)  # Set timeout to 3 seconds
def long_running_function(x):
  time.sleep(x)  # Simulate a long task


try:
  long_running_function(5)
except ExecutionTimeoutError as e:
  print(e)  # Output: Function 'long_running_function' timed out after 3 seconds

# 还支持超时时间覆写，比如下面的timeout=2将覆盖@timeout(3)
try:
  long_running_function(5, timeout=2)
except ExecutionTimeoutError as e:
  print(e)  # Output: Function 'long_running_function' timed out after 2 seconds
```


### 3.2 并行安全锁装饰器

`parallel_safe_lock` 装饰器确保函数只能在成功获取锁时执行。如果函数在指定的超时时间内无法获取锁，将引发 `AcquireLockTimeoutError` 异常。这在函数处理共享资源并需要防止并发执行时非常有用。


**使用举例**:

```python
from llmer.runtime import parallel_safe_lock, AcquireLockTimeoutError
import threading
from time import sleep

lock = threading.Lock()


@parallel_safe_lock(lock, seconds=0.5)
def write_data(data: str):
  print(f"Writing data: {data}")
  sleep(0.6)


def task():
  try:
    write_data("some data")
  except AcquireLockTimeoutError as e:
    print(e)  # Output: critical_section acquires lock, timeout exceeded 0.5


threads = []
for _ in range(3):
  t = threading.Thread(target=task)
  t.start()
  threads.append(t)

for t in threads:
  t.join()


# 同样，这里的超时时间也可以覆写，在调用write_data的时候write_data("some data", timeout=0.8)也能够修改原超时时间。
```

## 4. 文件工具

提供了文件处理的实用工具，例如YAML读取、文件转List（尤其适用jsonl）、List存文件、 图像转 Base64 编码。

### 4.1 文件转列表

`file_to_list()` 函数读取 JSONL 文件（其它任何文件均可，每一行转换成list中的一个元素），并将其内容作为字典列表返回。

#### 参数:
- `path` (Optional[str]): JSONL 文件的路径


**使用举例**:

```python
from llmer.file import file_to_list

# Example usage: Reading a JSONL file from the current script directory
data = file_to_list("data.jsonl")
print(data)
# Output: List of dictionaries read from the JSONL file
```


### 4.2 列表转文件

`list_to_file()` 函数将数据列表（例如字典、字符串等）保存到文件中。您可以指定打开文件的模式（`'w'` 为写入，`'a'` 为追加）。

#### 参数:
- `data` (List[Any]): 要保存到文件中的数据。它应该是一个列表，列表中的每个项目将被写入文件的一个新行。
- `path` (Optional[str]): 保存文件的路径
- `mode` (str, 默认 'w'): 打开文件的模式。`'w'` 将覆盖文件，`'a'` 将数据追加到文件末尾。

**使用举例**:

```python
from llmer.file import list_to_file

# Example data to save
data = [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]

# Example usage: Saving a list of dictionaries to a JSONL file
list_to_file(data, "output.jsonl")
```



### 4.3 YAML 读取

`yaml_reader()` 函数读取一个 YAML 配置文件，并将其内容作为 Python 字典返回。该函数假定 YAML 文件结构正确，并返回解析后的数据。

#### 参数:
- `path` (Optional[str]): YAML 文件的路径

**使用举例**:

```python
from llmer.file import yaml_reader

# Example YAML file path
yaml_file = "config.yaml"

# Example usage: Reading a YAML configuration file
config = yaml_reader(yaml_file)

print(config)
```


### 4.4 图像转 Base64

`image_to_base64()` 函数将图像文件转换为 Base64 编码的字符串。它还可以为 Base64 字符串添加`data:xxx`，以便直接在网页内容或其他用途中嵌入图像。

#### 参数:
- `path` (Optional[str]): 图像文件的路径
- `prefix` (bool, 可选): 如果为 `True`，则在 Base64 字符串前添加数据前缀。默认值为 `False`。

**使用举例**:

```python
from llmer.file import image_to_base64

# Example image file path
image_file = "example.png"

# Convert image to Base64 without prefix
encoded_image = image_to_base64(image_file)

print(encoded_image)

# Convert image to Base64 with prefix
encoded_image_with_prefix = image_to_base64(image_file, prefix=True)

print(encoded_image_with_prefix)
```


## 5. 提示工具

### 5.1 ChatML 格式化

`chatml()` 函数将一系列消息格式化为 ChatML 格式，这种格式通常用于以结构化方式处理语言模型中的对话。此函数生成一个字符串，其中每条消息都被适当地包装为系统、用户和助手角色的标签。

#### 参数:
- `messages` (List[Dict[str, str]]): 消息列表，其中每条消息是一个包含以下键的字典：
  - `role` (str): 说话者的角色，例如 `"system"`、`"user"` 或 `"assistant"`。
  - `content` (str): 消息的内容。


**使用举例**:

```python
from llmer.prompt import chatml

# Example messages
messages = [
  {"role": "system", "content": "You are a helpful assistant."},
  {"role": "user", "content": "Can you tell me the weather today?"},
  {"role": "assistant", "content": "The weather is sunny with a chance of rain."}
]

# Format messages into ChatML
formatted_message = chatml(messages)

print(formatted_message)
```

```text
<|im_start|>system
You are a helpful assistant.<|im_end|>
<|im_start|>user
Can you tell me the weather today?<|im_end|>
<|im_start|>assistant
The weather is sunny with a chance of rain.<|im_end|>
<|im_start|>assistant
```



## 贡献

欢迎为本项目做出贡献。您可以提交问题或提交拉取请求。

## 联系

您可以通过 pydaxing@gmail.com 联系我们。
