from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QLabel, QScrollArea, QLineEdit, QHBoxLayout, QMessageBox
from PyQt6.QtCore import pyqtSignal
from typing import List
from src.models.view_config import ViewportConfig

class ControlPanel(QWidget):
    """
    Panel with checkboxes to toggle trace visibility.
    """
    configChanged = pyqtSignal() # Emitted when any setting changes

    def __init__(self, config: ViewportConfig, parameter_names: List[str], parent=None):
        super().__init__(parent)
        self.config = config
        self.parameter_names = parameter_names
        
        self.layout = QVBoxLayout(self)
        
        # --- Visible Traces ---
        self.layout.addWidget(QLabel("<b>Visible Traces</b>"))
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        self.checks_layout = QVBoxLayout(content)
        
        self.checkboxes = {}
        for param in self.parameter_names:
            chk = QCheckBox(param)
            chk.setChecked(param in self.config.visible_traces)
            chk.toggled.connect(lambda checked, p=param: self.on_trace_toggled(p, checked))
            self.checks_layout.addWidget(chk)
            self.checkboxes[param] = chk
            
        self.checks_layout.addStretch()
        scroll.setWidget(content)
        self.layout.addWidget(scroll)
        
        # --- Frequency Range ---
        self.layout.addWidget(QLabel("<b>Frequency Range (Hz)</b>"))
        
        freq_layout = QVBoxLayout()
        
        # Min Freq
        h_min = QHBoxLayout()
        h_min.addWidget(QLabel("Min:"))
        self.min_input = QLineEdit(str(self.config.freq_min))
        self.min_input.editingFinished.connect(self.on_freq_changed)
        h_min.addWidget(self.min_input)
        freq_layout.addLayout(h_min)
        
        # Max Freq
        h_max = QHBoxLayout()
        h_max.addWidget(QLabel("Max:"))
        self.max_input = QLineEdit(str(self.config.freq_max))
        self.max_input.editingFinished.connect(self.on_freq_changed)
        h_max.addWidget(self.max_input)
        freq_layout.addLayout(h_max)
        
        self.layout.addLayout(freq_layout)
        self.layout.addStretch()

    def on_trace_toggled(self, param, checked):
        if checked:
            self.config.visible_traces.add(param)
        else:
            self.config.visible_traces.discard(param)
        
        self.configChanged.emit()

    def on_freq_changed(self):
        try:
            f_min = float(self.min_input.text())
            f_max = float(self.max_input.text())
            
            if f_min >= f_max:
                raise ValueError("Min frequency must be less than Max frequency.")
            
            if f_min < 0:
                raise ValueError("Frequency cannot be negative.")

            # Update config
            self.config.freq_min = f_min
            self.config.freq_max = f_max
            self.configChanged.emit()
            
        except ValueError as e:
            QMessageBox.warning(self, "Invalid Frequency", str(e))
            # Reset to current config values
            self.min_input.setText(str(self.config.freq_min))
            self.max_input.setText(str(self.config.freq_max))