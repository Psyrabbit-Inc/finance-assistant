class StatRow:
    def __init__(self, emoji: str, label: str, value):
        self.emoji = emoji
        self.label = label
        self.value = value

    def render(self) -> str:
        return f"{self.emoji} *{self.label}*: {self.value}\n"
