# Enhanced Calculator Project

This repository contains a simple modular calculator application written in Python.
The codebase is designed to illustrate common design patterns such as:

- **Facade** (`CalculatorFacade`)
- **Command parsing / REPL**
- **Memento pattern** (undo/redo functionality)
- **History tracking** using `pandas`
- Modular operations with an abstract `Operation` base class

## Features

- Arithmetic operations: add, sub, mul, div, pow, root
- Command-line REPL with history, undo/redo, save/load, and configuration
- Input validation with clear errors
- History persisted to CSV
- Robust unit tests targeting 100% coverage (CI enforces ≥90%)

## Installation

```bash
# clone and create venv
git clone <repo-url>
cd Module5_Calculator_Project
python -m venv .venv
# Windows example
.\.venv\Scripts\Activate.ps1
# install the project in editable mode
pip install -e .
pip install -r requirements.txt
```

Alternatively, just install the requirements and run directly from source.

## Usage

### Running the REPL

```bash
python -m app.calculator_repl
```

Type `help` inside the REPL to see available commands, or run operations directly:

```
calc> add 2 3
=> 5.0
calc> history
... history table ...
calc> undo
Undo: True
```

### As a library

You can import and use the calculator programmatically:

```python
from app.calculation import CalculatorFacade
calc = CalculatorFacade()
result = calc.calculate('mul', 5, 7)
print(result)  # 35.0
```

## Configuration

Environment variables (set via `.env` or OS):

- `HISTORY_CSV_PATH` – path to the history CSV (default `data/history.csv`)
- `AUTO_SAVE` – boolean (`True`/`False`) whether to auto-save on exit

The helpers live in `app/calculator_config.py`.

## Testing & Coverage

Run the full test suite with coverage:

```bash
pytest --cov=app --cov-report=term-missing
```

The GitHub Actions workflow will fail if coverage drops below 90%.


## Project Structure

```
app/                # application modules
 tests/              # unit and integration tests
 data/               # default history file location
 main.py             # optional entrypoint (if present)
 pytest.ini          # pytest configuration
 requirements.txt    # dependency list
 README.md           # this file
``` 

## Contributing

Contributions are welcome!  Please fork the repo and open a pull request with tests for any new behavior.

## License

This project is provided for educational purposes.  (Add license details here if applicable.)
