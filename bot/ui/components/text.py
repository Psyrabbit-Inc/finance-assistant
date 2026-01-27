class Text:
    def __init__(self, text: str):
        self.text = text

    def render(self) -> str:
        return self.text + "\n"
