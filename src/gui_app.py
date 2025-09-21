import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QCheckBox, QTextEdit, QGridLayout, QScrollArea, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QTextCursor
from model_utils import SYMPTOMS, predict_from_symptoms

class StylishDiagnosisApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🩺 AI Medical Diagnosis Assistant")
        self.resize(800, 600)
        self.symptom_checkboxes = {}
        self.init_ui()

    def init_ui(self):
        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header = QLabel("🩺 AI Medical Diagnosis Assistant (Demo)")
        header.setFont(QFont("Arial", 20, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("color: #2E4053;")
        layout.addWidget(header)

        # Info label
        info = QLabel("Select your symptoms and click Predict. <b>Educational demo only.</b>")
        info.setAlignment(Qt.AlignCenter)
        info.setStyleSheet("color: #34495E; font-size: 13px;")
        layout.addWidget(info)

        # Symptom checkboxes (scrollable)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QFrame()
        scroll_widget.setStyleSheet("background-color: #F8F9F9; border-radius: 10px;")
        grid = QGridLayout()
        grid.setSpacing(10)
        for i, symptom in enumerate(SYMPTOMS):
            cb = QCheckBox(symptom.replace("_", " ").capitalize())
            cb.setStyleSheet("font-size: 12px; padding:5px;")
            self.symptom_checkboxes[symptom] = cb
            grid.addWidget(cb, i // 3, i % 3)
        scroll_widget.setLayout(grid)
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll, stretch=1)

        # Buttons layout
        btn_layout = QHBoxLayout()
        predict_btn = QPushButton("Predict 🩺")
        predict_btn.setStyleSheet(
            "background-color: #27AE60; color: white; font-weight:bold; padding:10px; border-radius:8px;"
            "font-size:14px;"
        )
        predict_btn.clicked.connect(self.on_predict)

        clear_btn = QPushButton("Clear ✖")
        clear_btn.setStyleSheet(
            "background-color: #C0392B; color: white; font-weight:bold; padding:10px; border-radius:8px;"
            "font-size:14px;"
        )
        clear_btn.clicked.connect(self.on_clear)

        btn_layout.addWidget(predict_btn)
        btn_layout.addWidget(clear_btn)
        layout.addLayout(btn_layout)

        # Result area
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.result_area.setStyleSheet(
            "background-color: #FEF9E7; border:1px solid #F7DC6F; border-radius:10px; font-size:13px;"
        )
        layout.addWidget(QLabel("<b>Prediction Result</b>"))
        layout.addWidget(self.result_area, stretch=1)

        # Disclaimer
        footer = QLabel("Disclaimer: Educational demo only. Consult a doctor for medical advice.")
        footer.setStyleSheet("color: gray; font-size: 11px; font-style: italic;")
        footer.setAlignment(Qt.AlignRight)
        layout.addWidget(footer)

        # Apply main layout
        self.setLayout(layout)
        self.setStyleSheet("background-color: #ECF0F1;")

    def on_predict(self):
        symptom_dict = {s: int(cb.isChecked()) for s, cb in self.symptom_checkboxes.items()}
        if sum(symptom_dict.values()) == 0:
            self.result_area.setHtml("<span style='color:red;'><b>Please select at least one symptom!</b></span>")
            return

        preds = predict_from_symptoms(symptom_dict, top_k=3)
        text = "<h3>Top Predictions:</h3><ol>"
        for disease, prob in preds:
            text += f"<li><b>{disease}</b> — probability: {prob*100:.1f}%</li>"
        text += "</ol>"
        self.result_area.setHtml(text)
        self.result_area.moveCursor(QTextCursor.Start)

    def on_clear(self):
        for cb in self.symptom_checkboxes.values():
            cb.setChecked(False)
        self.result_area.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StylishDiagnosisApp()
    window.show()
    sys.exit(app.exec_())
