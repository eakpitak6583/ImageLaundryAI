"""
LaundryBot V6

Document Object
"""


class Document:

    def __init__(self, text):

        self.raw = text

        self.lines = []

    def add(self, line):

        self.lines.append(line)

    def __iter__(self):

        return iter(self.lines)

    def __len__(self):

        return len(self.lines)