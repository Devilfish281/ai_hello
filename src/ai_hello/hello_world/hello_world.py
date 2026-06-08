# src/ai_hello/hello_world/hello_world.py
"""Hello World module for the ai_hello project."""

# logger & setup_config
from ai_hello.my_utils.env_loader import load_dotenv_once
from ai_hello.setup_config import c_setup_config

load_dotenv_once()
setup_config = c_setup_config.get_instance()
logger = setup_config.get_logger()
_name: str | None = None


def i_hello_world_name_set(name: str) -> None:
    """Interface: save the name used by the Hello World module."""
    global _name

    _name = name


def i_hello_world_greet() -> None:
    """Interface: output a greeting."""
    if _name:
        logger.info(f"Hello {_name}")
        print(f"Hello {_name}")
    else:
        logger.info("Hello World")
        print("Hello World")
