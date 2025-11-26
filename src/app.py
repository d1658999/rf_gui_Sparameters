import sys
import os

# Add project root to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PyQt6.QtWidgets import QApplication
from src.gui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("S-Parameter Viewer")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
