"""Naming helpers."""


def pascal_to_snake_case(name: str) -> str:
    """Pascal Case to snake_case"""
    snake = ""
    for char in name:
        if char.isupper():
            snake += "_"
        snake += char.lower()
    return snake


def snake_to_pascal_case(name: str) -> str:
    """snake_case to PascalCase"""
    return "".join(map(lambda x: x.title(), name.split("_")))
