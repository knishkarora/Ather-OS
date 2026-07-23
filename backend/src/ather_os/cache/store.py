from typing import Protocol


class ResponseCache(Protocol):
    """Store provider outputs by a deterministic task cache key."""

    def get(self, key: str) -> str | None:
        """Return a cached output, if one exists."""

    def set(self, key: str, output: str) -> None:
        """Store an output for later equivalent task execution."""


class InMemoryResponseCache:
    """Minimal process-local response cache for local provider execution."""

    def __init__(self) -> None:
        self._outputs: dict[str, str] = {}

    def get(self, key: str) -> str | None:
        return self._outputs.get(key)

    def set(self, key: str, output: str) -> None:
        self._outputs[key] = output
