from uuid import uuid4
from ather_os.dag.models import Task, TaskType, QualityTier
from ather_os.providers.llm import LLMProvider

def test_clean_response_removes_think_blocks():
    raw_output = """<think>
Here's a thinking process:
1. Understand User Request...
</think>
def execute_pipeline():
    print("Hello world")"""
    cleaned = LLMProvider._clean_response(raw_output)
    assert "<think>" not in cleaned
    assert "</think>" not in cleaned
    assert "Here's a thinking process" not in cleaned
    assert cleaned == 'def execute_pipeline():\n    print("Hello world")'

def test_clean_response_handles_unclosed_think():
    raw_output = "<think> Here is truncated internal reasoning..."
    cleaned = LLMProvider._clean_response(raw_output)
    assert cleaned == ""

def test_clean_response_handles_clean_text():
    raw_output = "Executive summary of findings.\n- Option A: Fast\n- Option B: Secure"
    cleaned = LLMProvider._clean_response(raw_output)
    assert cleaned == raw_output
