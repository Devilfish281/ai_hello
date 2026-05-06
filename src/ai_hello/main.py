# src/ai_hello/main.py
from ai_hello.hello_world.hello_world import (
    i_hello_world_greet,
    i_hello_world_name_set,
)


def main() -> None:
    """Run the ai_hello program."""
    i_hello_world_name_set("Mark")
    i_hello_world_greet()


if __name__ == "__main__":
    main()
