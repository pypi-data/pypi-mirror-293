import time
import requests
from .utils import get_function_name, get_memory_usage
from .config import ENDPOINT_URL, LICENSE_ID, LICENSE_SECRET
from .logger import log_info

def probe():
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()

            data = {
                'function_name': get_function_name(func),
                'execution_time': end_time - start_time,
                'memory_usage': get_memory_usage(),
                'timestamp': time.time(),
            }

            # print all configuration
            log_info(f"ENDPOINT_URL: {ENDPOINT_URL} LICENSE_ID: {LICENSE_ID} LICENSE_SECRET: {LICENSE_SECRET}")
            log_info(f"Sending data for {data['function_name']}: {data}")
            # requests.post(ENDPOINT_URL, json=data)

            return result
        return wrapper
    return decorator
