"""
All necessary exceptions used in the project
for detection of the problems which arise during the process.
"""


class WrongCourierData(Exception):
    pass


class WrongOrderData(Exception):
    pass


class DataNotFound(Exception):
    pass


class WrongJSONRequest(Exception):
    pass


class MissingID(Exception):
    pass
