# Web Server Project

## Overview
This project involves building a basic web server that handles HTTP requests and generates appropriate responses, including streaming responses using generators. It leverages various advanced features of Python, including decorators, generators, iterators, coroutines & async iterators, inheritance, polymorphism, context managers, and singletons.

## Project Structure
webserver/
|
|-- webserver.py
|-- unauthorization.html
|-- not_found.html
|-- authorization.html

## Files
- **`webserver.py`** : Main implementation file containing the web server code.
- unauthorization.html: HTML content to display when a request is unauthorized.
- not_found.html: HTML content to display when a requested page is not found.
- authorization.html: HTML content to display when a request is successfully authorized.
- README.md: This documentation file.

## Decorators
- log_request: Logs each incoming request and its response.
- authorize_request: Checks if a request is authorized by comparing the authorization header.

## Generators
- response_generator: Generates HTTP responses.
- streaming_response_generator: Yields parts of a response incrementally.
  
## Iterators
- RequestIterator: Implements the iterator protocol to manage multiple requests.
  
## Coroutines & Async Iterators
- async_request_handler: Asynchronously processes requests using async iterators.
  
## Inheritance and Polymorphism
- BaseRequestHandler: Abstract base class with an abstract method handle_request.
- GetRequestHandler: Handles GET requests by inheriting from BaseRequestHandler.
- PostRequestHandler: Handles POST requests by inheriting from BaseRequestHandler.

## Context Managers
- ServerContextManager: Manages the server's lifecycle (start and stop) using context management.

## Singleton Pattern
- WebServer: Ensures there is only one instance of the server using the singleton pattern.
Streaming Responses
- Uses streaming_response_generator for sending data incrementally in response handlers.

## How to Run the Server
- Prerequisites
- Python 3.7+
- asyncio
- unittest

## Dependencies
- Python 3.7+
- asyncio

## Documentation

## Key Functions and Classes

#### Decorators
- log_request: Logs requests and responses.
- authorize_request: Authorizes requests based on the HTTP_AUTHORIZATION header.
  
#### Generators
- streaming_response_generator: Yields parts of the response incrementally with a delay.
Iterators
- RequestIterator: Manages and iterates over multiple requests.
  
#### Coroutines & Async Iterators
- async_request_handler: Handles multiple requests asynchronously.
- BaseRequestHandler and Derived Classes
- BaseRequestHandler: Abstract base class for handling requests.
- GetRequestHandler: Handles GET requests.
- PostRequestHandler: Handles POST requests.
  
#### Context Manager
- ServerContextManager: Manages the server's lifecycle.
  
#### Singleton Pattern
- WebServer: Ensures a single instance of the web server.

## Example Requests
The server handles the following example requests defined in WebServer.run method:

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

## Output
The server will log and print responses for each request, showing the HTTP responses.and the appropriate HTML content.

https://github.com/user-attachments/assets/1146f66c-7023-4960-99fa-208ba3cda816




