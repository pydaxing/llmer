from abc import ABC, abstractmethod
from typing import List, Dict, Any, Callable

class ModelBase(ABC):

    def __init__(
            self,
            api_key: str = None,
            endpoint: str = None,
            api_version: str = None,
            headers: Dict[str, Any] = None,
            timeout: float = 600,
            retry: int = 2
    ):
        self.api_key = api_key
        self.endpoint = endpoint
        self.api_version = api_version
        self.headers = headers
        self.timeout = timeout
        self.retry = retry

    def chat(
            self,
            model: str = None,
            temperature: float = 1.0,
            top_p: float = 0.1,
            max_tokens: int = 1024,
            messages: List[Dict[str, Any]] = None,
            response_format = None,
            tools: List = None,
            tool_choice: str = None,
            stream: bool = False
    ):
        if stream:
            return self._stream_response(
                model,
                temperature,
                top_p,
                max_tokens,
                messages,
                response_format,
                tools,
                tool_choice
            )
        else:
            return self._non_stream_response(
                model,
                temperature,
                top_p,
                max_tokens,
                messages,
                response_format,
                tools,
                tool_choice
            )

    def _non_stream_response(self, *args, **kwargs):
        raise NotImplementedError("_non_stream_response not implemented!")

    def _stream_response(self, *args, **kwargs):
        raise NotImplementedError("_stream_response not implemented!")
