import hashlib
import json

from ather_os.cache.store import ResponseCache
from ather_os.dag.models import Task
from ather_os.providers.provider import TaskProvider


class CachedTaskProvider:
    """Reuse successful provider outputs for equivalent local tasks."""

    def __init__(self, provider: TaskProvider, response_cache: ResponseCache) -> None:
        self._provider = provider
        self._response_cache = response_cache

    def execute(self, task: Task) -> str:
        key = task_cache_key(task)
        cached_output = self._response_cache.get(key)
        if cached_output is not None:
            return cached_output

        output = self._provider.execute(task)
        self._response_cache.set(key, output)
        return output


def task_cache_key(task: Task) -> str:
    """Return a stable key for fields that can affect a provider response."""

    payload = {
        "context_needs": task.context_needs,
        "prompt": task.prompt,
        "quality_tier": task.quality_tier.value,
        "type": task.type.value,
    }
    encoded_payload = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded_payload.encode()).hexdigest()
