# src/ai_hello/main.py

# logger & setup_config
from ai_hello.my_utils.env_loader import load_dotenv_once
from ai_hello.setup_config import c_setup_config

load_dotenv_once()
setup_config = c_setup_config.get_instance()
logger = setup_config.get_logger()


from ai_hello.hello_world.hello_world import i_hello_world_greet, i_hello_world_name_set


def main() -> None:
    """Run the ai_hello program."""
    logger.info("Starting ai_hello program.")
    # TESTING_FLAG can be used to conditionally run code during development/testing
    logger.debug(f"TESTING_FLAG is set to: {setup_config.testing_flag}")
    i_hello_world_name_set("Mark")
    i_hello_world_greet()
    logger.info("Finished ai_hello program.")


if __name__ == "__main__":
    main()
