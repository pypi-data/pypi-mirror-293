import json
import time
import grpc

from . import profiler_output_pb2_grpc, profiler_output_pb2
from .utils import get_function_name, get_memory_usage
from .logger import log_info

class Profiler:
    def __init__(self, address, token):
        self._address = address
        self._token = token

    def sendProfilerOutput(self, data):
        with grpc.insecure_channel(self._address) as channel:
            stub = profiler_output_pb2_grpc.ProfilerStub(channel)
            response = stub.SendProfilerOutput(profiler_output_pb2.ProfilerOutputRequest(
                token=self._token,
                profiler_output=profiler_output_pb2.ProfilerOutput(
                    function_name=data['function_name'],
                    start_time=data['start_time'],
                    end_time=data['end_time'],
                    memory_usage=data['memory_usage'],
                    cpu_usage=data['cpu_usage'],
                    # parameters=data['parameters'],
                )
            ))
        print(f"Result: {response.ok}")

    def probe(self):
        def decorator(func):
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = func(*args, **kwargs)
                end_time = time.time()

                try:
                    args_json = json.dumps(args)
                    kwargs_json = json.dumps(kwargs)
                except TypeError as e:
                    log_info(f"Error serializing arguments: {e}")
                    args_json = str(args)
                    kwargs_json = str(kwargs)

                data = {
                    'function_name': get_function_name(func),
                    'start_time': start_time,
                    'end_time': end_time,
                    'execution_time': end_time - start_time,
                    'memory_usage': get_memory_usage(),
                    'cpu_usage': 0,
                    'parameters': {'args': args_json, 'kwargs': kwargs_json},
                    'timestamp': time.time(),
                }

                self.sendProfilerOutput(data)
                return result
            return wrapper
        return decorator
