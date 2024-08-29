import pytest
from sentok.main import SenTok

def test_sentok_initialization():
    sentok = SenTok()
    assert sentok is not None
