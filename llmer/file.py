import os
import sys
import base64
import yaml
import json
import jsonlines
from typing import List, Any, Dict, Optional

def get_main_script_dir():
    """获取最终执行脚本的目录"""
    # sys.argv[0] 包含了运行时执行的脚本路径
    main_script = sys.argv[0]
    main_script_dir = os.path.dirname(os.path.abspath(main_script))
    return main_script_dir



def file_to_list(path: Optional[str] = None):
    res = []
    # 获取最终执行脚本的目录
    main_script_dir = get_main_script_dir()

    # 如果传入的路径不是绝对路径，则与最终执行脚本的目录拼接
    if path and not os.path.isabs(path):
        path = os.path.join(main_script_dir, path)

    with jsonlines.open(path, "r") as r:
        for line in r:
            res.append(line)
    return res



def list_to_file(data: List[Any] = None, path: Optional[str] = None, mode='w'):
    """将列表保存为 JSONL 文件"""
    # 获取最终执行脚本的目录
    main_script_dir = get_main_script_dir()

    # 如果传入的路径不是绝对路径，则与最终执行脚本的目录拼接
    if path and not os.path.isabs(path):
        path = os.path.join(main_script_dir, path)
    if data:
        with jsonlines.open(path, mode=mode) as writer:
            writer.write_all(data)


def yaml_reader(path: Optional[str] = None) -> Dict[str, Any]:
    """读取 YAML 配置文件并返回内容"""
    # 获取最终执行脚本的目录
    main_script_dir = get_main_script_dir()

    # 如果传入的路径是相对路径，则与脚本目录拼接成绝对路径
    if not os.path.isabs(path):
        path = os.path.join(main_script_dir, 'prompts', path)

    # 使用安全加载方法读取 YAML 文件
    with open(path, 'r') as file:
        component = yaml.safe_load(file)

    return component



def image_to_base64(path: Optional[str] = None, prefix=False) -> str:
    """
    将图片文件转换为 Base64 编码的字符串，并添加适当的前缀。

    :param path: 图片的路径（相对或绝对路径）。
    :return: 带有前缀的 Base64 编码字符串。
    """
    # 获取最终执行脚本的目录
    main_script_dir = get_main_script_dir()

    # 如果传入的路径不是绝对路径，则与最终执行脚本的目录拼接
    if path and not os.path.isabs(path):
        path = os.path.join(main_script_dir, path)

    # 获取图片的扩展名
    _, ext = os.path.splitext(path)
    ext = ext.lower().strip('.')  # 获取文件扩展名并转小写

    # 支持的图像格式（根据扩展名来判断）
    valid_image_formats = ["png", "jpeg", "jpg", "gif", "bmp", "tiff", "webp", "ico"]

    if ext not in valid_image_formats:
        raise ValueError(f"Unsupported image format: {ext}. Supported formats are: {', '.join(valid_image_formats)}")

    # 打开图片文件并读取内容
    with open(path, "rb") as img_file:
        # 读取图片并转换为 Base64 编码
        encoded_image = base64.b64encode(img_file.read()).decode("utf-8")

    if prefix:
        # 返回带前缀的 Base64 编码字符串
        data_prefix = f"data:image/{ext};base64,"
        encoded_image = data_prefix + encoded_image


    return encoded_image