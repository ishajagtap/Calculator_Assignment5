# app/history.py
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Optional
from datetime import timezone


COLUMNS = ["timestamp", "operation", "a", "b", "result"]

class History:
    def __init__(self):
        self.df = pd.DataFrame(columns=COLUMNS)

    def append(self, operation: str, a: float, b: float, result: float):
        row = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "operation": operation,
            "a": a,
            "b": b,
            "result": result
        }
        self.df = pd.concat([self.df, pd.DataFrame([row])], ignore_index=True)

    def to_csv(self, path: str):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.df.to_csv(path, index=False)

    def load_csv(self, path: str):
        self.df = pd.read_csv(path)
        # ensure columns in expected order if present
        self.df = self.df[[c for c in COLUMNS if c in self.df.columns]]