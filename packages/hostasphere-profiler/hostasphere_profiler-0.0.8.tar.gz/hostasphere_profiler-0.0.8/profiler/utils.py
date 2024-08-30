from . import profiler_output_pb2 as profiler_output
import inspect
import os
import psutil

def get_function_name(func):
    return func.__name__

def get_func_params(args, func):
    result = []
    sig = inspect.signature(func)
    params = sig.parameters
    for i, arg in enumerate(args):
        arg_name = list(params.keys())[i] if i < len(params) else 'N/A'
        result.append(profiler_output.FuncParams(
            arg=str(arg),
            arg_name=arg_name,
            type=type(arg).__name__
        ))
    return result

def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss

def get_cpu_usage():
    process = psutil.Process(os.getpid())
    return process.cpu_percent()