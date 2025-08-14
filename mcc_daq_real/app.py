import sys
import os
import time
from typing import List, Tuple
from collections import deque
import numpy as np

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox, QSpinBox, QMessageBox
)
from PySide6.QtCore import Qt, QTimer

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from ul_wrapper import get_board_names, ain_volts, is_available, BIP10VOLTS, BIP5VOLTS, BIP2VOLTS, BIP1VOLTS
from ul_scan_wrapper import AInScanManager

RANGE_OPTIONS = [
    ("±10V", BIP10VOLTS),
    ("±5V", BIP5VOLTS),
    ("±2V", BIP2VOLTS),
    ("±1V", BIP1VOLTS),
]

class MCCRealTest(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MCC DAQ - Test Réel (ctypes cbw64)")
        self.resize(900, 600)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.x = []
        self.y = []
        self.t0 = None
        self.buffer_seconds = 1
        self.scan_manager = AInScanManager()

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Controls
        ctl = QHBoxLayout()
        layout.addLayout(ctl)

        self.detect_btn = QPushButton("🔍 Détecter les Cartes")
        self.detect_btn.clicked.connect(self.detect_boards)
        ctl.addWidget(self.detect_btn)

        # LEDs état détection: rouge (par défaut), vert (si détectée)
        self.led_red = QLabel()
        self.led_green = QLabel()
        for led in (self.led_red, self.led_green):
            led.setFixedSize(18, 18)
        self._set_led(self.led_red, True)
        self._set_led(self.led_green, False)
        ctl.addWidget(QLabel("État:"))
        ctl.addWidget(self.led_red)
        ctl.addWidget(self.led_green)

        ctl.addWidget(QLabel("Carte:"))
        self.board_combo = QComboBox()
        ctl.addWidget(self.board_combo)

        ctl.addWidget(QLabel("Canal:"))
        self.chan_spin = QSpinBox()
        self.chan_spin.setRange(0, 15)
        self.chan_spin.valueChanged.connect(self._on_channel_changed)
        ctl.addWidget(self.chan_spin)

        ctl.addWidget(QLabel("Plage:"))
        self.range_combo = QComboBox()
        for text, val in RANGE_OPTIONS:
            self.range_combo.addItem(text, userData=val)
        ctl.addWidget(self.range_combo)

        ctl.addWidget(QLabel("Fréquence (Hz):"))
        self.freq_spin = QSpinBox()
        self.freq_spin.setRange(10, 10000)
        self.freq_spin.setValue(1000)
        ctl.addWidget(self.freq_spin)

        ctl.addWidget(QLabel("Durée buffer (s):"))
        self.buf_spin = QSpinBox()
        self.buf_spin.setRange(1, 3)
        self.buf_spin.setValue(1)
        self.buf_spin.valueChanged.connect(self._on_buffer_changed)
        ctl.addWidget(self.buf_spin)

        self.start_btn = QPushButton("▶️ Démarrer")
        self.start_btn.clicked.connect(self.start_sampling)
        ctl.addWidget(self.start_btn)

        self.stop_btn = QPushButton("⏹️ Stop")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_sampling)
        ctl.addWidget(self.stop_btn)

        # SPS label
        ctl.addWidget(QLabel("SPS:"))
        self.rate_label = QLabel("0")
        ctl.addWidget(self.rate_label)

        ctl.addStretch(1)

        # Plot (Matplotlib)
        self.fig = Figure(figsize=(5, 3), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Voltage (V)')
        self.ax.grid(True, alpha=0.3)
        (self.line,) = self.ax.plot([], [], color=(0/255, 150/255, 255/255), linewidth=2)
        layout.addWidget(self.canvas, 1)
        # Toolbar for zoom/pan
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)

        # Init
        if not is_available():
            QMessageBox.warning(self, "DLL manquante", "cbw64.dll indisponible. Installez Measurement Computing InstaCal/UL et relancez.")
        self.detect_boards()

    def detect_boards(self):
        self.board_combo.clear()
        try:
            names: List[Tuple[int, str]] = get_board_names()
        except Exception as e:
            QMessageBox.critical(self, "Erreur détection", f"{e}")
            return
        if not names:
            self.board_combo.addItem("Aucune carte (InstaCal)", userData=None)
            self._update_detect_led(False)
            self.start_btn.setEnabled(False)
            return
        for bnum, name in names:
            self.board_combo.addItem(f"{bnum}: {name}", userData=bnum)
        # Validation réelle: tentative de lecture sur le canal 0
        ok = self._probe_selected_board()
        self._update_detect_led(ok)
        self.start_btn.setEnabled(ok)

    def start_sampling(self):
        bnum = self.board_combo.currentData()
        if bnum is None:
            QMessageBox.information(self, "Aucune carte", "Aucune carte n'est sélectionnée.")
            return
        # Try hardware scan first, fallback to timer-based sampling
        freq = int(self.freq_spin.value())
        chan = int(self.chan_spin.value())
        rng = int(self.range_combo.currentData())
        
        self.use_scan = False
        try:
            buffer_size = max(1000, freq * self.buffer_seconds)
            success = self.scan_manager.start_scan(bnum, chan, rng, freq, buffer_size)
            if success:
                self.use_scan = True
                print(f"Using hardware AInScan at {self.scan_manager.get_actual_rate()} Hz")
        except Exception as e:
            print(f"AInScan failed ({e}), falling back to timer-based sampling")
            self.use_scan = False
            
        self.x.clear(); self.y.clear()
        self.t0 = time.time()
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        
        # reset plot view
        self.ax.cla()
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Voltage (V)')
        self.ax.grid(True, alpha=0.3)
        (self.line,) = self.ax.plot([], [], color=(0/255, 150/255, 255/255), linewidth=2)
        
        if self.use_scan:
            # Hardware scan mode: fast GUI updates
            self.timer.start(50)  # 20 FPS
        else:
            # Timer-based mode: sample at requested frequency
            period_ms = max(1, int(1000 / freq))
            self.timer.start(period_ms)

    def stop_sampling(self):
        self.timer.stop()
        self.scan_manager.stop_scan()
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

    def update_plot(self):
        """Update plot with latest data (scan or timer-based)."""
        try:
            if hasattr(self, 'use_scan') and self.use_scan:
                # Hardware scan mode
                freq = self.scan_manager.get_actual_rate()
                max_points = max(100, int(freq * self.buffer_seconds))
                voltages, num_points = self.scan_manager.get_data(max_points)
                
                if num_points == 0:
                    return
                    
                # Generate time array
                dt = 1.0 / freq
                t_end = time.time() - self.t0
                t_start = t_end - (num_points - 1) * dt
                times = np.linspace(t_start, t_end, num_points)
                
                # Update rolling buffer
                self.x.extend(times)
                self.y.extend(voltages)
                
                # Keep only buffer window
                max_buffer_points = max(1000, int(freq * self.buffer_seconds * 1.2))
                if len(self.x) > max_buffer_points:
                    excess = len(self.x) - max_buffer_points
                    self.x = self.x[excess:]
                    self.y = self.y[excess:]
                    
                actual_rate = freq
            else:
                # Timer-based mode: single point sampling
                bnum = self.board_combo.currentData()
                if bnum is None:
                    return
                chan = int(self.chan_spin.value())
                rng = int(self.range_combo.currentData())
                
                v = ain_volts(bnum, chan=chan, rng=rng)
                t = time.time() - self.t0
                
                self.x.append(t)
                self.y.append(v)
                
                # Keep only buffer window
                freq = int(self.freq_spin.value())
                max_buffer_points = max(100, int(freq * self.buffer_seconds * 1.2))
                if len(self.x) > max_buffer_points:
                    excess = len(self.x) - max_buffer_points
                    self.x = self.x[excess:]
                    self.y = self.y[excess:]
                    
                # Calculate actual rate from timestamps
                if len(self.x) >= 2:
                    dt_avg = (self.x[-1] - self.x[0]) / (len(self.x) - 1)
                    actual_rate = int(1.0 / dt_avg) if dt_avg > 0 else 0
                else:
                    actual_rate = 0
                
        except Exception as e:
            # Error reading data
            self._update_detect_led(False)
            self.stop_sampling()
            QMessageBox.critical(self, "Erreur acquisition", f"{e}")
            return
            
        # Update matplotlib line
        self.line.set_data(self.x, self.y)
        
        # X limits: rolling window
        xmin = 0 if not self.x else max(0.0, self.x[-1] - self.buffer_seconds)
        xmax = max(self.buffer_seconds, self.x[-1] if self.x else self.buffer_seconds)
        self.ax.set_xlim(xmin, xmax)
        
        # Y limits with margin
        if self.y:
            ymin = min(self.y)
            ymax = max(self.y)
            if ymin == ymax:
                ymin -= 0.1
                ymax += 0.1
            pad = max(0.05 * (ymax - ymin), 0.02)
            self.ax.set_ylim(ymin - pad, ymax + pad)
            
        # Update SPS display
        self.rate_label.setText(str(actual_rate))
            
        self.canvas.draw_idle()

    def _on_buffer_changed(self, val: int):
        self.buffer_seconds = int(val)

    def _probe_selected_board(self) -> bool:
        """Fait une lecture rapide pour vérifier la présence réelle de la carte."""
        bnum = self.board_combo.currentData()
        if bnum is None:
            return False
        try:
            _ = ain_volts(int(bnum), chan=0, rng=self.range_combo.currentData() or 1)
            return True
        except Exception:
            return False

    def _on_channel_changed(self, _):
        # clear buffers and re-probe presence to avoid cross-channel artifacts
        was_running = self.timer.isActive()
        if was_running:
            self.stop_sampling()
        self.x.clear(); self.y.clear()
        self.line.set_data([], [])
        self.canvas.draw_idle()
        ok = self._probe_selected_board()
        self._update_detect_led(ok)
        self.start_btn.setEnabled(ok)
        if was_running and ok:
            self.start_sampling()

    def _set_led(self, widget: QLabel, on: bool, color_on: str = "#00c853", color_off: str = "#8e8e8e"):
        # Round LED using stylesheet
        color = color_on if on else color_off
        widget.setStyleSheet(
            f"background-color: {color}; border: 1px solid #444; border-radius: 9px;"
        )

    def _update_detect_led(self, detected: bool):
        # red ON when not detected, green ON when detected
        self._set_led(self.led_red, not detected, color_on="#ff1744")
        self._set_led(self.led_green, detected, color_on="#00e676")


def main():
    app = QApplication(sys.argv)
    win = MCCRealTest()
    win.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
