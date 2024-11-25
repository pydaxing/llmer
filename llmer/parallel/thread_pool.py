import concurrent.futures
from typing import List, Dict, Any, Callable
from tqdm import tqdm  # 导入 tqdm 库
from .base import ParallelBase

class ThreadPool(ParallelBase):
    def __init__(self, parallel_count: int = 1):
        """
        初始化 ThreadPool 类，设定最大并发线程数。
        :param parallel_count: 最大并发线程数，默认为1
        """
        super().__init__(parallel_count)

    def __call__(self, func: Callable[..., Any]) -> Callable[..., List[Any]]:
        """
        使得 ThreadPool 实例可以作为装饰器使用。
        :param func: 被装饰的函数
        :return: 一个新的函数，具有并发执行功能
        """
        def wrapper(parallel_params: List[Dict[Any, Any]], *args, **kwargs) -> List[Any]:
            result = [None] * len(parallel_params)

            # 使用 ThreadPoolExecutor 来并行执行任务
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.parallel_count) as executor:
                # 提交任务并记录对应的索引
                futures = {
                    executor.submit(func, **param): index
                    for index, param in enumerate(parallel_params)
                }

                # 使用 tqdm 显示进度条
                for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc=f"Thread Pool Processing -> [{func.__name__}]"):
                    index = futures[future]
                    result[index] = future.result()

            return result

        return wrapper
