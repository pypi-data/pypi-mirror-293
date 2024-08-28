from typing import TYPE_CHECKING, Any

from langchain._api import create_importer

if TYPE_CHECKING:
    from langchain_community.chat_models.anthropic import (
        ChatAnthropic,
        convert_messages_to_prompt_anthropic,
    )

# Create a way to dynamically look up deprecated imports.
# Used to consolidate logic for raising deprecation warnings and
# handling optional imports.
DEPRECATED_LOOKUP = {
    "convert_messages_to_prompt_anthropic": "langchain_community.chat_models.anthropic",
    "ChatAnthropic": "langchain_community.chat_models.anthropic",
}

_import_attribute = create_importer(__package__, deprecated_lookups=DEPRECATED_LOOKUP)


def __getattr__(name: str) -> Any:
    """Look up attributes dynamically."""
    return _import_attribute(name)


__all__ = [
    "convert_messages_to_prompt_anthropic",
    "ChatAnthropic",
]
