from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QFormLayout, QLineEdit, QPushButton,
    QComboBox, QSpinBox, QCheckBox, QHBoxLayout, QApplication, QScrollArea, QMessageBox,
    QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
import sys
import numpy as np
import random
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import json

MAX_SONDES = 16 # Défini globalement


def set_light_mode_and_style(app):
    palette = QPalette()
    window_bg = QColor(255, 255, 255)
    text_color_palette = QColor(0, 0, 0)
    base_bg = QColor(240, 240, 240)
    button_bg = QColor(200, 200, 200)
    highlight_color = QColor(0, 120, 215)

    palette.setColor(QPalette.Window, window_bg)
    palette.setColor(QPalette.WindowText, text_color_palette)
    palette.setColor(QPalette.Base, base_bg)
    palette.setColor(QPalette.AlternateBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
    palette.setColor(QPalette.Text, text_color_palette)
    palette.setColor(QPalette.Button, button_bg)
    palette.setColor(QPalette.ButtonText, text_color_palette)
    app.setPalette(palette)

    app.setStyleSheet('''
        QWidget {
            font-family: 'Segoe UI', 'Arial', sans-serif;
            font-size: 13px;
            color: #000; 
        }
        QLabel#titleLabel {
            font-size: 20px;
            font-weight: bold;
            color: #00bfff; 
            letter-spacing: 2px;
            padding-bottom: 5px;
        }
        QLineEdit, QComboBox, QSpinBox, QTableWidget { 
            background-color: #f0f0f0; 
            border: 1px solid #aaa;
            border-radius: 6px;
            padding: 5px 8px;
            color: #000; 
        }
        QComboBox::drop-down { border: none; }
        QTableWidget { gridline-color: #aaa; }
        QHeaderView::section {
            background-color: #e0e0e0; 
            color: #00bfff; 
            font-weight: bold;
            padding: 4px;
            border: 1px solid #aaa;
        }
        QPushButton {
            background: #00bfff;
            color: white; 
            border-radius: 8px;
            padding: 8px 18px;
            font-weight: bold;
            font-size: 14px;
        }
        QPushButton:hover {
            background: #005fa3;
        }
        QPushButton:disabled {
            background-color: #aaa;
            color: #777;
        }
        QCheckBox { color: #000; }
        QCheckBox::indicator { 
            width: 16px; height: 16px;
            border: 1px solid #aaa; border-radius: 3px;
        }
        QCheckBox::indicator:checked {
            background-color: #00bfff; border: 1px solid #00bfff;
        }
        QScrollArea { border: 1px solid #aaa; background-color: #f0f0f0; }
        QTabWidget::pane {
            border: 1px solid #aaa; border-top: none;
        }
        QTabBar::tab {
            background: #e0e0e0; color: #000;
            padding: 8px 15px; border: 1px solid #aaa;
            border-bottom: none; 
            border-top-left-radius: 6px; border-top-right-radius: 6px;
        }
        QTabBar::tab:selected {
            background: #3c3c44; color: #00bfff; 
            border-bottom: 1px solid #3c3c44; 
        }
        QTabBar::tab:!selected:hover { background: #ccc; }
    ''')

# --- Fonctions Utilitaires et Classes (inchangées) ---
def set_dark_mode_and_style(app): # Renommé pour plus de clarté
    palette = QPalette()
    window_bg = QColor(30, 30, 36)
    text_color_palette = QColor(220, 220, 220) 
    base_bg = QColor(24, 24, 28)
    button_bg = QColor(40, 40, 48)
    highlight_color = QColor(0, 120, 215)
    
    palette.setColor(QPalette.Window, window_bg)
    palette.setColor(QPalette.WindowText, text_color_palette)
    palette.setColor(QPalette.Base, base_bg) 
    palette.setColor(QPalette.AlternateBase, QColor(36, 36, 42))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(20, 20, 20)) 
    palette.setColor(QPalette.Text, text_color_palette) 
    palette.setColor(QPalette.Button, button_bg)
    palette.setColor(QPalette.ButtonText, text_color_palette)
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Highlight, highlight_color)
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)

    app.setStyleSheet('''
        QWidget {
            font-family: 'Segoe UI', 'Arial', sans-serif;
            font-size: 13px;
            color: #e0e0e0; 
        }
        QLabel#titleLabel {
            font-size: 20px;
            font-weight: bold;
            color: #00bfff; 
            letter-spacing: 2px;
            padding-bottom: 5px;
        }
        QLineEdit, QComboBox, QSpinBox, QTableWidget { 
            background-color: #23232b; 
            border: 1px solid #444;
            border-radius: 6px;
            padding: 5px 8px;
            color: #e0e0e0; 
        }
        QComboBox::drop-down { border: none; }
        QComboBox::down-arrow { image: url(no_arrow.png); /* Consider placeholder or actual icon */ }
        QTableWidget { gridline-color: #444; }
        QHeaderView::section {
            background-color: #2c2c34; 
            color: #00bfff; 
            font-weight: bold;
            padding: 4px;
            border: 1px solid #444;
        }
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00bfff, stop:1 #005fa3);
            color: white; 
            border-radius: 8px;
            padding: 8px 18px;
            font-weight: bold;
            font-size: 14px;
        }
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #005fa3, stop:1 #00bfff);
        }
        QPushButton:disabled {
            background-color: #35353f;
            color: #777;
        }
        QCheckBox { color: #e0e0e0; }
        QCheckBox::indicator { 
            width: 16px; height: 16px;
            border: 1px solid #555; border-radius: 3px;
        }
        QCheckBox::indicator:checked {
            background-color: #00bfff; border: 1px solid #00bfff;
        }
        QScrollArea { border: 1px solid #444; background-color: #1e1e24; }
        QTabWidget::pane {
            border: 1px solid #444; border-top: none;
        }
        QTabBar::tab {
            background: #2c2c34; color: #e0e0e0;
            padding: 8px 15px; border: 1px solid #444;
            border-bottom: none; 
            border-top-left-radius: 6px; border-top-right-radius: 6px;
        }
        QTabBar::tab:selected {
            background: #3c3c44; color: #00bfff; 
            border-bottom: 1px solid #3c3c44; 
        }
        QTabBar::tab:!selected:hover { background: #35353f; }
    ''')

def lecture_tension_sonde(sonde_idx): # Simulation
    return round(random.uniform(-2.5, 2.5), 3)

class CalibrationGraph(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure(figsize=(5, 3), dpi=100)
        fig.patch.set_facecolor('#1e1e24') 
        self.axes = fig.add_subplot(111)
        self._apply_axes_style()
        super().__init__(fig)
        self.setParent(parent)

    def _apply_axes_style(self):
        self.axes.set_facecolor('#23232b') 
        self.axes.tick_params(axis='x', colors='#e0e0e0')
        self.axes.tick_params(axis='y', colors='#e0e0e0')
        self.axes.xaxis.label.set_color('#e0e0e0')
        self.axes.yaxis.label.set_color('#e0e0e0')
        self.axes.title.set_color('#00bfff')
        for spine in self.axes.spines.values():
            spine.set_edgecolor('#555')

    def plot(self, x_data, y_data, slope, intercept, r2):
        self.axes.clear()
        self._apply_axes_style() # Re-apply styles after clear

        if len(x_data) > 0 and len(y_data) > 0 :
            self.axes.scatter(x_data, y_data, color='#00bfff', label='Points de mesure')
            if len(x_data) > 1 : # Need at least 2 points for a line
                line_x_plot = np.array([min(x_data), max(x_data)])
            else: # Single point, just plot the point
                line_x_plot = np.array(x_data)
            line_y_plot = slope * line_x_plot + intercept
            self.axes.plot(line_x_plot, line_y_plot, color='#ff8800', label='Régression linéaire')
        
        self.axes.set_xlabel('Hauteur (unité)')
        self.axes.set_ylabel('Tension (V)')
        self.axes.set_title(f'Calibration (R²={r2:.4f})')
        if len(x_data) > 0:
            legend = self.axes.legend()
            for text in legend.get_texts():
                text.set_color("#e0e0e0")
            legend.get_frame().set_facecolor('#2c2c34')
            legend.get_frame().set_edgecolor('#444')
        self.draw()

    def clear_plot(self, title="Entrez des points pour la calibration"):
        self.axes.clear()
        self._apply_axes_style()
        self.axes.set_title(title)
        self.axes.set_xlabel('Hauteur (unité)')
        self.axes.set_ylabel('Tension (V)')
        self.draw()

# --- Fenêtre de Sélection des Sondes ---
def show_sonde_selection_config_window():
    # Gère la création de QApplication si c'est la première fenêtre
    created_app_here = not QApplication.instance()
    app = QApplication.instance() or QApplication(sys.argv)
    
    if created_app_here: # Appliquer le style uniquement si l'app vient d'être créée ici
        set_dark_mode_and_style(app)
    
    selection_window = QWidget()
    selection_window.setWindowTitle("Configuration des Sondes - HRNeoWave")
    selection_window.setMinimumWidth(500)
    main_v_layout = QVBoxLayout(selection_window)

    title_lbl = QLabel("Configuration et Sélection des Sondes")
    title_lbl.setObjectName("titleLabel")
    title_lbl.setAlignment(Qt.AlignCenter)
    main_v_layout.addWidget(title_lbl)

    subtitle_lbl = QLabel("<i>Choisissez le nombre de sondes actives et sélectionnez celles à calibrer.</i>")
    subtitle_lbl.setAlignment(Qt.AlignCenter)
    main_v_layout.addWidget(subtitle_lbl)
    main_v_layout.addSpacing(20)

    num_sondes_layout = QHBoxLayout()
    num_sondes_label = QLabel("Nombre total de sondes actives pour cet essai :")
    num_sondes_spinbox = QSpinBox()
    num_sondes_spinbox.setRange(1, MAX_SONDES)
    num_sondes_spinbox.setValue(3) # Valeur par défaut
    num_sondes_layout.addWidget(num_sondes_label)
    num_sondes_layout.addWidget(num_sondes_spinbox)
    num_sondes_layout.addStretch()
    main_v_layout.addLayout(num_sondes_layout)
    main_v_layout.addSpacing(10)

    selection_label = QLabel("Cochez les sondes que vous souhaitez calibrer maintenant :")
    main_v_layout.addWidget(selection_label)

    sondes_checkboxes_list = []
    # Utiliser un QScrollArea pour gérer un grand nombre de sondes
    checkbox_scroll_area = QScrollArea()
    checkbox_scroll_area.setWidgetResizable(True)
    checkbox_container = QWidget()
    checkbox_grid_layout = QVBoxLayout(checkbox_container) # QVBoxLayout pour une liste verticale

    for i in range(MAX_SONDES):
        cb = QCheckBox(f"Sonde {i+1}")
        sondes_checkboxes_list.append(cb)
        checkbox_grid_layout.addWidget(cb)
    
    checkbox_scroll_area.setWidget(checkbox_container)
    checkbox_scroll_area.setMinimumHeight(150) # Hauteur fixe pour le scroll area
    main_v_layout.addWidget(checkbox_scroll_area)
    main_v_layout.addSpacing(20)
    
    def update_active_sondes_and_checkboxes():
        active_count = num_sondes_spinbox.value()
        for i, cb_widget in enumerate(sondes_checkboxes_list):
            is_active_for_essai = (i < active_count)
            cb_widget.setEnabled(is_active_for_essai)
            if not is_active_for_essai: # Désactiver et décocher si pas active pour l'essai
                cb_widget.setChecked(False)
            # Optionnel: cocher par défaut celles qui sont actives pour l'essai
            # elif is_active_for_essai and not cb_widget.isChecked():
            #     cb_widget.setChecked(True)

    num_sondes_spinbox.valueChanged.connect(update_active_sondes_and_checkboxes)
    update_active_sondes_and_checkboxes() # Appel initial

    proceed_button = QPushButton("Passer à la Calibration Individuelle")
    proceed_button.setMinimumHeight(40)
    
    def on_proceed_button_clicked():
        selected_indices = [i for i, cb in enumerate(sondes_checkboxes_list) if cb.isChecked() and cb.isEnabled()]
        if not selected_indices:
            QMessageBox.warning(selection_window, "Aucune Sonde Sélectionnée",
                                "Veuillez cocher au moins une sonde active pour la calibration.")
            return
        
        selection_window.close() # Ferme la fenêtre actuelle
        show_individual_calibration_window(selected_indices) # Ouvre la fenêtre suivante

    proceed_button.clicked.connect(on_proceed_button_clicked)
    main_v_layout.addWidget(proceed_button, alignment=Qt.AlignCenter)

    selection_window.show()

    if created_app_here:
        sys.exit(app.exec_())
    # Si appelée depuis une autre fenêtre, ne pas appeler sys.exit() ici

# --- Fenêtre de Calibration Individuelle (adaptée) ---
def show_individual_calibration_window(selected_sondes_indices):
    # QApplication doit déjà exister si cette fenêtre est appelée après la sélection
    app = QApplication.instance() 
    if not app: # Sécurité: si appelée directement pour test, créer une app
        created_app_here_for_individual = True
        app = QApplication(sys.argv)
        set_dark_mode_and_style(app)
    else:
        created_app_here_for_individual = False

    calib_window = QWidget()
    calib_window.setWindowTitle("Calibration individuelle des sondes - HRNeoWave")
    calib_window.setMinimumSize(750, 700) 
    
    main_v_layout_calib = QVBoxLayout(calib_window)

    title_lbl_calib = QLabel("Calibration Individuelle des Sondes")
    title_lbl_calib.setObjectName("titleLabel")
    title_lbl_calib.setAlignment(Qt.AlignCenter)
    main_v_layout_calib.addWidget(title_lbl_calib)

    subtitle_lbl_calib = QLabel(f"<i>Calibration pour les sondes : {', '.join([str(i+1) for i in selected_sondes_indices])}</i>")
    subtitle_lbl_calib.setAlignment(Qt.AlignCenter)
    main_v_layout_calib.addWidget(subtitle_lbl_calib)
    main_v_layout_calib.addSpacing(15)

    # Ajout stockage des résultats et suivi validation
    calibration_results = {}
    validated_sondes = set()

    tabs_widget = QTabWidget()
    sonde_calibration_data_widgets = {} 

    for sonde_original_idx in selected_sondes_indices:
        tab_content_widget = QWidget()
        tab_v_layout = QVBoxLayout(tab_content_widget)

        points_control_layout = QHBoxLayout()
        points_label = QLabel("Nombre de points de calibration :")
        points_combo = QComboBox()
        points_combo.addItems(["3", "4", "5", "6", "7"]) 
        points_combo.setCurrentText("3") 
        points_control_layout.addWidget(points_label)
        points_control_layout.addWidget(points_combo)
        points_control_layout.addStretch()
        tab_v_layout.addLayout(points_control_layout)

        calibration_table = QTableWidget()
        calibration_table.setColumnCount(3)
        calibration_table.setHorizontalHeaderLabels(["Hauteur (m)", "Tension (V)", "Acquisition Auto"])
        calibration_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        calibration_table.verticalHeader().setVisible(False)
        calibration_table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked)
        calibration_table.setMinimumHeight(140)  # Agrandir la zone du tableau
        calibration_table.setStyleSheet("QTableWidget { font-size: 11px; padding: 9px; }")

        bottom_section_layout = QHBoxLayout()
        graph_widget = CalibrationGraph()
        
        results_group_layout = QVBoxLayout()
        result_info_label = QLabel("Résultats de la calibration:")
        result_info_label.setStyleSheet("font-weight:bold; color:#00bfff;")
        calibration_result_display_label = QLabel("<i>Entrez les points pour calculer.</i>")
        calibration_result_display_label.setWordWrap(True)
        calibration_result_display_label.setAlignment(Qt.AlignTop)
        results_group_layout.addWidget(result_info_label)
        results_group_layout.addWidget(calibration_result_display_label)
        results_group_layout.addStretch()

        bottom_section_layout.addWidget(graph_widget, 2) 
        bottom_section_layout.addLayout(results_group_layout, 1) 

        pre_calibration_checks_layout = QHBoxLayout()
        cb_sonde_nettoyee = QCheckBox("Sonde nettoyée")
        cb_parallele_verif = QCheckBox("Parallélisme vérifié")
        cb_visuelle_inspection = QCheckBox("Inspection visuelle OK")
        cb_cable_compensation = QCheckBox("Compensation des câbles")
        pre_calibration_checks_layout.addWidget(cb_sonde_nettoyee)
        pre_calibration_checks_layout.addWidget(cb_parallele_verif)
        pre_calibration_checks_layout.addWidget(cb_visuelle_inspection)
        pre_calibration_checks_layout.addWidget(cb_cable_compensation)

        buttons_layout = QHBoxLayout()
        recalculate_button = QPushButton("Recalculer & Afficher Graphe")
        validate_sonde_button = QPushButton(f"Valider Calibration Sonde {sonde_original_idx+1}")
        buttons_layout.addStretch()
        buttons_layout.addWidget(recalculate_button)
        buttons_layout.addWidget(validate_sonde_button)

        tab_v_layout.addWidget(calibration_table)
        tab_v_layout.addLayout(bottom_section_layout)
        tab_v_layout.addSpacing(10)
        tab_v_layout.addLayout(pre_calibration_checks_layout)
        tab_v_layout.addSpacing(10)
        tab_v_layout.addLayout(buttons_layout)

        tabs_widget.addTab(tab_content_widget, f"Sonde {sonde_original_idx+1}")
        
        sonde_calibration_data_widgets[sonde_original_idx] = {
            "points_combo": points_combo,
            "table": calibration_table,
            "graph": graph_widget,
            "result_label": calibration_result_display_label,
            "cb_nettoyee": cb_sonde_nettoyee,
            "cb_parallele": cb_parallele_verif,
            "cb_visuelle": cb_visuelle_inspection,
            "cb_cable": cb_cable_compensation,
            "recalculate_btn": recalculate_button,
            "validate_btn": validate_sonde_button
        }

        def _update_table_rows_local(num_rows, current_table, current_sonde_idx_for_btn):
            current_table.setRowCount(num_rows)
            for r_idx_table in range(num_rows):
                current_table.setRowHeight(r_idx_table, 28)  # Hauteur de ligne plus grande
                if not current_table.cellWidget(r_idx_table, 2):
                    read_tension_button = QPushButton("Lire Tension")
                    read_tension_button.clicked.connect(
                        lambda checked=False, row_idx_btn=r_idx_table, tbl_btn=current_table, s_idx_btn_local=current_sonde_idx_for_btn: 
                            _read_and_set_tension_local(row_idx_btn, tbl_btn, s_idx_btn_local)
                    )
                    current_table.setCellWidget(r_idx_table, 2, read_tension_button)

        def _read_and_set_tension_local(row_index, target_table, s_idx_read_local):
            tension_value = lecture_tension_sonde(s_idx_read_local)
            item = QTableWidgetItem(str(tension_value))
            item.setTextAlignment(Qt.AlignCenter)
            target_table.setItem(row_index, 1, item)

        def _trigger_recalculation_local(s_idx_recalc_local):
            widgets = sonde_calibration_data_widgets[s_idx_recalc_local]
            current_table = widgets["table"]
            num_calibration_points = int(widgets["points_combo"].currentText())
            hauteurs_x, tensions_y = [], []
            valid_points = 0
            for r_idx_recalc in range(num_calibration_points):
                try:
                    h_item = current_table.item(r_idx_recalc, 0)
                    v_item = current_table.item(r_idx_recalc, 1)
                    if h_item and v_item and h_item.text().strip() and v_item.text().strip():
                        h_val = float(h_item.text())
                        v_val = float(v_item.text())
                        hauteurs_x.append(h_val)
                        tensions_y.append(v_val)
                        valid_points += 1
                except (ValueError, AttributeError): pass 
            
            current_graph = widgets["graph"] # Get the graph specific to this tab
            if valid_points >= 2: 
                np_x = np.array(hauteurs_x)
                np_y = np.array(tensions_y)
                try:
                    slope, intercept = np.polyfit(np_x, np_y, 1)
                    y_pred = slope * np_x + intercept
                    if len(np_y) >=3 and not np.all(np.isclose(np_y, np.mean(np_y))): 
                        r_squared = 1 - (np.sum((np_y - y_pred)**2) / np.sum((np_y - np.mean(np_y))**2))
                    elif len(np_y) >=3 and np.all(np.isclose(np_y, y_pred)): 
                        r_squared = 1.0
                    else: r_squared = 0.0
                except (np.linalg.LinAlgError, ValueError) as e: 
                    slope, intercept, r_squared = 0,0,0
                    widgets["result_label"].setText(f"<b style='color:#ff5555;'>Erreur de calcul: {e}</b>")
                    current_graph.clear_plot("Erreur de calcul de régression")
                    return

                current_graph.plot(np_x, np_y, slope, intercept, r_squared)
                status_text = f"<b>Pente (Facteur):</b> {slope:.4f}<br>"
                status_text += f"<b>Ordonnée à l'origine:</b> {intercept:.4f}<br>"
                status_text += f"<b>Coefficient R²:</b> {r_squared:.4f}<br>"
                
                if r_squared >= 0.999:
                    status_text += "<b style='color:#50fa7b;'>Linéarité excellente (Validation OK).</b>"
                elif r_squared >= 0.996: 
                    status_text += "<b style='color:#adebad;'>Linéarité bonne (Validation OK).</b>"
                else:
                    status_text += f"<b style='color:#ff5555;'>Linéarité insuffisante (R² < 0.996). Calibration à refaire.</b>"
                widgets["result_label"].setText(status_text)
            else:
                current_graph.clear_plot("Pas assez de points (min 2) pour la régression")
                widgets["result_label"].setText("<i>Entrez au moins 2 points de calibration complets (Hauteur et Tension).</i>")
        
        def _validate_sonde_calibration_local(s_idx_valid_local):
            widgets = sonde_calibration_data_widgets[s_idx_valid_local]
            if not (widgets["cb_nettoyee"].isChecked() and \
                    widgets["cb_parallele"].isChecked() and \
                    widgets["cb_visuelle"].isChecked() and \
                    widgets["cb_cable"].isChecked()):
                QMessageBox.warning(calib_window, "Vérifications Incomplètes", 
                                    f"Veuillez cocher toutes les cases de vérification préalable pour la sonde {s_idx_valid_local+1}.")
                return

            num_calibration_points = int(widgets["points_combo"].currentText())
            valid_points_for_validation = 0
            hauteurs_x_val, tensions_y_val = [], []

            for r_idx_val in range(num_calibration_points):
                try:
                    h_item_val = widgets["table"].item(r_idx_val, 0)
                    v_item_val = widgets["table"].item(r_idx_val, 1)
                    if h_item_val and v_item_val and h_item_val.text().strip() and v_item_val.text().strip():
                        hauteurs_x_val.append(float(h_item_val.text()))
                        tensions_y_val.append(float(v_item_val.text()))
                        valid_points_for_validation +=1
                    else: 
                        QMessageBox.warning(calib_window, "Données Manquantes",
                                            f"Veuillez remplir toutes les cellules 'Hauteur' et 'Tension' pour les {num_calibration_points} points de la sonde {s_idx_valid_local+1}.")
                        return
                except (ValueError, AttributeError):
                    QMessageBox.warning(calib_window, "Données Invalides", 
                                        f"Les points de calibration pour la sonde {s_idx_valid_local+1} ne sont pas tous des nombres valides.")
                    return
            
            if valid_points_for_validation < num_calibration_points or valid_points_for_validation < 2:
                 QMessageBox.warning(calib_window, "Pas assez de données", 
                                        f"Veuillez fournir tous les {num_calibration_points} points de calibration valides pour la sonde {s_idx_valid_local+1}.")
                 return
            
            np_x_val = np.array(hauteurs_x_val)
            np_y_val = np.array(tensions_y_val)
            try:
                slope_val, intercept_val = np.polyfit(np_x_val, np_y_val, 1)
                y_pred_val = slope_val * np_x_val + intercept_val
                if len(np_y_val) >= 2 and not np.all(np.isclose(np_y_val, np.mean(np_y_val))):
                    r_squared_val = 1 - (np.sum((np_y_val - y_pred_val)**2) / np.sum((np_y_val - np.mean(np_y_val))**2))
                elif len(np_y_val) >=2 and np.all(np.isclose(np_y_val, y_pred_val)):
                    r_squared_val = 1.0
                else: r_squared_val = 0.0
            except (np.linalg.LinAlgError, ValueError) as e:
                QMessageBox.critical(calib_window, "Erreur de Calcul", f"Impossible de calculer la régression pour la sonde {s_idx_valid_local+1}: {e}")
                return

            if r_squared_val >= 0.996: 
                QMessageBox.information(calib_window, "Calibration Validée", 
                                        f"Calibration pour la sonde {s_idx_valid_local+1} validée avec succès !\n"
                                        f"Facteur (pente): {slope_val:.4f}\n"
                                        f"Ordonnée à l'origine: {intercept_val:.4f}\n"
                                        f"R²: {r_squared_val:.4f}")
                # Enregistrer les facteurs de calibration
                calibration_results[s_idx_valid_local] = {
                    "slope": slope_val,
                    "intercept": intercept_val,
                    "r2": r_squared_val,
                    "points": list(zip(hauteurs_x_val, tensions_y_val))
                }
                validated_sondes.add(s_idx_valid_local)
                # Vérifier si toutes les sondes sont validées pour activer le bouton sauvegarde
                if len(validated_sondes) == len(selected_sondes_indices):
                    save_btn.setEnabled(True)
            else:
                QMessageBox.warning(calib_window, "Validation Échouée", 
                                    f"La linéarité (R² = {r_squared_val:.4f}) pour la sonde {s_idx_valid_local+1} est insuffisante. "
                                    "Le R² doit être supérieur ou égal à 0.996.\n"
                                    "Veuillez vérifier les points ou refaire la calibration.")

        points_combo.currentIndexChanged.connect(
            lambda index, s_idx_combo=sonde_original_idx, tbl_combo=calibration_table, cmb_combo=points_combo: 
                _update_table_rows_local(int(cmb_combo.itemText(index)), tbl_combo, s_idx_combo)
        )
        recalculate_button.clicked.connect(lambda checked=False, s_idx_recalc=sonde_original_idx: _trigger_recalculation_local(s_idx_recalc))
        validate_sonde_button.clicked.connect(lambda checked=False, s_idx_valid=sonde_original_idx: _validate_sonde_calibration_local(s_idx_valid))
        calibration_table.itemChanged.connect(lambda item, s_idx_item=sonde_original_idx: _trigger_recalculation_local(s_idx_item) if item.column() < 2 else None)

        _update_table_rows_local(int(points_combo.currentText()), calibration_table, sonde_original_idx)
        _trigger_recalculation_local(sonde_original_idx) 

    main_v_layout_calib.addWidget(tabs_widget)

    # Ajout du bouton Sauvegarder la calibration
    save_btn = QPushButton("Sauvegarder la calibration")
    save_btn.setEnabled(False)
    def save_calibration_to_file():
        try:
            with open("calibration_results.json", "w", encoding="utf-8") as f:
                json.dump(calibration_results, f, indent=4)
            QMessageBox.information(calib_window, "Sauvegarde réussie", "Les résultats de calibration ont été sauvegardés dans calibration_results.json.")
        except Exception as e:
            QMessageBox.critical(calib_window, "Erreur de sauvegarde", f"Erreur lors de la sauvegarde : {e}")
    save_btn.clicked.connect(save_calibration_to_file)
    main_v_layout_calib.addWidget(save_btn, alignment=Qt.AlignCenter)

    calib_window.show()
    
    # Si cette fenêtre a créé l'application (cas de test direct), elle gère l'exec.
    # Sinon, la boucle d'événements est déjà gérée par la fenêtre précédente.
    if created_app_here_for_individual:
        sys.exit(app.exec_())

# --- Point d'Entrée Principal ---
if __name__ == '__main__':
    # La première fenêtre à être lancée est la sélection des sondes
    show_sonde_selection_config_window()

# Dans calibration.py, remplacez la classe CalibrationMainWindow par :

class CalibrationMainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calibration des Sondes - HRNeoWave")
        self.setMinimumSize(800, 600)
        
        layout = QVBoxLayout(self)
        
        # En-tête
        title_label = QLabel("Calibration des Sondes")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Bouton pour lancer la vraie calibration
        start_calib_btn = QPushButton("🔧 Démarrer la Calibration")
        start_calib_btn.setMinimumHeight(50)
        start_calib_btn.clicked.connect(self.start_calibration)
        layout.addWidget(start_calib_btn)
        
        # Theme switch
        self.theme_switch = QCheckBox("Mode sombre")
        self.theme_switch.setChecked(True)
        self.theme_switch.stateChanged.connect(self.toggle_theme)
        layout.addWidget(self.theme_switch)
        
        # Bouton continuer
        self.next_step = QPushButton("Continuer ➡️")
        self.next_step.setMinimumHeight(40)
        layout.addWidget(self.next_step, alignment=Qt.AlignCenter)
        
    def start_calibration(self):
        """Lance la fenêtre de sélection des sondes"""
        # Fermer cette fenêtre temporairement
        self.hide()
        
        # Lancer la vraie calibration
        show_sonde_selection_config_window()
        
        # Réafficher cette fenêtre après
        self.show()
        
    def toggle_theme(self):
        if self.theme_switch.isChecked():
            set_dark_mode_and_style(QApplication.instance())
        else:
            set_light_mode_and_style(QApplication.instance())
            
    def sync_theme_switch(self, theme):
        if theme == "dark":
            self.theme_switch.setChecked(True)
        else:
            self.theme_switch.setChecked(False)