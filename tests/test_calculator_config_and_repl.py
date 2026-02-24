# tests/test_calculator_config_and_repl.py
import os
import subprocess
import sys
import json
from pathlib import Path
import tempfile

import pytest

from app import calculator_config as cfg

def test_get_history_path_creates_dir(tmp_path, monkeypatch):
    # set a nested path inside tmp_path
    target = tmp_path / "nested" / "h.csv"
    monkeypatch.setenv("HISTORY_CSV_PATH", str(target))
    path = cfg.get_history_path()
    assert str(target) == path
    # directory must exist
    assert target.parent.exists()

@pytest.mark.parametrize("val,expected", [
    ("True", True),
    ("true", True),
    ("1", True),
    ("yes", True),
    ("False", False),
    ("false", False),
    ("0", False),
    ("no", False),
])
def test_get_auto_save_variants(monkeypatch, val, expected):
    monkeypatch.setenv("AUTO_SAVE", val)
    assert cfg.get_auto_save() is expected

def test_get_auto_save_invalid(monkeypatch):
    monkeypatch.setenv("AUTO_SAVE", "notabool")
    with pytest.raises(Exception):
        cfg.get_auto_save()

def test_repl_runs_and_exits(tmp_path, monkeypatch):
    # Run the REPL as a subprocess and send 'exit\n' as input.
    # Point HISTORY_CSV_PATH to tmp_path so we don't pollute user dirs.
    history_file = tmp_path / "history.csv"
    env = os.environ.copy()
    env["HISTORY_CSV_PATH"] = str(history_file)
    env["AUTO_SAVE"] = "True"
    # call Python module
    proc = subprocess.run(
        [sys.executable, "-m", "app.calculator_repl"],
        input="exit\n",
        text=True,
        capture_output=True,
        env=env,
        timeout=5
    )
    out = proc.stdout + proc.stderr
    assert "Goodbye." in out
    # since AUTO_SAVE=True, history file should exist (even if empty)
    assert history_file.exists()