import random

class Block:
    def __init__(self, probability):
        if random.random() <= probability:
            self.blocked = True
        else:
            self.blocked = False

    def get_blocked(self):
        return self.blocked

    def set_blocked(self, b):
        self.blocked = b

    def __str__(self):
        return str(self.blocked)[0]