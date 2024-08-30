import grpc
from concurrent import futures

from profiler import profiler_output_pb2, profiler_output_pb2_grpc

#syntax = "proto3";
#
# package profiler_output;
#
# service Profiler {
#     rpc SendProfilerOutput (ProfilerOutputRequest) returns (Response);
# }
#
# message FuncParams {
#     repeated string args = 1;
#     repeated string kwargs = 2;
# }
#
# message ProfilerOutput {
#     string function_name = 1;
#     float start_time = 2;
#     float end_time = 3;
#     float memory_usage = 4;
#     float cpu_usage = 5;
#     repeated FuncParams func_params = 6;
# }
#
# message ProfilerOutputRequest {
#     string token = 1;
#     ProfilerOutput profiler_output = 3;
# }
#
# message Response {
#     bool ok = 1;
#     string message = 2;
# }

class ProfilerServicer(profiler_output_pb2_grpc.ProfilerServicer):
    def SendProfilerOutput(self, request, context):
        func_params_list = []
        for func_param in request.profiler_output.func_params:
            func_params_list.append(
                f"args={func_param.args}, kwargs={func_param.kwargs}")

        print(f"Function Name: {request.profiler_output.function_name}"
              f" License ID: {request.token}"
              f" Start Time: {request.profiler_output.start_time}"
              f" End Time: {request.profiler_output.end_time}"
              f" Memory Usage: {request.profiler_output.memory_usage}"
              f" CPU Usage: {request.profiler_output.cpu_usage}"
              f" Parameters: {func_params_list}")
        return profiler_output_pb2.Response(ok=True, message="Success")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    profiler_output_pb2_grpc.add_ProfilerServicer_to_server(ProfilerServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
