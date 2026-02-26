from __future__ import annotations
from dataclasses import dataclass
import pandas as pd

@dataclass
class AppState:
    df_raw: pd.DataFrame | None = None
    df_work: pd.DataFrame | None = None
