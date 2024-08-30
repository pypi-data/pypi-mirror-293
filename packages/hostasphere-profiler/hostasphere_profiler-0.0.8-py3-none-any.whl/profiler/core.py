import time
import grpc

from . import profiler_output_pb2_grpc as profiler_output_grpc, profiler_output_pb2 as profiler_output
from .utils import get_function_name, get_memory_usage, get_cpu_usage, get_func_params

class Profiler:
    def __init__(self, address, token):
        self._address = address
        self._token = token

    def sendProfilerOutput(self, profiler_data: profiler_output.ProfilerOutput):
        try:
            with grpc.insecure_channel(self._address) as channel:
                stub = profiler_output_grpc.ProfilerStub(channel)
                profiler_data.token = self._token
                response = stub.SendProfilerOutput(profiler_data)
            if not response.ok:
                raise Exception(
                    f"Error sending profiler output: {response.message}")
        except grpc.RpcError as e:
            raise Exception("Impossible to send profiler output check address, or check if hostaspere is running")


    def probe(self):
        def decorator(func):
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = func(*args, **kwargs)
                end_time = time.time()

                profiler_data = profiler_output.ProfilerOutputRequest(
                    profiler_output=profiler_output.ProfilerOutput(
                        function_name=get_function_name(func),
                        start_time=start_time,
                        end_time=end_time,
                        memory_usage=get_memory_usage(),
                        cpu_usage=get_cpu_usage(),
                        func_params=get_func_params(args, func)
                    )
                )
                self.sendProfilerOutput(profiler_data)
                return result
            return wrapper
        return decorator
