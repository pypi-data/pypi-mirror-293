import grpc
from concurrent import futures

from profiler import profiler_output_pb2, profiler_output_pb2_grpc

class ProfilerServicer(profiler_output_pb2_grpc.ProfilerServicer):
    def SendProfilerOutput(self, request, context):
        print(f"Function Name: {request.profiler_output.function_name}"
                f"License ID: {request.token}"
                f"Start Time: {request.profiler_output.start_time}"
                f"End Time: {request.profiler_output.end_time}"
                f"Memory Usage: {request.profiler_output.memory_usage}"
                f"CPU Usage: {request.profiler_output.cpu_usage}")
                # f"Parameters: {request.profiler_output.parameters}")
        return profiler_output_pb2.Response(ok=True, message="Success")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    profiler_output_pb2_grpc.add_ProfilerServicer_to_server(ProfilerServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
