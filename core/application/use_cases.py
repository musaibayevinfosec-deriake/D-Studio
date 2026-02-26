from __future__ import annotations
import pandas as pd
from core.domain.pipeline import Rule, RuleType

def apply_pipeline(df: pd.DataFrame, rules: list[Rule]) -> pd.DataFrame:
    out = df.copy()

    for r in rules:
        col = r.column
        if col not in out.columns:
            continue  # UI-də xəbərdarlıq da verə bilərik

        # Hər şeyi string kimi saxlayırıq
        s = out[col].astype(str)

        if r.rule_type == RuleType.TRIM:
            out[col] = s.str.strip()

        elif r.rule_type == RuleType.UPPERCASE:
            out[col] = s.str.upper()

        elif r.rule_type == RuleType.REPLACE:
            params = r.params or {}
            old = str(params.get("old", ""))
            new = str(params.get("new", ""))
            out[col] = s.str.replace(old, new, regex=False)

    return out
