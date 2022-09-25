import random

class Block:
    def __init__(self, probability):
        """
        initializes cell to be blocked based on probability p.
        """
        if random.random() <= probability:
            self.blocked = True
        else:
            self.blocked = False

    def get_blocked(self):
        """
        get_blocked retrieves whether block is blocked (T/F).
        """
        return self.blocked

    def set_blocked(self, b):
        """
        set_blocked makes a block blocked (T/F). 
        """
        self.blocked = b

    def __str__(self):
        """
        returns first char (T/F) if block is blocked.
        """
        return str(self.blocked)[0]