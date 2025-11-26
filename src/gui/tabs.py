from PyQt6.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QButtonGroup
from src.models.dataset import SParameterDataset
from src.models.view_config import ViewportConfig, PlotType
from src.gui.plot_widget import PlotWidget
from src.gui.control_panel import ControlPanel

class FileTab(QWidget):
    """
    Represents a single open file tab.
    Contains the plot and view configuration.
    """
    def __init__(self, dataset: SParameterDataset, parent=None):
        super().__init__(parent)
        self.dataset = dataset
        self.config = ViewportConfig()
        # Initialize visible traces to all
        self.config.visible_traces = set(dataset.parameter_names)
        self.config.freq_min = dataset.frequencies[0]
        self.config.freq_max = dataset.frequencies[-1]
        
        # Main Layout (Horizontal: Plot Left, Controls Right)
        self.main_layout = QHBoxLayout(self)
        
        # Left Container (Buttons + Plot)
        self.left_container = QWidget()
        self.left_layout = QVBoxLayout(self.left_container)
        
        # Plot Type Selection
        self.type_layout = QHBoxLayout()
        self.btn_mag = QPushButton("Magnitude (dB)")
        self.btn_phase = QPushButton("Phase (deg)")
        self.btn_smith = QPushButton("Smith Chart")
        
        self.btn_mag.setCheckable(True)
        self.btn_phase.setCheckable(True)
        self.btn_smith.setCheckable(True)
        self.btn_mag.setChecked(True)
        
        self.type_group = QButtonGroup(self)
        self.type_group.addButton(self.btn_mag)
        self.type_group.addButton(self.btn_phase)
        self.type_group.addButton(self.btn_smith)
        
        self.type_layout.addWidget(self.btn_mag)
        self.type_layout.addWidget(self.btn_phase)
        self.type_layout.addWidget(self.btn_smith)
        self.type_layout.addStretch()
        
        self.left_layout.addLayout(self.type_layout)
        
        # Plot Widget
        self.plot_widget = PlotWidget()
        self.left_layout.addWidget(self.plot_widget)
        
        self.main_layout.addWidget(self.left_container, stretch=3)
        
        # Right Container (Control Panel)
        self.control_panel = ControlPanel(self.config, dataset.parameter_names)
        self.main_layout.addWidget(self.control_panel, stretch=1)
        
        # Connect signals
        self.type_group.buttonClicked.connect(self.on_type_changed)
        self.control_panel.configChanged.connect(self.plot_widget.refresh_plot)
        
        # Initial update
        self.update_plot()

    def on_type_changed(self, button):
        if button == self.btn_mag:
            self.config.active_plot_type = PlotType.MAGNITUDE_DB
        elif button == self.btn_phase:
            self.config.active_plot_type = PlotType.PHASE_DEG
        elif button == self.btn_smith:
            self.config.active_plot_type = PlotType.SMITH
        
        self.update_plot()

    def update_plot(self):
        self.plot_widget.set_data(self.dataset, self.config)


class TabManager(QTabWidget):
    """
    Manages multiple FileTabs.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)

    def add_dataset(self, dataset: SParameterDataset):
        """Create a new tab for the dataset."""
        tab = FileTab(dataset)
        self.addTab(tab, dataset.filename)
        self.setCurrentWidget(tab)

    def close_tab(self, index):
        widget = self.widget(index)
        if widget:
            widget.deleteLater()
        self.removeTab(index)
    
    def current_file_tab(self) -> FileTab:
        return self.currentWidget()