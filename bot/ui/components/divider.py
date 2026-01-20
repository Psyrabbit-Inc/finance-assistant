class Divider:
    def __init__(self, char="─", length=14):
        self.char = char
        self.length = length

    def render(self) -> str:
        return self.char * self.length + "\n"
