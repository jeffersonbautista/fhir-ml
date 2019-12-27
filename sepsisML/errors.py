class PatientNotFound(Exception):
    def __init__(self, message):
        super(PatientNotFound, self).__init__(message)
        self.message = message

class InvalidId(Exception):
    def __init__(self, message):
        super(PatientNotFound, self).__init__(message)
        self.message = message 

class InvalidVersion(Exception):
    def __init__(self, message):
        super(InvalidVersion, self).__init__(message)
        self.message = message

class NotEnoughData(Exception):
    def __init__(self, message):
        super(NotEnoughData, self).__init__(message)
        self.message = message
    