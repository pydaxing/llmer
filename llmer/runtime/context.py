import time
import inspect
import threading
from typing import Callable, Any

from llmer.runtime.exceptions import AcquireLockTimeoutError, ExecutionTimeoutError



def timeout(seconds: float):
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args, timeout=None, **kwargs) -> Any:
            """包装函数，支持动态超时时间"""
            effective_timeout = timeout if timeout is not None else seconds
            is_generator = inspect.isgeneratorfunction(func)

            if is_generator:
                def generator_wrapper():
                    start_time = time.time()  # 记录第一次 yield 开始时间
                    thread_exception = None

                    # 启动线程来执行生成器
                    def worker():
                        nonlocal thread_exception
                        try:
                            for item in func(*args, **kwargs):
                                yield item
                        except Exception as e:
                            thread_exception = e
                            raise e

                    # 生成器实例
                    gen = worker()
                    while True:
                        try:
                            # 每次调用生成器时都要检查超时
                            elapsed_time = time.time() - start_time
                            if elapsed_time > effective_timeout:
                                raise ExecutionTimeoutError(
                                    f"Function '{func.__name__}' timed out after {effective_timeout} seconds"
                                )

                            # `next(gen)` 会迭代到下一个生成器项
                            yield next(gen)
                        except StopIteration:
                            break  # 如果生成器完成，退出循环
                        except Exception as e:
                            thread_exception = e
                            break

                    if thread_exception:
                        raise thread_exception

                return generator_wrapper()
            else:
                result = []
                thread_exception = None

                def worker():
                    nonlocal thread_exception
                    try:
                        result.append(func(*args, **kwargs))
                    except Exception as e:
                        thread_exception = e

                thread = threading.Thread(target=worker, daemon=True)
                thread.start()
                thread.join(timeout=effective_timeout)

                if thread.is_alive():
                    raise ExecutionTimeoutError(
                        f"Function '{func.__name__}' timed out after {effective_timeout} seconds"
                    )

                if thread_exception:
                    raise thread_exception

                return result[0] if result else None

        return wrapper
    return decorator




def parallel_safe_lock(lock: threading.Lock, seconds: float = 1) -> Callable[..., Any]:

    def decorator(rw_func: Callable[..., Any]) -> Callable[..., Any]:

        def wrapper(*args, timeout=None, **kwargs) -> Any:
            """
            包装函数：允许在每次调用时覆盖超时值
            :param timeout: 覆盖超时时间
            :param args: 被装饰函数的参数
            :param kwargs: 被装饰函数的关键字参数
            :return: 函数的返回结果
            """
            # 如果调用时有传递覆盖的超时值，则使用覆盖值
            lock_timeout = timeout if timeout is not None else seconds
            acquired = False
            try:
                if not lock.acquire(timeout=lock_timeout):
                    raise AcquireLockTimeoutError(f"{rw_func.__name__} acquires lock, timeout exceeded {lock_timeout}")
                acquired = True
                return rw_func(*args, **kwargs)
            finally:
                if acquired:
                    lock.release()

        return wrapper

    return decorator



