import asyncio
from typing import Callable, List, Dict, Any
from tqdm.asyncio import tqdm  # 导入 tqdm.asyncio 来支持异步更新
from .base import ParallelBase

class AsyncParallel(ParallelBase):
    def __init__(self, parallel_count: int = 1):
        """
        初始化 AsyncParallel 类，设定最大并发任务数
        :param parallel_count: 最大并发任务数，默认为1
        """
        super().__init__(parallel_count)
        self.semaphore = asyncio.Semaphore(parallel_count)  # 控制并发数量

    def __call__(self, func: Callable[..., Any]) -> Callable[..., List[Any]]:
        """
        使 AsyncParallel 实例能够作为装饰器使用。
        :param func: 被装饰的函数
        :return: 一个新的异步函数，支持并发执行
        """
        async def wrapper(parallel_params: List[Dict[Any, Any]], *args, **kwargs) -> List[Any]:
            result = [None] * len(parallel_params)

            # 创建 tqdm 进度条
            with tqdm(total=len(parallel_params), desc=f"Async Parallel Processing -> [{func.__name__}]") as pbar:
                async def worker(index, param):
                    async with self.semaphore:  # 限制并发任务数
                        result[index] = await func(**param)  # 调用被装饰的函数
                        pbar.update(1)  # 每当一个任务完成时，更新进度条

                # 使用 asyncio.gather 并发执行所有任务
                await asyncio.gather(*[
                    worker(i, param) for i, param in enumerate(parallel_params)
                ])

            return result

        return wrapper
