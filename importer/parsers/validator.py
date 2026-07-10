"""
LaundryBot V6

Parser Validator
"""


REQUIRED = [

    "job_no",

    "customer",

]


def validate(data):

    missing = []

    for field in REQUIRED:

        if not data.get(field):

            missing.append(field)

    return missing