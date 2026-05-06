# src/ai_hello/hello_world/hello_world.py
"""Hello World module for the ai_hello project."""

_name: str | None = None


def i_hello_world_name_set(name: str) -> None:
    """Interface: save the name used by the Hello World module."""
    global _name

    _name = name


def i_hello_world_greet() -> None:
    """Interface: output a greeting."""
    if _name:
        print(f"Hello {_name}")
    else:
        print("Hello World")
