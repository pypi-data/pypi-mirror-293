# tests/test_onwut.py

from onwut import parse_dates
from datetime import datetime

def test_parse_dates():
    assert parse_dates('2024-08') == datetime(2024, 8, 1)
    assert parse_dates('2024') == datetime(2024, 1, 1)

# 他のテストを追加できます
