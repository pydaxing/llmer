from fastapi import FastAPI
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel, Field
import uvicorn
from inspect import signature, isgeneratorfunction, isasyncgenfunction
from typing import Callable, Any, Dict
import asyncio

def generate_input_model(func: Callable) -> BaseModel:
    """
    根据函数签名动态创建 Pydantic 模型，用于请求体验证。
    """
    fields: Dict[str, Any] = {}
    sig = signature(func)

    for name, param in sig.parameters.items():
        annotation = param.annotation
        if param.default is param.empty:
            fields[name] = (annotation, Field(...))  # 必填字段
        else:
            fields[name] = (annotation, Field(default=param.default))  # 可选字段

    return type(
        f"{func.__name__.capitalize()}Input",
        (BaseModel,),
        { "__annotations__": {k: v[0] for k, v in fields.items()}, **{k: v[1] for k, v in fields.items()} },
    )

def deploy(host: str = "127.0.0.1", port: int = 9510):
    """
    装饰器将函数部署为 FastAPI 服务。通过 `isasyncgenfunction` 判断是否为异步流式返回。
    """
    def decorator(func: Callable):
        # 创建 FastAPI 应用
        app = FastAPI()

        # 动态生成输入模型
        InputModel = generate_input_model(func)

        # 定义路由
        @app.post(f"/{func.__name__}")
        async def api_handler(data: InputModel):
            try:
                # 调用原函数并获取结果
                result = func(**data.dict())

                # 如果是异步生成器函数，返回 StreamingResponse
                if isasyncgenfunction(func):  # 判断是否为异步生成器函数
                    async def sse_generator():
                        async for item in result:
                            yield f"data: {item}\n\n"
                    return StreamingResponse(sse_generator(), media_type="text/event-stream")

                # 如果是同步生成器函数，返回 StreamingResponse
                elif isgeneratorfunction(func):  # 判断是否为同步生成器函数
                    def sse_generator():
                        for item in result:
                            yield f"data: {item}\n\n"
                    return StreamingResponse(sse_generator(), media_type="text/event-stream")

                # 否则返回普通 JSON 响应
                if asyncio.iscoroutine(result):
                    result = await result
                return JSONResponse(content={"success": True, "data": result})
            except Exception as e:
                return JSONResponse(content={"success": False, "error": str(e)}, status_code=400)

        # 启动服务的方法
        def serve():
            uvicorn.run(app, host=host, port=port)

        func.serve = serve
        return func
    return decorator
