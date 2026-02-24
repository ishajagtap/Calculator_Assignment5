# tests/test_process_command_all_branches.py
import os
from pathlib import Path
import builtins
import io
import sys
import pytest

from app.calculation import CalculatorFacade
from app.calculator_repl import process_command

def setup_env(tmp_path, monkeypatch, autosave="True"):
    hist = tmp_path / "history.csv"
    monkeypatch.setenv("HISTORY_CSV_PATH", str(hist))
    monkeypatch.setenv("AUTO_SAVE", autosave)
    return str(hist)

def test_process_command_help_and_ops_and_exit_and_clear(tmp_path, monkeypatch):
    history_path = setup_env(tmp_path, monkeypatch, autosave="False")
    calc = CalculatorFacade()

    # help
    r = process_command(calc, "help", history_path, False)
    assert "Enhanced Calculator REPL" in r["printed"]

    # basic op
    r2 = process_command(calc, "add 4 5", history_path, False)
    assert "=> 9.0" in r2["printed"]

    # history (should have one entry now)
    r3 = process_command(calc, "history", history_path, False)
    assert "operation" in r3["printed"] or "add" in r3["printed"]

    # clear
    r4 = process_command(calc, "clear", history_path, False)
    assert "Cleared history." in r4["printed"]
    # history now empty
    r5 = process_command(calc, "history", history_path, False)
    assert "No history." in r5["printed"]

    # undo/redo on fresh (should return printed booleans)
    r6 = process_command(calc, "undo", history_path, False)
    assert r6["printed"].startswith("Undo:")
    r7 = process_command(calc, "redo", history_path, False)
    assert r7["printed"].startswith("Redo:")

    # save and load (save to path, then load)
    r8 = process_command(calc, "save", history_path, False)
    assert "Saved history to" in r8["printed"]
    r9 = process_command(calc, "load", history_path, False)
    assert "Loaded history from" in r9["printed"]

    # exit with auto_save False (exit should set exit True and not crash)
    r10 = process_command(calc, "exit", history_path, False)
    assert r10["exit"] is True
    assert "Goodbye." in r10["printed"]

def test_process_command_division_by_zero_and_unknown(tmp_path, monkeypatch):
    history_path = setup_env(tmp_path, monkeypatch, autosave="False")
    calc = CalculatorFacade()

    # Division by zero
    r = process_command(calc, "div 1 0", history_path, False)
    assert "Math error:" in r["printed"] or "Math error" in r["printed"]

    # Unknown operation -> input error from calculate
    r2 = process_command(calc, "thisdoesnotexist 1 2", history_path, False)
    # process_command catches and returns 'Input error' or 'Calculation error'
    assert ("Input error" in r2["printed"]) or ("Calculation error" in r2["printed"]) or ("Unknown operation" in r2["printed"])

def test_process_command_exit_autosave_true(tmp_path, monkeypatch):
    # Ensure that when exit with AUTO_SAVE True, history file is created
    history_path = setup_env(tmp_path, monkeypatch, autosave="True")
    calc = CalculatorFacade()
    calc.calculate("add", 1, 1)  # create a history entry
    r = process_command(calc, "exit", history_path, True)
    assert r["exit"] is True
    assert Path(history_path).exists()