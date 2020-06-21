class StudyAlreadyExistsException(Exception):
    """
    Exception if the study folder already exists
    """
    pass


class StudyCsvMissingException(Exception):
    """
    Exception if there is no csv file which contains enrolled subjects information
    """
    pass


class NoSuchUserException(Exception):
    """
    Exception if entered login username does not exist
    """
    pass


class WrongPasswordException(Exception):
    """
    Exception if password for existing user is wrong
    """
    pass


class MissingCredentialsException(Exception):
    """
    Exception if credentials are missing
    """
    pass


class EmptyStudyTableException(Exception):
    """
    Exception if study data table is empty resulting in "No data available".
    """
    pass
