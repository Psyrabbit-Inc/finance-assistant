from typing import List, Optional


class VStack:
    """
    Вертикальный стек компонентов.
    Пример использования:
        VStack([Header("Текст"), Divider(), Badge("OK")])
    """

    def __init__(self, children: List, spacing: int = 1):
        self.children = children
        self.spacing = spacing

    def render(self) -> str:
        """
        Рендерит компоненты друг под другом.
        Каждый компонент обязан иметь метод .render() -> str
        """
        parts = []
        for child in self.children:
            if hasattr(child, "render"):
                parts.append(child.render())
            else:
                parts.append(str(child))
        return "\n" * self.spacing.join(parts)


class HStack:
    """
    Горизонтальный стек компонентов.
    Нужен реже, но пригодится позже.
    """

    def __init__(self, children: List, separator: str = "   "):
        self.children = children
        self.separator = separator

    def render(self) -> str:
        rendered = []
        for child in self.children:
            if hasattr(child, "render"):
                rendered.append(child.render())
            else:
                rendered.append(str(child))
        return self.separator.join(rendered)


class Spacer:
    """
    Просто пустая строка между компонентами.
    """

    def render(self) -> str:
        return ""
