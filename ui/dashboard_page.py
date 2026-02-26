from __future__ import annotations

import pandas as pd
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox

from core.app_state import AppState
from ui.chart_widget import ChartWidget
from ui.kpi_card import KPICard


class DashboardPage(QWidget):
    def __init__(self, state: AppState):
        super().__init__()
        self.state = state

        root = QVBoxLayout(self)

        controls = QHBoxLayout()
        self.cmb_x = QComboBox()
        self.cmb_y = QComboBox()
        self.cmb_chart = QComboBox()
        self.cmb_chart.addItems(["Bar", "Line"])

        controls.addWidget(QLabel("X:"))
        controls.addWidget(self.cmb_x)
        controls.addWidget(QLabel("Y:"))
        controls.addWidget(self.cmb_y)
        controls.addWidget(self.cmb_chart)
        root.addLayout(controls)

        kpi = QHBoxLayout()
        self.kpi_rows = KPICard("Rows", 0)
        self.kpi_cols = KPICard("Columns", 0)
        kpi.addWidget(self.kpi_rows)
        kpi.addWidget(self.kpi_cols)
        root.addLayout(kpi)

        self.chart = ChartWidget()
        root.addWidget(self.chart, 1)

        self.cmb_chart.currentTextChanged.connect(self.update_chart)
        self.cmb_x.currentTextChanged.connect(self.update_chart)
        self.cmb_y.currentTextChanged.connect(self.update_chart)

    def refresh_from_state(self):
        df = self.state.df_work
        if df is None or df.empty:
            self.cmb_x.clear()
            self.cmb_y.clear()
            self.kpi_rows.update_value(0)
            self.kpi_cols.update_value(0)
            return

        cols = list(df.columns)

        self.cmb_x.blockSignals(True)
        self.cmb_y.blockSignals(True)

        self.cmb_x.clear()
        self.cmb_y.clear()
        self.cmb_x.addItems(cols)
        self.cmb_y.addItems(cols)

        self.cmb_x.blockSignals(False)
        self.cmb_y.blockSignals(False)

        self.kpi_rows.update_value(len(df))
        self.kpi_cols.update_value(len(df.columns))

        self.update_chart()

    def update_chart(self):
        df = self.state.df_work
        if df is None or df.empty:
            return

        x_col = self.cmb_x.currentText()
        y_col = self.cmb_y.currentText()
        if not x_col or not y_col:
            return

        x = df[x_col].astype(str)
        y = pd.to_numeric(df[y_col], errors="coerce").fillna(0)

        if self.cmb_chart.currentText() == "Bar":
            self.chart.plot_bar(x, y)
        else:
            self.chart.plot_line(x, y)
