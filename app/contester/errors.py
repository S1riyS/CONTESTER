# General exception of testing
class TestingError(Exception):
    ...


# Server response exception
class ServerResponseError(TestingError):
    ...


# Execution exception
class ExecutionError(TestingError):
    ...