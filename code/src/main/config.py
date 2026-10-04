from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[3]

DOCS_DIR = REPO_ROOT / "documents"
PROMPTS_DIR = REPO_ROOT / "code/src/prompts"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=REPO_ROOT / ".env", extra="ignore")

    github_token: str
    gemini_api_key: str
    codebase_repo_path: str
    documentation_repo_path: str
    pr_number: int


settings = Settings()
