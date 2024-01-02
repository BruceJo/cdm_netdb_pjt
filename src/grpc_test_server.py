import grpc
from concurrent import futures
import test_proto_pb2
import test_proto_pb2_grpc

# Implementing the BookService
class BookServiceServicer(test_proto_pb2_grpc.BookServiceServicer):
    def GetBook(self, request, context):
        response = test_proto_pb2_grpc.BookService.GetBook(request=request,target=None)
        response.title = "The Hitchhiker's Guide to the Galaxy"
        response.author = "Douglas Adams"
        response.isbn = request.isbn
        return response

    def GetBooksViaAuthor(self, request, context):
        response = test_proto_pb2_grpc.BookService.GetBooksViaAuthor()
        response.extend([
            test_proto_pb2.Book(title="The Hitchhiker's Guide to the Galaxy", author="Douglas Adams", isbn=123456789),
            test_proto_pb2.Book(title="The Restaurant at the End of the Universe", author="Douglas Adams", isbn=234567890),
            test_proto_pb2.Book(title="Life, the Universe and Everything", author="Douglas Adams", isbn=345678901),
            test_proto_pb2.Book(title="So Long, and Thanks for All the Fish", author="Douglas Adams", isbn=456789012),
            test_proto_pb2.Book(title="Mostly Harmless", author="Douglas Adams", isbn=567890123)
        ])
        return response
    
    def GetGreatestBook(self, request, context):
        response = test_proto_pb2_grpc.GetGreatestBook()
        response.book.title = "The Hitchhiker's Guide to the Galaxy"
        response.book.author = "Douglas Adams"
        response.book.isbn = 123456789
        return response
    
    def GetBooks(self, request, context):
        response = test_proto_pb2_grpc.GetBooks()
        response.extend([
            test_proto_pb2.Book(title="The Hitchhiker's Guide to the Galaxy", author="Douglas Adams", isbn=123456789),
            test_proto_pb2.Book(title="The Restaurant at the End of the Universe", author="Douglas Adams", isbn=234567890),
            test_proto_pb2.Book(title="Life, the Universe and Everything", author="Douglas Adams", isbn=345678901),
            test_proto_pb2.Book(title="So Long, and Thanks for All the Fish", author="Douglas Adams", isbn=456789012),
            test_proto_pb2.Book(title="Mostly Harmless", author="Douglas Adams", isbn=567890123)
        ])
        return response
    
# Creating a gRPC server
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    test_proto_pb2_grpc.add_BookServiceServicer_to_server(BookServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
