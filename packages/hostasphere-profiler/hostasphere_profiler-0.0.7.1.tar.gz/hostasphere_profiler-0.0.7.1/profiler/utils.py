import inspect
import os
import psutil

def get_function_name(func):
    return func.__name__

def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss