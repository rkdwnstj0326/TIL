"""Automatic tests must never consume actual GMS usage."""
import pytest


@pytest.fixture(autouse=True)
def never_call_live_gms(monkeypatch):
    from src.rag.gms import GMS
    def blocked(*args, **kwargs):
        raise AssertionError('Actual GMS calls are prohibited in pytest; use explicit live validation script.')
    monkeypatch.setattr(GMS, 'json', blocked)
