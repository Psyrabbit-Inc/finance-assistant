class Header:
    def __init__(self, title: str, emoji: str = "✨"):
        self.title = title
        self.emoji = emoji

    def render(self) -> str:
        return f"{self.emoji} *{self.title}*\n"
