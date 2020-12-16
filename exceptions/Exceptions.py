class EmptyStudyTableException(BaseException):
    """
    Exception if study data table is empty resulting in "No data available".
    """
    pass


class MissingCredentialsException(BaseException):
    """
    Exception if credentials are missing
    """
    pass


class NoSuchUserException(BaseException):
    """
    Exception if entered login username does not exist
    """
    pass


class StudyAlreadyExistsException(BaseException):
    """
    Exception if the study folder already exists
    """
    pass


class StudyCsvMissingException(BaseException):
    """
    Exception if there is no csv file which contains enrolled subjects information
    """
    pass


class WrongPasswordException(BaseException):
    """
    Exception if password for existing user is wrong
    """
    pass
