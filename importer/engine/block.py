"""
LaundryBot V6

Block Object
"""


class Block:

    def __init__(self):

        self.lines = []

    def add(self, line):

        self.lines.append(line)

    def text(self):

        return "\n".join(

            str(i)

            for i in self.lines

        )

    def __iter__(self):

        return iter(self.lines)

    def __len__(self):

        return len(self.lines)