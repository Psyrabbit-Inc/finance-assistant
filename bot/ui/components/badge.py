class Badge:
    def __init__(self, emoji: str, text: str):
        self.emoji = emoji
        self.text = text

    def render(self) -> str:
        return f"{self.emoji} {self.text}\n"
