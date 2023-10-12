class SyntaxException(Exception):
    def __init__(self, message):
        ...
        self.message = "Invalid syntax: " + message