"""
LaundryBot V6

Page Object
"""


class Page:

    def __init__(self, number):

        self.number = number

        self.lines = []

    def add(self, line):

        self.lines.append(line)

    def __iter__(self):

        return iter(self.lines)