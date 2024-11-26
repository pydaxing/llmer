import json
import re

from .runtime.exceptions import ParseJSONError

def parse_json(content):
    """
    解析 JSON 字符串，支持以下情况：
    1. 带有 ```json 标记的内容（前后可能有其他文本）。
    2. 普通 JSON 字符串。
    3. 自动忽略非 JSON 部分，仅提取有效的 JSON 部分。
    """
    try:
        # 使用正则提取 JSON 部分
        match = re.search(r'```json\s*(.*?)```', content, re.DOTALL)
        if match:
            json_str = match.group(1).strip()  # 提取 ```json 和 ``` 之间的内容
        else:
            # 如果没有 ```json 标记，尝试直接解析整个输入
            json_str = content.strip()

        # 尝试解析 JSON
        return json.loads(json_str)
    except Exception as e:
        raise ParseJSONError(str(e))

