from __future__ import annotations

import pandas as pd
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QMessageBox, QFileDialog
)
from PySide6.QtCore import Signal

from core.app_state import AppState
from core.infrastructure.csv_io import read_csv, write_csv
from core.domain.pipeline import Rule, RuleType
from core.application.use_cases import apply_pipeline

# Əgər səndə table model varsa:
from ui.table_model import PandasTableModel
from PySide6.QtWidgets import QTableView, QListWidget, QListWidgetItem, QComboBox, QLineEdit, QGroupBox, QFormLayout
from PySide6.QtCore import Qt


class CleanerPage(QWidget):
    """
    Bu page: əvvəlki cleaning/pipeline UI-nin aynısıdır.
    Sadəcə QMainWindow yox, QWidget-dir.
    """
    data_changed = Signal()  # Dashboard-a xəbər vermək üçün

    def __init__(self, state: AppState):
        super().__init__()
        self.state = state

        # əvvəlki dəyişənlərin
        self.rules: list[Rule] = []

        # ========= UI (burada əvvəlki UI-ni qururuq) =========
        root = QVBoxLayout(self)

        # Top buttons
        top = QHBoxLayout()
        self.btn_open = QPushButton("Open CSV")
        self.btn_export = QPushButton("Export CSV")
        self.btn_export.setEnabled(False)
        top.addWidget(self.btn_open)
        top.addWidget(self.btn_export)
        root.addLayout(top)

        self.lbl_info = QLabel("Load a CSV to start.")
        root.addWidget(self.lbl_info)

        # Table
        self.table = QTableView()
        self.model = PandasTableModel(pd.DataFrame())
        self.table.setModel(self.model)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        root.addWidget(self.table, 1)

        # Pipeline list
        root.addWidget(QLabel("Cleaning Pipeline"))
        self.pipeline_list = QListWidget()
        root.addWidget(self.pipeline_list, 1)

        # Pipeline buttons
        pipe_btns = QHBoxLayout()
        self.btn_remove = QPushButton("Remove Rule")
        self.btn_clear = QPushButton("Clear Pipeline")
        self.btn_apply = QPushButton("Apply Pipeline")
        self.btn_apply.setEnabled(False)
        pipe_btns.addWidget(self.btn_remove)
        pipe_btns.addWidget(self.btn_clear)
        pipe_btns.addWidget(self.btn_apply)
        root.addLayout(pipe_btns)

        # Rule builder
        box = QGroupBox("Add Rule")
        form = QFormLayout(box)

        self.cmb_rule = QComboBox()
        self.cmb_rule.addItems([rt.value for rt in RuleType])

        self.cmb_col = QComboBox()
        self.txt_old = QLineEdit()
        self.txt_new = QLineEdit()

        form.addRow("Rule Type", self.cmb_rule)
        form.addRow("Column", self.cmb_col)
        form.addRow("Replace: old", self.txt_old)
        form.addRow("Replace: new", self.txt_new)

        self.btn_add_rule = QPushButton("Add")
        self.btn_add_rule.setEnabled(False)
        form.addRow(self.btn_add_rule)

        root.addWidget(box)

        # ========= Signals =========
        self.btn_open.clicked.connect(self.open_csv)
        self.btn_export.clicked.connect(self.export_csv)
        self.btn_add_rule.clicked.connect(self.add_rule)
        self.btn_remove.clicked.connect(self.remove_rule)
        self.btn_clear.clicked.connect(self.clear_pipeline)
        self.btn_apply.clicked.connect(self.apply_rules)
        self.cmb_rule.currentTextChanged.connect(self._toggle_replace_fields)

        self._toggle_replace_fields(self.cmb_rule.currentText())

    def _toggle_replace_fields(self, rule_name: str):
        is_replace = (rule_name == RuleType.REPLACE.value)
        self.txt_old.setEnabled(is_replace)
        self.txt_new.setEnabled(is_replace)

    def open_csv(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")
        if not path:
            return

        try:
            df = read_csv(path)

            # STATE-ə yazırıq (ən vacib hissə)
            self.state.df_raw = df
            self.state.df_work = df.copy()

            # UI yenilə
            self.model.set_df(self.state.df_work)
            self.cmb_col.clear()
            self.cmb_col.addItems(list(self.state.df_work.columns))

            self.lbl_info.setText(f"Loaded: {path} | Rows: {len(df)} | Cols: {len(df.columns)}")

            self.btn_apply.setEnabled(True)
            self.btn_add_rule.setEnabled(True)
            self.btn_export.setEnabled(True)

            # Dashboard-a xəbər ver
            self.data_changed.emit()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load CSV:\n{e}")

    def add_rule(self):
        if self.state.df_work is None or self.state.df_work.empty:
            return

        rule_type = RuleType(self.cmb_rule.currentText())
        col = self.cmb_col.currentText().strip()
        if not col:
            return

        params = None
        if rule_type == RuleType.REPLACE:
            params = {"old": self.txt_old.text(), "new": self.txt_new.text()}

        r = Rule(rule_type=rule_type, column=col, params=params)
        self.rules.append(r)

        item = QListWidgetItem(r.label())
        item.setData(Qt.UserRole, r)
        self.pipeline_list.addItem(item)

    def remove_rule(self):
        row = self.pipeline_list.currentRow()
        if row < 0:
            return
        self.pipeline_list.takeItem(row)
        self.rules = [self.pipeline_list.item(i).data(Qt.UserRole) for i in range(self.pipeline_list.count())]

    def clear_pipeline(self):
        self.pipeline_list.clear()
        self.rules = []

    def apply_rules(self):
        if self.state.df_work is None or self.state.df_work.empty:
            return
        try:
            self.state.df_work = apply_pipeline(self.state.df_work, self.rules)
            self.model.set_df(self.state.df_work)

            # Dashboard-a xəbər ver (çox vacib)
            self.data_changed.emit()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Apply failed:\n{e}")

    def export_csv(self):
        if self.state.df_work is None or self.state.df_work.empty:
            return
        path, _ = QFileDialog.getSaveFileName(self, "Export CSV", "cleaned.csv", "CSV Files (*.csv)")
        if not path:
            return
        try:
            write_csv(self.state.df_work, path)
            QMessageBox.information(self, "Export", f"Saved to:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Export failed:\n{e}")
