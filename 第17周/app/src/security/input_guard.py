import re

class InputGuard:
    def __init__(self, max_length=200):
        self.max_length = max_length

    def validate(self, text):
        if text is None or text.strip() == "":
            return False, "Empty input"

        if len(text) > self.max_length:
            return False, "Input too long"

        if not self.is_valid_utf8(text):
            return False, "Invalid characters"

        if self.is_repeated(text):
            return False, "Repeated input detected"

        return True, "OK"

    def is_valid_utf8(self, text):
        try:
            text.encode("utf-8")
            return True
        except:
            return False

    def is_repeated(self, text):
        return len(set(text)) <= 2
