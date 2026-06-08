# src/ai_hello/setup_config.py
import logging
import os
import threading
from pathlib import Path
from typing import ClassVar

from langchain_openai import ChatOpenAI
from pydantic import BaseModel, ConfigDict, Field

from ai_hello.my_utils.env_loader import load_dotenv_once
from ai_hello.my_utils.llm_loader import get_llm_or_init
from ai_hello.my_utils.logger_setup import setup_logger

try:
    load_dotenv_once()
except Exception:
    pass


LOGGER_PROJECT_NAME = "ai_hello"
DEFAULT_PROJECT_NAME = "AI Hello"
DEFAULT_OPENAI_MODEL = "gpt-5.1"
DEFAULT_PROJECT_ROOT = Path(__file__).resolve().parents[2]


class c_setup_config(BaseModel):
    """Represents setup variables for the ai_hello project."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    project_name: str = Field(
        default_factory=lambda: c_setup_config.get_env(
            "PROJECT_NAME",
            DEFAULT_PROJECT_NAME,
        ),
        description="Human-readable project name.",
    )

    project_root: Path = Field(
        default=DEFAULT_PROJECT_ROOT,
        description="Root directory for the ai_hello project.",
    )

    openai_model: str = Field(
        default_factory=lambda: c_setup_config.get_env(
            "OPENAI_MODEL",
            DEFAULT_OPENAI_MODEL,
        ),
        description="Default OpenAI model to use for LLM interactions.",
    )

    testing_flag: bool = Field(
        default_factory=lambda: c_setup_config.env_bool("TESTING_FLAG", False),
        description="Flag to indicate if the application is running in testing mode.",
    )

    logger: logging.Logger | None = Field(
        default=None,
        exclude=True,
        repr=False,
        description="Runtime logger instance.",
    )

    llm: ChatOpenAI | None = Field(
        default=None,
        exclude=True,
        repr=False,
        description="Runtime LLM instance.",
    )

    _instance: ClassVar["c_setup_config | None"] = None
    _lock: ClassVar[threading.Lock] = threading.Lock()

    @staticmethod
    def get_env(name: str, default: str | None = None) -> str:
        """Return a cleaned environment variable value or the provided default."""
        value = os.getenv(name, default)

        if value is None:
            raise ValueError(f"Missing required environment variable: {name}")

        return str(value).strip().strip("'\"")

    @staticmethod
    def get_required_env(name: str) -> str:
        """Return a required environment variable value or raise a clear error."""
        value = os.getenv(name)

        if value is None or not value.strip():
            raise ValueError(f"Missing required environment variable: {name}")

        return value.strip().strip("'\"")

    @staticmethod
    def env_bool(name: str, default: bool = False) -> bool:
        """Read an environment variable as a boolean value."""
        raw_value = os.getenv(name)

        if raw_value is None:
            return default

        return raw_value.strip().lower() in {"1", "true", "yes", "y", "on"}

    def i_setup_config_secret_values(self) -> tuple[str, ...]:
        """Return secret values that should be redacted from logs."""
        secret_values: list[str] = []

        openai_api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if openai_api_key:
            secret_values.append(openai_api_key)

        return tuple(secret_values)

    def set_logger(self, logger: logging.Logger) -> None:
        """Set the logger instance used by the application."""
        self.logger = logger

    def get_logger(self) -> logging.Logger:
        """Return the configured logger, initializing it once if needed."""
        if self.logger is None:
            self.logger = setup_logger(
                LOGGER_PROJECT_NAME,
                secret_values=self.i_setup_config_secret_values(),
            )
            self.logger.info("Logger started.")

        return self.logger

    def get_llm(self) -> ChatOpenAI:
        """Return the configured LLM, initializing it once if needed."""
        if self.llm is None:
            self.llm = get_llm_or_init(
                self,
                temperature=0.0,
                streaming=True,
            )

        return self.llm

    def validate_initialization(self, *, require_llm: bool = False) -> None:
        """Validate required ai_hello configuration values."""
        logger = self.get_logger()
        logger.info("Validating configuration initialization...")

        if not self.project_name.strip():
            logger.error("PROJECT_NAME cannot be empty.")
            raise ValueError("PROJECT_NAME cannot be empty.")

        if not self.openai_model.strip():
            logger.error("OPENAI_MODEL cannot be empty.")
            raise ValueError("OPENAI_MODEL cannot be empty.")

        if not self.project_root.exists():
            logger.error("Project root does not exist: %s", self.project_root)
            raise ValueError(f"Project root does not exist: {self.project_root}")

        if not require_llm:
            return

        openai_api_key = self.get_required_env("OPENAI_API_KEY")

        if len(openai_api_key) < 20:
            logger.error("OPENAI_API_KEY looks too short to be valid.")
            raise ValueError("OPENAI_API_KEY looks too short to be valid.")

        if self.llm is None:
            self.get_llm()

    def to_dict(self) -> dict[str, object]:
        """Return a safe dictionary representation of the configuration."""
        return {
            "project_name": self.project_name,
            "project_root": str(self.project_root),
            "openai_model": self.openai_model,
            "testing_flag": self.testing_flag,
            "openai_api_key_configured": bool(os.getenv("OPENAI_API_KEY", "").strip()),
            "logger_initialized": self.logger is not None,
            "llm_initialized": self.llm is not None,
        }

    def __repr__(self) -> str:
        """Return a safe developer-friendly representation of this config."""
        return (
            "c_setup_config("
            f"project_name={self.project_name!r}, "
            f"project_root={str(self.project_root)!r}, "
            f"openai_model={self.openai_model!r}, "
            f"testing_flag={self.testing_flag!r}, "
            f"logger_initialized={self.logger is not None!r}, "
            f"llm_initialized={self.llm is not None!r}"
            ")"
        )

    @classmethod
    def get_instance(cls) -> "c_setup_config":
        """Return the shared thread-safe setup config instance."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()

        return cls._instance
