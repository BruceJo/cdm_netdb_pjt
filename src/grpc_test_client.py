import grpc
import test_proto_pb2
import test_proto_pb2_grpc

# Establishing a connection to the server
channel = grpc.insecure_channel('localhost:50051')
stub = test_proto_pb2_grpc.BookServiceStub(channel)

# Example of using the GetBook method
response = stub.GetBook(test_proto_pb2.GetBookRequest(isbn=123456789))
print("GetBook response:", response)