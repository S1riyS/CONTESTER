# General exception of testing
class TestingSystemError(Exception):
    def __init__(self):
        self.message = 'Testing system error'


# Server response exception
class ServerResponseError(TestingSystemError):
    def __init__(self):
        super().__init__()
        self.message = 'Server Response Error'


# Execution exception
class ExecutionError(TestingSystemError):
    def __init__(self):
        super().__init__()
        self.message = 'Execution Error'


# Wrong answer exception
class WrongAnswerError(TestingSystemError):
    def __init__(self):
        super().__init__()
        self.message = 'Wrong Answer'


# Wrong answer exception
class TimeLimitError(TestingSystemError):
    def __init__(self):
        super().__init__()
        self.message = 'Time Limit Error'
