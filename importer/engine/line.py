"""
LaundryBot V6

Line Object
"""


class Line:

    def __init__(self, text):

        self.text = text.strip()

    def __str__(self):

        return self.text