import asyncio
from typing import Callable, Any, List, Dict
from tqdm.asyncio import tqdm  # 导入 tqdm.asyncio 来支持异步更新
from .base import ParallelBase

class AsyncExecutor(ParallelBase):
    def __init__(self, parallel_count: int = 1):
        """
        初始化 AsyncExecutor 类，设定最大并发数量
        :param parallel_count: 最大并发任务数，默认为1
        """
        super().__init__(parallel_count)
        self.semaphore = asyncio.Semaphore(parallel_count)  # 限制最大并发数

    def __call__(self, func: Callable[..., Any]) -> Callable[..., List[Any]]:
        """
        使得 AsyncExecutor 实例可以作为装饰器使用。
        :param func: 被装饰的函数
        :return: 一个新的异步函数，支持并发执行
        """
        async def wrapper(parallel_params: List[Dict[Any, Any]], *args, **kwargs) -> List[Any]:
            result = [None] * len(parallel_params)

            # 使用 tqdm 创建进度条
            with tqdm(total=len(parallel_params), desc=f"Async Executor Processing -> [{func.__name__}]") as pbar:
                async def worker(index, param):
                    async with self.semaphore:  # 限制并发
                        loop = asyncio.get_running_loop()  # 获取当前事件循环
                        # 使用 run_in_executor 将非异步函数放入线程池
                        result[index] = await loop.run_in_executor(
                            None,  # 使用默认的 ThreadPoolExecutor
                            func,   # 要调用的非异步函数
                            *param.values()  # 解包参数字典
                        )
                        pbar.update(1)  # 每完成一个任务，更新进度条

                # 使用 asyncio.gather 并发执行所有任务
                await asyncio.gather(*[
                    worker(i, param) for i, param in enumerate(parallel_params)
                ])

            return result

        return wrapper
