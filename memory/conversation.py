from collections import defaultdict


class ConversationMemory:

    def __init__(self):
        self.data = defaultdict(dict)

    def get(self, session_id):

        return self.data[session_id]

    def update(self, session_id, model=None, question=None):

        if model:
            self.data[session_id]["model"] = model

        if question:
            self.data[session_id]["question"] = question

    def clear(self, session_id):

        if session_id in self.data:
            del self.data[session_id]


memory = ConversationMemory()