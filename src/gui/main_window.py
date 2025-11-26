from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QWidget, QVBoxLayout
from PyQt6.QtGui import QAction
from src.gui.tabs import TabManager
from src.core.loader import load_touchstone_file
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("S-Parameter Viewer")
        self.resize(1000, 800)
        
        # Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # Tab Manager
        self.tabs = TabManager()
        self.layout.addWidget(self.tabs)
        
        # Menu Bar
        self.create_menu()
        
    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("&File")
        
        open_action = QAction("&Open...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file_dialog)
        file_menu.addAction(open_action)
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def open_file_dialog(self):
        file_filter = "Touchstone Files (*.s1p *.s2p *.s3p *.s4p *.snp);;All Files (*)"
        filepath, _ = QFileDialog.getOpenFileName(self, "Open Touchstone File", "", file_filter)
        
        if filepath:
            self.load_file(filepath)

    def load_file(self, filepath):
        try:
            dataset = load_touchstone_file(filepath)
            self.tabs.add_dataset(dataset)
        except Exception as e:
            QMessageBox.critical(self, "Error Loading File", str(e))
