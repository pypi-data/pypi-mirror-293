import time
import grpc
import asyncio
from . import profiler_output_pb2_grpc as profiler_output_grpc
from .utils import *


class Profiler:
    def __init__(self, address, token):
        self._address = address
        self._token = token
        # todo: validate address and token

    async def send_profiler_output(self, profiler_data: profiler_output.ProfilerOutput):
        try:
            async with grpc.aio.insecure_channel(self._address) as channel:
                stub = profiler_output_grpc.ProfilerStub(channel)
                profiler_data.token = self._token
                response = await stub.SendProfilerOutput(profiler_data)
            if not response.ok:
                raise Exception(f"Error sending profiler output: {response.message}")
        except grpc.RpcError:
            raise Exception("Failed to send profiler output. Check the address or ensure the host is running.")

    def probe(self):
        def decorator(func):
            async def async_wrapper(*args, **kwargs):
                return await self._execute_and_profile(func, *args, **kwargs)

            def sync_wrapper(*args, **kwargs):
                return asyncio.run(self._execute_and_profile(func, *args, **kwargs))

            return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

        return decorator

    async def _execute_and_profile(self, func, *args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
        end_time = time.time()

        returned_value = profiler_output.ReturnedValue(
            value=str(result),
            type=type(result).__name__
        )

        profiler_data = profiler_output.ProfilerOutputRequest(
            profiler_output=profiler_output.ProfilerOutput(
                function_name=get_function_name(func),
                function_id=hash_function(func),
                function_caller=get_caller(),
                start_time=start_time,
                end_time=end_time,
                execution_time=(end_time - start_time) * 1000,  # in milliseconds
                memory_usage=get_memory_usage(),
                cpu_usage=get_cpu_usage(),
                func_params=get_func_params(args, func),
                returned_value=returned_value
            )
        )
        await self.send_profiler_output(profiler_data)
        return result