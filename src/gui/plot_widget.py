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
        
        # Persistent Markers: List of dicts {'freq': float, 'trace': str}
        self.markers = []
        
        self.canvas.mpl_connect("pick_event", self.on_pick)
        self.canvas.mpl_connect("button_press_event", self.on_click)

    def set_data(self, dataset: SParameterDataset, config: ViewportConfig):
        """Update the plot with new data/config."""
        self.dataset = dataset
        self.config = config
        self.markers = [] # Reset markers on new file load? Or keep? Reset for safety.
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
        
        # Draw Markers
        self.draw_markers()
        
        self.figure.tight_layout()
        self.canvas.draw()

    def plot_magnitude_db(self):
        """Plot Magnitude in dB."""
        self.ax.axis('auto') # Reset aspect ratio
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
        self.ax.axis('auto') # Reset aspect ratio
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
            rf.plotting.smith(ax=self.ax, draw_labels=True)
        except Exception:
            self.ax.grid(True)
            self.ax.text(0, 0, "Smith Chart Grid Error")
            
        # Determine mask for frequency range
        mask = np.ones(len(self.dataset.frequencies), dtype=bool)
        if self.config.freq_min > 0 and self.config.freq_max > self.config.freq_min:
            mask = (self.dataset.frequencies >= self.config.freq_min) & \
                   (self.dataset.frequencies <= self.config.freq_max)

        for param in self.dataset.parameter_names:
            if self.config.visible_traces and param not in self.config.visible_traces:
                continue
            
            _, s_complex = self.dataset.get_complex_data(param)
            
            # Apply mask
            s_filtered = s_complex[mask]
            
            if len(s_filtered) > 0:
                self.ax.plot(np.real(s_filtered), np.imag(s_filtered), label=param, picker=5)
            
        self.ax.legend()
        self.ax.axis('equal')
        # Force limits to keep the chart centered and sized appropriately
        self.ax.set_xlim(-1.1, 1.1)
        self.ax.set_ylim(-1.1, 1.1)

    def draw_markers(self):
        """Draw persistent markers."""
        for marker in self.markers:
            freq = marker['freq']
            trace = marker['trace']
            
            if self.config.visible_traces and trace not in self.config.visible_traces:
                continue
                
            # Get data point
            data = self.dataset.find_nearest_data_point(trace, freq)
            
            # Determine x, y based on plot type
            if self.config.active_plot_type == PlotType.SMITH:
                x = np.real(data['complex'])
                y = np.imag(data['complex'])
                text = (f"{trace}\n"
                        f"{data['frequency']/1e9:.3f} GHz\n"
                        f"Z: {data['complex']:.3f}")
            elif self.config.active_plot_type == PlotType.MAGNITUDE_DB:
                x = data['frequency']
                y = data['magnitude_db']
                text = (f"{trace}\n"
                        f"{data['frequency']/1e9:.3f} GHz\n"
                        f"{y:.2f} dB")
            elif self.config.active_plot_type == PlotType.PHASE_DEG:
                x = data['frequency']
                y = data['phase_deg']
                text = (f"{trace}\n"
                        f"{data['frequency']/1e9:.3f} GHz\n"
                        f"{y:.2f}°")
            
            # Draw
            self.ax.plot(x, y, 'ro') # Red dot
            self.ax.annotate(text, xy=(x, y), xytext=(10, 10), textcoords="offset points",
                             bbox=dict(boxstyle="round", fc="w", alpha=0.8),
                             arrowprops=dict(arrowstyle="->"))

    def on_pick(self, event):
        """Handle click on plot to add marker."""
        if not self.dataset: 
            return
            
        line = event.artist
        # Ensure we picked a line
        if not hasattr(line, 'get_label'):
            return
            
        xdata, ydata = line.get_data()
        ind = event.ind
        
        # Take the first point clicked
        idx = ind[0]
        
        # Determine frequency based on plot type
        # For Mag/Phase, xdata is frequency.
        # For Smith, we need to lookup frequency by index.
        # Note: This assumes xdata matches dataset.frequencies[mask] or dataset.frequencies
        # Smith chart plotting uses masking.
        
        label = line.get_label()
        
        if self.config.active_plot_type == PlotType.SMITH:
             # Re-calculate mask to map index back to frequency
            mask = np.ones(len(self.dataset.frequencies), dtype=bool)
            if self.config.freq_min > 0 and self.config.freq_max > self.config.freq_min:
                mask = (self.dataset.frequencies >= self.config.freq_min) & \
                       (self.dataset.frequencies <= self.config.freq_max)
            
            # Get filtered frequencies
            filtered_freqs = self.dataset.frequencies[mask]
            if idx < len(filtered_freqs):
                freq = filtered_freqs[idx]
            else:
                return # Should not happen
        else:
            freq = xdata[idx]

        # Add marker
        self.markers.append({'freq': freq, 'trace': label})
        self.refresh_plot()

    def on_click(self, event):
        """Handle click events (Right click to clear)."""
        if event.button == 3: # Right Click
            self.markers = []
            self.refresh_plot()
