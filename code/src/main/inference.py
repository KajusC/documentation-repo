from typing import Literal

from google import genai
from pydantic import BaseModel

from src.common.tree import list_files
from src.main.config import DOCS_DIR, PROMPTS_DIR, settings

MODEL = "gemini-3.5-flash-lite"

client = genai.Client(api_key=settings.gemini_api_key)
TOPIC_PROMPT = (PROMPTS_DIR / "topic_and_path.md").read_text(encoding="utf-8")
UPDATE_PROMPT = (PROMPTS_DIR / "documentation_update.md").read_text(encoding="utf-8")


class Decision(BaseModel):
    status: Literal["updated", "created", "unchanged", "removed"]
    documentation_path: str = ""
    documentation: str = ""


class NewDoc(BaseModel):
    path: str


class Topic(BaseModel):
    topic: str
    documentation: list[NewDoc] = []


def ask(system_prompt, schema, text):
    response = client.models.generate_content(
        model=MODEL,
        contents=text,
        config={
            "system_instruction": system_prompt,
            "temperature": 1,
            "response_mime_type": "application/json",
            "response_schema": schema,
            "thinking_config": {"thinking_level": "MEDIUM"},
        },
    )
    return response.parsed


def new_pages(change):
    """Nothing documents this file yet, so ask where its docs should go."""
    topic = ask(
        TOPIC_PROMPT,
        Topic,
        f"Code change: `{change['path']}`\n Methods: `{change['methods']}`\n"
        f"Documentation tree: `{list_files(DOCS_DIR)}`",
    )
    if topic is None:
        return []
    text = f"# {topic.topic}\n\n## Purpose \n\n## Sources"
    return [{"path": doc.path, "text": text} for doc in topic.documentation]


def review(pages, change):
    parts = [f"Documentation path: `{p['path']}`\n\n{p['text']}" for p in pages]
    parts.append(f"Code changes:\n\n```diff\n{change['patch']}\n```")
    for method in change["methods"]:
        parts.append(
            f"Changed method `{method['name']}`:\n\n```csharp\n{method['source']}\n```"
        )
    return ask(UPDATE_PROMPT, list[Decision], "\n\n".join(parts)) or []


def infer(changes):
    updates = []
    for change in changes:
        print("inferring", change["path"], flush=True)
        is_new = not change["pages"]
        pages = new_pages(change) if is_new else change["pages"]

        for decision in review(pages, change):
            path = decision.documentation_path
            status = "created" if is_new and path else decision.status
            if path and decision.documentation and status in ("updated", "created"):
                updates.append(
                    {"path": path, "status": status, "text": decision.documentation}
                )
            print(f"  {status}: {path}", flush=True)
    print(f"\n{len(updates)} updated", flush=True)
    return updates
