class Card:
    def __init__(self, components: list):
        self.components = components

    def render(self) -> str:
        return "".join(c.render() for c in self.components) + "\n"
