from .divider import Divider

class Section:
    def __init__(self, title: str, components: list, emoji: str = "📌"):
        self.title = title
        self.components = components
        self.emoji = emoji

    def render(self) -> str:
        header = f"{self.emoji} *{self.title}*\n"
        divider = Divider().render()
        content = "".join(c.render() for c in self.components)
        return f"{header}{divider}{content}\n"
