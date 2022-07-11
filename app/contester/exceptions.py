# General exception of testing
class ContesterError(Exception):
    def __init__(self):
        self.message = 'Testing system error'


# Server response exception
class ApiServiceError(ContesterError):
    def __init__(self):
        super().__init__()
        self.message = 'Server Response Error'


# Execution exception
class ExecutionError(ContesterError):
    def __init__(self):
        super().__init__()
        self.message = 'Execution Error'


# Wrong answer exception
class WrongAnswerError(ContesterError):
    def __init__(self):
        super().__init__()
        self.message = 'Wrong Answer'


# Wrong answer exception
class TimeOutError(ContesterError):
    def __init__(self):
        super().__init__()
        self.message = 'Time Limit Error'
