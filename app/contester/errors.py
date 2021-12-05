# General exception of testing
class TestingException(Exception):
    ...


# Server response exception
class ServerResponseException(TestingException):
    ...


# Execution exception
class ExecutionException(TestingException):
    ...