from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np
from src.models.dataset import SParameterDataset
from src.models.view_config import ViewportConfig, PlotType
import skrf as rf

class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.layout.addWidget(self.canvas)
        
        self.dataset = None
        self.config = None
        
        # Default axes
        self.ax = self.figure.add_subplot(111)
        
        # Annotation
        self.annot = self.ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
        self.annot.set_visible(False)
        
        self.canvas.mpl_connect("pick_event", self.on_pick)

    def set_data(self, dataset: SParameterDataset, config: ViewportConfig):
        """Update the plot with new data/config."""
        self.dataset = dataset
        self.config = config
        self.refresh_plot()

    def refresh_plot(self):
        """Redraw the plot based on current config."""
        if not self.dataset or not self.config:
            return

        self.ax.clear()
        
        plot_type = self.config.active_plot_type
        
        if plot_type == PlotType.MAGNITUDE_DB:
            self.plot_magnitude_db()
        elif plot_type == PlotType.PHASE_DEG:
            self.plot_phase_deg()
        elif plot_type == PlotType.SMITH:
            self.plot_smith()
            
        self.canvas.draw()

    def plot_magnitude_db(self):
        """Plot Magnitude in dB."""
        self.ax.set_xlabel("Frequency (Hz)")
        self.ax.set_ylabel("Magnitude (dB)")
        self.ax.grid(True)
        
        for param in self.dataset.parameter_names:
            if self.config.visible_traces and param not in self.config.visible_traces:
                continue
                
            freq, mag = self.dataset.get_magnitude_db(param)
            # Enable picker with 5 points tolerance
            self.ax.plot(freq, mag, label=param, picker=5)
            
        self.ax.legend()
        
        if self.config.freq_min > 0 and self.config.freq_max > self.config.freq_min:
             self.ax.set_xlim(left=self.config.freq_min, right=self.config.freq_max)

    def plot_phase_deg(self):
        """Plot Phase in degrees."""
        self.ax.set_xlabel("Frequency (Hz)")
        self.ax.set_ylabel("Phase (deg)")
        self.ax.grid(True)
        
        for param in self.dataset.parameter_names:
            if self.config.visible_traces and param not in self.config.visible_traces:
                continue
            
            freq, phase = self.dataset.get_phase_deg(param)
            self.ax.plot(freq, phase, label=param, picker=5)
            
        self.ax.legend()
        
        if self.config.freq_min > 0 and self.config.freq_max > self.config.freq_min:
             self.ax.set_xlim(left=self.config.freq_min, right=self.config.freq_max)

    def plot_smith(self):
        """Plot Smith Chart."""
        try:
            rf.plotting.smith(ax=self.ax)
        except Exception:
            self.ax.grid(True)
            self.ax.text(0, 0, "Smith Chart Grid Error")

        for param in self.dataset.parameter_names:
            if self.config.visible_traces and param not in self.config.visible_traces:
                continue
            
            _, s_complex = self.dataset.get_complex_data(param)
            # Picker might need careful handling on smith chart, but basic plot supports it
            self.ax.plot(np.real(s_complex), np.imag(s_complex), label=param, picker=5)
            
        self.ax.legend()
        self.ax.axis('equal')

    def on_pick(self, event):
        """Handle click on plot."""
        if not self.dataset: 
            return
            
        line = event.artist
        xdata, ydata = line.get_data()
        ind = event.ind
        
        # Take the first point clicked
        idx = ind[0]
        x_val = xdata[idx]
        y_val = ydata[idx]
        
        # Identify parameter
        label = line.get_label()
        
        # Get precise data from dataset (optional, or just use plot data)
        # For smith chart, x/y are real/imag. For Mag/Phase, x is freq.
        
        if self.config.active_plot_type == PlotType.SMITH:
            # Show Real/Imag or Mag/Phase
            # Use dataset to get freq? Smith chart doesn't strictly map x to freq directly without index lookup
            # skrf's smith chart x/y are real/imag.
            # But we know the index `idx` in the arrays.
            freq = self.dataset.frequencies[idx]
            data = self.dataset.find_nearest_data_point(label, freq)
            text = (f"{label}\n"
                    f"Freq: {data['frequency']/1e9:.3f} GHz\n"
                    f"Mag: {data['magnitude_db']:.2f} dB\n"
                    f"Phase: {data['phase_deg']:.2f}°\n"
                    f"Z: {data['complex']:.3f}")
        else:
            # x_val is frequency
            data = self.dataset.find_nearest_data_point(label, x_val)
            text = (f"{label}\n"
                    f"Freq: {data['frequency']/1e9:.3f} GHz\n"
                    f"Mag: {data['magnitude_db']:.2f} dB\n"
                    f"Phase: {data['phase_deg']:.2f}°")
            
        self.annot.xy = (x_val, y_val)
        self.annot.set_text(text)
        self.annot.set_visible(True)
        self.canvas.draw()