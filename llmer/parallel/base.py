from abc import ABC, abstractmethod
from typing import List, Dict, Any, Callable

class ParallelBase(ABC):

    def __init__(self, parallel_count: int = 1):
        self.parallel_count = parallel_count

    def __call__(self, func: Callable[..., Any]) -> Callable[..., List[Any]]:
        raise NotImplementedError("__call__ not implemented!")
