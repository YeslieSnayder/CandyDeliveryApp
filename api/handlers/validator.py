import re

from flask import request
from model.exeptions import *


async def validate_and_return_json():
    """
    The method checks the correctness of the entered data.
    Request should be json-type (Content-Type: application/json) and contains at least 1 field.
    :return: JSON-object from the request - if the request is correct
    """
    if request is None or not request.is_json \
            or re.search(r'{.*[\'\"].*[\'\"].*:.*}', request.data.__str__()) is None:
        raise WrongJSONRequest
    try:
        return request.get_json()
    except Exception:
        raise WrongJSONRequest()
