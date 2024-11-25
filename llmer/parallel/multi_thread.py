import threading
from typing import List, Dict, Any, Callable
from tqdm import tqdm  # 导入 tqdm
from .base import ParallelBase

class MultiThread(ParallelBase):
    def __init__(self, parallel_count: int = 1):
        """
        初始化 MultiThread 类，设定最大并发线程数。
        :param parallel_count: 最大并发线程数，默认为1
        """
        super().__init__(parallel_count)

    def __call__(self, func: Callable[..., Any]) -> Callable[..., List[Any]]:
        """
        使得 MultiThread 实例可以作为装饰器使用。
        :param func: 被装饰的函数
        :return: 一个新的函数，具有并发执行功能
        """
        def wrapper(parallel_params: List[Dict[Any, Any]], *args, **kwargs) -> List[Any]:
            result = [None] * len(parallel_params)
            threads = []

            # 定义每个线程执行的工作
            def worker(index, param):
                result[index] = func(**param)

            # 使用 tqdm 创建进度条，func.__name__ 获取函数名称
            with tqdm(total=len(parallel_params), desc=f"Multi Thread Processing -> [{func.__name__}]") as pbar:
                # 创建并启动线程，限制并行线程数
                for i, param in enumerate(parallel_params):
                    if len(threads) >= self.parallel_count:
                        threads[0].join()  # 等待第一个线程完成后再启动新线程
                        threads.pop(0)

                    thread = threading.Thread(target=worker, args=(i, param))
                    threads.append(thread)
                    thread.start()

                    # 每启动一个线程，就更新进度条
                    pbar.update(1)

                # 等待所有线程完成
                for thread in threads:
                    thread.join()

            return result

        return wrapper
