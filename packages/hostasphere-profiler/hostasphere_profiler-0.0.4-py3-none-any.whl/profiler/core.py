import time
from .utils import get_function_name, get_memory_usage
from .logger import log_info

class Profiler:
    def __init__(self, endpoint_url, license_id, license_secret):
        self._endpoint_url = endpoint_url
        self._license_id = license_id
        self._license_secret = license_secret

    def probe(self):
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

                log_info(f"ENDPOINT_URL: {self._endpoint_url} LICENSE_ID: {self._license_id} LICENSE_SECRET: {self._license_secret}")
                log_info(f"Sending data for {data['function_name']}: {data}")
                # requests.post(self.ENDPOINT_URL, json=data)

                return result
            return wrapper
        return decorator
