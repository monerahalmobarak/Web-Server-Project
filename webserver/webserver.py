import asyncio
import logging
from functools import wraps
from abc import ABC, abstractmethod
import unittest

# The Needed Imports
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("my-logger-app")

# The Function to read HTML content 
async def read_file_async(file_path):
    loop = asyncio.get_event_loop()
    try:
        with open(file_path, 'rb') as file:
            return await loop.run_in_executor(None, file.read)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return b""

# The Decorator for Logging Requests
def log_request(func):
    @wraps(func)
    async def wrapper(request, *args, **kwargs):
        request_id = id(request)  
        logger.debug(f"Request {request_id} received: {request}")
        response = await func(request, *args, **kwargs)
        logger.debug(f"Response {request_id}: {response}")
        return response
    return wrapper

# The Decorator for Authorizing Requests
def authorize_request(func):
    @wraps(func)
    async def wrapper(request, *args, **kwargs):
        if request.get('HTTP_AUTHORIZATION') == 'Basic dXNlcm5hbWU6cGFzc3dvcmQ=':
            return await func(request, *args, **kwargs)
        else:
            unauthorized_content = await read_file_async("unauthorization.html")
            return '401 Unauthorized', [('Content-Type', 'text/html')], streaming_response_generator([unauthorized_content])
    return wrapper

# Async generator for streaming HTTP Response Incrementally
async def streaming_response_generator(body):
    for part in body:
        yield part
        await asyncio.sleep(0.5)

# Base Request Handler Class
class BaseRequestHandler(ABC):
    @abstractmethod
    async def handle_request(self, request):
        pass

# The Class for GET Requests
class GetRequestHandler(BaseRequestHandler):
    async def handle_request(self, request):
        logger.debug("GET request handled")
        await asyncio.sleep(2)  # Changed to 2 seconds for testing
        if request['PATH_INFO'] == '/http/vrhvevnd.com':
            return '404 Not Found', [('Content-Type', 'text/html')], streaming_response_generator([b"\n\n", b"Page not found", b"\n\n", await read_file_async("not_found.html")])
        return '200 OK', [('Content-Type', 'text/html')], streaming_response_generator([b"\n\n", b"GET request successful", b"\n\n", await read_file_async("authorization.html")])

# The Class for POST Requests
class PostRequestHandler(BaseRequestHandler):
    async def handle_request(self, request):
        logger.debug("POST request handled")
        return '200 OK', [('Content-Type', 'text/html')], streaming_response_generator([b"\n\n", b"POST request successful", b"\n\n", await read_file_async("authorization.html"), b"Hello Post", b"\n\n"])

# Request Iterator for Handling The requests
class RequestIterator:
    def __init__(self, requests):
        self._requests = requests
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._requests):
            result = self._requests[self._index]
            self._index += 1
            return result
        else:
            raise StopIteration

# Asynchronous request handler
async def async_request_handler(requests):
    tasks = [process_request(request) for request in RequestIterator(requests)]
    for task in asyncio.as_completed(tasks):
        response = await task
        yield response

# Process each request and apply decorators for logging and authorization
@log_request
@authorize_request
async def process_request(request):
    if request['REQUEST_METHOD'] == 'GET':
        handler = GetRequestHandler()
    elif request['REQUEST_METHOD'] == 'POST':
        handler = PostRequestHandler()
    else:
        return '405 Method Not Allowed', [('Content-Type', 'text/html')], streaming_response_generator([b"Method Not Allowed"])
    return await handler.handle_request(request)

# Context manager 
class ServerContextManager:
    def __enter__(self):
        print("Starting server...")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Stopping server...")

# Singleton pattern
class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class WebServer(metaclass=SingletonMeta):
    async def run(self):
        with ServerContextManager():
            requests = [
                {
                    'REQUEST_METHOD': 'GET',
                    'PATH_INFO': '/http/example.com',
                    'HTTP_AUTHORIZATION': 'Basic dXNlcm5hbWU6cGFzc3dvcmQ='
                },
                {
                    'REQUEST_METHOD': 'GET',
                    'PATH_INFO': '/http/example2.com',
                    'HTTP_AUTHORIZATION': 'Basic dXNlcm5hbW33U6cGFzc3dvcmQ='
                },
                {
                    'REQUEST_METHOD': 'GET',
                    'PATH_INFO': '/http/vrhvevnd.com',
                    'HTTP_AUTHORIZATION': 'Basic dXNlcm5hbWU6cGFzc3dvcmQ='
                },
                {
                    'REQUEST_METHOD': 'POST',
                    'PATH_INFO': '/http/example.com',
                    'HTTP_AUTHORIZATION': 'Basic dXNlcm5hbWU6cGFzc3dvcmQ='
                }
            ]
            # Process requests asynchronously
            async for response in async_request_handler(requests):
                status, headers, body = response
                logger.debug(f"Response: {status}, {headers}")
                print(f"{status}\n")
                for header in headers:
                    print(f"{header[0]}: {header[1]}")
                print()
                async for part in body:
                    if isinstance(part, bytes):
                        print(part.decode('utf-8'))
                    else:
                        print(part)

if __name__ == "__main__":
    server = WebServer()
    asyncio.run(server.run())


# Unit tests
class TestWebServer(unittest.TestCase):

    def setUp(self):
        self.server = WebServer()

    async def run_server(self, requests):
        responses = []
        async for response in async_request_handler(requests):
            responses.append(response)
        return responses

    def test_get_request(self):
        requests = [
            {
                'REQUEST_METHOD': 'GET',
                'PATH_INFO': '/http/example.com',
                'HTTP_AUTHORIZATION': 'Basic dXNlcm5hbWU6cGFzc3dvcmQ='
            }
        ]
        responses = asyncio.run(self.run_server(requests))
        self.assertEqual(responses[0][0], '200 OK')

    def test_post_request(self):
        requests = [
            {
                'REQUEST_METHOD': 'POST',
                'PATH_INFO': '/http/example.com',
                'HTTP_AUTHORIZATION': 'Basic dXNlcm5hbWU6cGFzc3dvcmQ='
            }
        ]
        responses = asyncio.run(self.run_server(requests))
        self.assertEqual(responses[0][0], '200 OK')

    def test_unauthorized_request(self):
        requests = [
            {
                'REQUEST_METHOD': 'GET',
                'PATH_INFO': '/http/example.com',
                'HTTP_AUTHORIZATION': 'Basic invalid'
            }
        ]
        responses = asyncio.run(self.run_server(requests))
        self.assertEqual(responses[0][0], '401 Unauthorized')

    def test_not_found_request(self):
        requests = [
            {
                'REQUEST_METHOD': 'GET',
                'PATH_INFO': '/http/vrhvevnd.com',
                'HTTP_AUTHORIZATION': 'Basic dXNlcm5hbWU6cGFzc3dvcmQ='
            }
        ]
        responses = asyncio.run(self.run_server(requests))
        self.assertEqual(responses[0][0], '404 Not Found')


if __name__ == "__main__":
    unittest.main()
