class LLMExectionError(Exception):
    error_code = 95101
    error_msg = 'LLM Execution Failed!'

    def __init__(self, message=None, *args):
        super().__init__(message, *args)
        if message:
            self.error_msg += f' {message}'

    def __str__(self):
        return self.error_msg



class AgentExecutionError(Exception):
    error_code = 95102
    error_msg = 'Agent Execution Failed!'

    def __init__(self, message=None, *args):
        super().__init__(message, *args)
        if message:
            self.error_msg += f' {message}'

    def __str__(self):
        return self.error_msg


class ToolExecutionError(Exception):
    error_code = 95103
    error_msg = 'Tool Execution Failed!'

    def __init__(self, message=None, *args):
        super().__init__(message, *args)
        if message:
            self.error_msg += f' {message}'

    def __str__(self):
        return self.error_msg


class ModuleExecutionError(Exception):
    error_code = 95104
    error_msg = 'Module Execution Failed!'

    def __init__(self, message=None, *args):
        super().__init__(message, *args)
        if message:
            self.error_msg += f' {message}'

    def __str__(self):
        return self.error_msg

# 自定义锁超时异常
class AcquireLockTimeoutError(Exception):
    error_code = 95105
    error_msg = 'Lock Acquisition Failed!'

    def __init__(self, message=None, *args):
        super().__init__(message, *args)
        if message:
            self.error_msg += f' {message}'

    def __str__(self):
        return self.error_msg


class ExecutionTimeoutError(Exception):
    """自定义异常，指示函数执行超时"""
    error_code = 95106
    error_msg = 'Execution Time Out!'

    def __init__(self, message=None, *args):
        super().__init__(message, *args)
        if message:
            self.error_msg += f' {message}'

    def __str__(self):
        return self.error_msg

