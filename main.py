# main.py - Versão final com correções aplicadas
import sys
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QInputDialog, QMenu,
    QAction, QSystemTrayIcon, QStyle, QLabel, QScrollArea, QHBoxLayout,
    QMessageBox, QLineEdit, QMainWindow, QSizePolicy, QShortcut,
    QTextEdit, QDialog
)
from PyQt5.QtGui import (
    QIcon, QPainter, QColor, QFontDatabase, QFont,
    QCursor, QDrag, QPixmap, QMouseEvent, QKeySequence
)
from PyQt5.QtCore import (
    Qt, QSize, QPropertyAnimation, QEasingCurve,
    pyqtProperty, QPoint, QMimeData
)

# --- FUNÇÃO PARA ENCONTRAR RECURSOS ---
def resource_path(relative_path):
    """ Obtém o caminho absoluto para o recurso, funciona para dev e para PyInstaller """
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# --- Configurações ---
APP_DATA_DIR = Path.home() / "Documents" / "FCTBI_data"
DATA_FILE = str(APP_DATA_DIR / "respostas.json")
BACKUP_FILE = str(APP_DATA_DIR / "respostas_backup.json")
FONT_FILE = "BLMelody-Regular.otf"
APP_FONT_NAME = "BL Melody Regular"
PRIMARY_COLOR = "#463e91"
SECONDARY_COLOR = "#f0f0f0"
ACCENT_COLOR = "#5a52a9"
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 650
MIN_WINDOW_WIDTH = 350
MIN_WINDOW_HEIGHT = 500


# --- Classe para Animação de Fade ---
class FaderWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._opacity = 1.0
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(300)
        self.fade_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.fade_animation.finished.connect(self._on_fade_out_finished)
        self._is_hiding = False

    @pyqtProperty(float)
    def windowOpacity(self):
        return self._opacity

    @windowOpacity.setter
    def windowOpacity(self, value):
        self._opacity = value
        self.setWindowOpacity(value)

    def fade_in(self):
        self._is_hiding = False
        self.fade_animation.stop()
        self.setWindowOpacity(0.0)
        self.show()
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.start()

    def fade_out(self):
        self._is_hiding = True
        self.fade_animation.stop()
        self.fade_animation.setStartValue(1.0)
        self.fade_animation.setEndValue(0.0)
        self.fade_animation.start()

    def _on_fade_out_finished(self):
        if self._is_hiding:
            self.hide()


# --- Classe do Botão Flutuante ---
class FloatingButton(FaderWidget):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.setup_ui()

    def setup_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(60, 60)
        self.move(20, 500)  # Posição inicial
        self.drag_position = None
        self._was_click = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(0, 0, 0, 80))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(6, 8, 48, 48)
        painter.setBrush(QColor(PRIMARY_COLOR))
        painter.drawEllipse(5, 5, 50, 50)
        painter.setPen(QColor("#FFFFFF"))
        font = QFont(APP_FONT_NAME, 10, QFont.Bold)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignCenter, "FCTBI")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            self._was_click = True
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.drag_position:
            self.move(event.globalPos() - self.drag_position)
            self._was_click = False
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self._was_click:
            self.fade_out()
            self.callback()
            event.accept()
        self._was_click = False
        self.drag_position = None

class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajuda - FCTBI Respostas Rápidas")
        self.setFixedSize(500, 400)
        layout = QVBoxLayout()
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setHtml("""
            <h1>Manual do Usuário</h1>
            <h2>Como usar o FCTBI Respostas Rápidas</h2>
            <p>Este aplicativo permite gerenciar e acessar rapidamente respostas pré-definidas organizadas em seções.</p>
            <h3>Funcionalidades Principais:</h3>
            <ul>
                <li><b>Seções:</b> Organize suas respostas em diferentes categorias</li>
                <li><b>Busca:</b> Encontre respostas rapidamente pelo conteúdo</li>
                <li><b>Cópia rápida:</b> Clique em uma resposta para copiar para a área de transferência</li>
                <li><b>Arrastar e soltar:</b> Arraste respostas e seções para reorganizá-las</li>
            </ul>
            <h3>Atalhos de Teclado:</h3>
            <ul>
                <li><b>Ctrl+F:</b> Focar no campo de busca</li>
                <li><b>Ctrl+N:</b> Adicionar nova resposta</li>
                <li><b>Ctrl+S:</b> Salvar manualmente</li>
                <li><b>ESC:</b> Minimizar para a bola flutuante</li>
            </ul>
            <h3>Como usar:</h3>
            <ol>
                <li>Adicione seções usando o botão "+" na barra de seções</li>
                <li>Adicione respostas usando o botão "Adicionar Resposta"</li>
                <li>Clique em uma resposta para copiá-la</li>
                <li>Arraste seções ou respostas para reorganizá-las</li>
                <li>Clique nos três pontos (⋮) para editar ou remover respostas</li>
            </ol>
            <p>Oferecimento facilittec.com.br<br>de Pablo p/Bianca s2.</p></p>
        """)
        close_btn = QPushButton("Fechar")
        close_btn.clicked.connect(self.close)
        layout.addWidget(text_edit)
        layout.addWidget(close_btn)
        self.setLayout(layout)

class DraggableSectionButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMouseTracking(True)
        self.drag_start_position = None
        self.setCursor(Qt.OpenHandCursor)
        self.setCheckable(True)
        self.setObjectName("sectionButton")

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if not (event.buttons() & Qt.LeftButton) or not self.drag_start_position:
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        self.setCursor(Qt.ClosedHandCursor)
        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(f"SECTION:{self.text()}")
        pixmap = QPixmap(self.size())
        self.render(pixmap)
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
        drag.setMimeData(mime_data)
        drag.exec_(Qt.MoveAction)
        self.setCursor(Qt.OpenHandCursor)

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.setCursor(Qt.OpenHandCursor)
        super().mouseReleaseEvent(event)

class DraggableResponseWidget(QWidget):
    def __init__(self, response_data, main_window):
        super().__init__()
        self.response_data = response_data
        self.main_window = main_window
        self.drag_start_position = None
        self.setCursor(Qt.OpenHandCursor)
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        self.response_btn = QPushButton(self.response_data["texto"])
        self.response_btn.setObjectName("responseButton")
        self.response_btn.setToolTip("Clique para copiar ou arraste para reorganizar")
        self.response_btn.clicked.connect(self.on_copy_clicked)
        self.response_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.menu_btn = QPushButton("⋮")
        self.menu_btn.setObjectName("menuButton")
        self.menu_btn.setToolTip("Opções")
        menu = QMenu(self)
        edit_action = menu.addAction("Editar")
        edit_action.triggered.connect(self.on_edit_clicked)
        remove_action = menu.addAction("Remover")
        remove_action.triggered.connect(self.on_remove_clicked)
        self.menu_btn.setMenu(menu)
        layout.addWidget(self.response_btn)
        layout.addWidget(self.menu_btn)
        
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if not (event.buttons() & Qt.LeftButton) or not self.drag_start_position:
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        self.setCursor(Qt.ClosedHandCursor)
        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(f"RESPONSE:{self.response_data['texto']}")
        pixmap = QPixmap(self.size())
        self.render(pixmap)
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
        drag.setMimeData(mime_data)
        drag.exec_(Qt.MoveAction)
        self.setCursor(Qt.OpenHandCursor)

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.setCursor(Qt.OpenHandCursor)
        super().mouseReleaseEvent(event)
        
    def on_copy_clicked(self):
        self.main_window.copy_to_clipboard(self.response_data["texto"])

    def on_edit_clicked(self):
        self.main_window.edit_response(self.response_data["texto"])

    def on_remove_clicked(self):
        self.main_window.remove_response(self.response_data["texto"])

class DataManager:
    def __init__(self, data_file: str):
        self.data_file = data_file
        self.data = self._load_data()

    def _load_data(self) -> Dict[str, List[Dict[str, Any]]]:
        default_data = {"Geral": []}
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(default_data, f)
            return default_data
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not data: return default_data
                if isinstance(data, list):
                    migrated = {"Geral": [{"texto": item, "data": datetime.now().isoformat()} for item in data]}
                    with open(self.data_file, 'w', encoding='utf-8') as f: json.dump(migrated, f)
                    return migrated
                return data
        except (json.JSONDecodeError, IOError) as e:
            print(f"Erro ao carregar dados: {e}")
            if os.path.exists(BACKUP_FILE):
                try:
                    with open(BACKUP_FILE, 'r', encoding='utf-8') as f: return json.load(f)
                except: pass
            return default_data

    def save(self) -> bool:
        try:
            if os.path.exists(self.data_file): os.replace(self.data_file, BACKUP_FILE)
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
            return True
        except IOError as e:
            print(f"Erro ao salvar dados: {e}")
            return False

    def add_section(self, section_name: str) -> bool:
        if section_name and section_name not in self.data:
            self.data[section_name] = []
            return self.save()
        return False

    def rename_section(self, old_name: str, new_name: str) -> bool:
        if old_name not in self.data or new_name in self.data or not new_name: return False
        self.data[new_name] = self.data.pop(old_name)
        return self.save()

    def remove_section(self, section_name: str) -> bool:
        if len(self.data) <= 1 or section_name not in self.data: return False
        del self.data[section_name]
        return self.save()

    def add_response(self, section_name: str, text: str) -> bool:
        if section_name not in self.data or not text: return False
        self.data[section_name].append({"texto": text, "data": datetime.now().isoformat()})
        return self.save()

    def edit_response(self, section_name: str, old_text: str, new_text: str) -> bool:
        if section_name not in self.data or not new_text: return False
        for item in self.data[section_name]:
            if item["texto"] == old_text:
                item["texto"] = new_text
                item["data"] = datetime.now().isoformat()
                return self.save()
        return False

    def remove_response(self, section_name: str, text: str) -> bool:
        if section_name not in self.data: return False
        self.data[section_name] = [item for item in self.data[section_name] if item["texto"] != text]
        return self.save()

    def reorder_sections(self, new_order: List[str]) -> bool:
        if set(new_order) != set(self.data.keys()): return False
        self.data = {section: self.data[section] for section in new_order}
        return self.save()

    def reorder_responses(self, section_name: str, new_order: List[str]) -> bool:
        """
        ### MÉTODO CORRIGIDO ###
        Reordena as respostas de forma segura, evitando perda de dados.
        """
        if section_name not in self.data:
            return False

        item_map = {item["texto"]: item for item in self.data[section_name]}
        
        # Cria a nova lista na ordem recebida
        new_list = [item_map[text] for text in new_order if text in item_map]
        
        # Adiciona ao final quaisquer itens que estavam no original mas não na nova ordem
        # para garantir que nenhuma resposta seja perdida por um erro de filtragem.
        new_order_set = set(new_order)
        for text, item in item_map.items():
            if text not in new_order_set:
                new_list.append(item)

        self.data[section_name] = new_list
        return self.save()

class RespostaRapidaApp(QMainWindow, FaderWidget):
    def __init__(self):
        QMainWindow.__init__(self)
        FaderWidget.__init__(self)

        APP_DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.data_manager = DataManager(DATA_FILE)
        self.current_section = list(self.data_manager.data.keys())[0] if self.data_manager.data else "Geral"
        self.search_filter = ""
        self.drag_position = None

        # Configurar o ícone da janela
        self.setWindowIcon(QIcon(resource_path('fctbi.ico')))

        self.setup_ui()
        self.setup_connections()
        self.setup_tray_icon()
        self.setup_shortcuts()
        
        self.floating_button = FloatingButton(self.show_window)
        self.floating_button.hide()

        self.update_sections_ui()
        self.update_responses_ui()

    def setup_ui(self):
        self.setWindowTitle('FCTBI - Respostas Rápidas')
        self.setMinimumSize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        title_bar = QWidget()
        title_bar.setObjectName("titleBar")
        title_bar.setFixedHeight(45)
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(15, 0, 15, 0)
        title_label = QLabel("FCTBI")
        title_label.setObjectName("titleLabel")
        btn_help = QPushButton("?")
        btn_help.setObjectName("titleButton")
        btn_help.setFixedSize(30, 30)
        btn_help.setToolTip("Ajuda")
        btn_minimize = QPushButton("–")
        btn_minimize.setObjectName("titleButton")
        btn_minimize.setFixedSize(30, 30)
        btn_minimize.setToolTip("Minimizar")
        btn_close = QPushButton("✕")
        btn_close.setObjectName("titleButton")
        btn_close.setFixedSize(30, 30)
        btn_close.setToolTip("Fechar")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(btn_help)
        title_layout.addWidget(btn_minimize)
        title_layout.addWidget(btn_close)
        main_layout.addWidget(title_bar)
        btn_help.clicked.connect(self.show_help)
        btn_minimize.clicked.connect(self.minimize_window)
        btn_close.clicked.connect(self.close_window)
        search_bar = QWidget()
        search_bar.setObjectName("searchBar")
        search_bar.setFixedHeight(50)
        search_layout = QHBoxLayout(search_bar)
        search_layout.setContentsMargins(15, 5, 15, 5)
        self.search_input = QLineEdit()
        self.search_input.setObjectName("searchInput")
        self.search_input.setPlaceholderText("Buscar respostas...")
        search_layout.addWidget(self.search_input)
        main_layout.addWidget(search_bar)
        self.sections_container = QWidget()
        self.sections_container.setObjectName("sectionsContainer")
        self.sections_container.setFixedHeight(60)
        sections_layout = QHBoxLayout(self.sections_container)
        sections_layout.setContentsMargins(10, 5, 10, 5)
        self.sections_scroll = QScrollArea()
        self.sections_scroll.setWidgetResizable(True)
        self.sections_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.sections_widget = QWidget()
        self.sections_widget.setAcceptDrops(True)
        self.sections_layout = QHBoxLayout(self.sections_widget)
        self.sections_layout.setAlignment(Qt.AlignLeft)
        self.sections_layout.setContentsMargins(0, 0, 0, 0)
        self.sections_scroll.setWidget(self.sections_widget)
        btn_add_section = QPushButton("+")
        btn_add_section.setObjectName("addSectionButton")
        btn_add_section.setFixedSize(30, 30)
        btn_add_section.setToolTip("Adicionar nova seção")
        sections_layout.addWidget(self.sections_scroll)
        sections_layout.addWidget(btn_add_section)
        main_layout.addWidget(self.sections_container)
        btn_add_section.clicked.connect(self.add_section)
        self.content_container = QWidget()
        self.content_container.setObjectName("contentContainer")
        content_layout = QVBoxLayout(self.content_container)
        content_layout.setContentsMargins(15, 5, 15, 15)
        self.responses_scroll = QScrollArea()
        self.responses_scroll.setWidgetResizable(True)
        self.responses_widget = QWidget()
        self.responses_widget.setAcceptDrops(True)
        self.responses_layout = QVBoxLayout(self.responses_widget)
        self.responses_layout.setAlignment(Qt.AlignTop)
        self.responses_layout.setContentsMargins(0, 0, 5, 0)
        self.responses_scroll.setWidget(self.responses_widget)
        self.btn_add_response = QPushButton("Adicionar Resposta")
        self.btn_add_response.setObjectName("addButton")
        content_layout.addWidget(self.responses_scroll)
        content_layout.addWidget(self.btn_add_response)
        main_layout.addWidget(self.content_container)
        self.btn_add_response.clicked.connect(self.add_response)
        self.apply_styles()

    def apply_styles(self):
        self.setStyleSheet(f"""
            #centralWidget {{
                background-color: #FFFFFF;
                border: 5px solid {PRIMARY_COLOR};
                border-radius: 20px;
            }}
            #titleBar {{ background-color: transparent; }}
            #titleLabel {{
                font-family: "{APP_FONT_NAME}";
                color: {PRIMARY_COLOR};
                font-size: 16px;
                font-weight: bold;
            }}
            #titleButton {{
                background-color: transparent;
                color: {PRIMARY_COLOR};
                border: none;
                font-size: 16px;
                font-weight: bold;
                min-width: 30px;
                min-height: 30px;
            }}
            #titleButton:hover {{ background-color: {SECONDARY_COLOR}; border-radius: 5px; }}
            #searchBar {{ background-color: transparent; }}
            #searchInput {{
                border: 1px solid {SECONDARY_COLOR};
                border-radius: 15px;
                padding: 5px 15px;
                font-size: 12px;
            }}
            #searchInput:focus {{ border-color: {PRIMARY_COLOR}; }}
            #sectionsContainer {{ background-color: transparent; border-bottom: 1px solid {SECONDARY_COLOR}; }}
            #addSectionButton {{
                background-color: {PRIMARY_COLOR};
                color: white;
                border: none;
                border-radius: 15px;
                font-weight: bold;
            }}
            #addSectionButton:hover {{ background-color: {ACCENT_COLOR}; }}
            QPushButton#sectionButton {{
                background-color: {SECONDARY_COLOR};
                color: #555;
                border: none;
                padding: 7px 12px;
                border-radius: 15px;
                font-size: 11px;
                min-width: 60px;
            }}
            QPushButton#sectionButton:hover {{ background-color: #e0e0e0; }}
            QPushButton#sectionButton:checked {{
                background-color: {PRIMARY_COLOR};
                color: white;
                font-weight: bold;
            }}
            #contentContainer {{ background-color: transparent; }}
            QPushButton#responseButton {{
                background-color: {PRIMARY_COLOR};
                color: white;
                border: none;
                padding: 10px;
                text-align: left;
                border-radius: 5px;
                font-size: 12px;
            }}
            QPushButton#responseButton:hover {{ background-color: {ACCENT_COLOR}; }}
            QPushButton#menuButton {{
                background-color: {PRIMARY_COLOR};
                color: white;
                border: none;
                border-radius: 5px;
                min-width: 30px;
                max-width: 30px;
                font-weight: bold;
            }}
            QPushButton#menuButton:hover {{ background-color: {ACCENT_COLOR}; }}
            QPushButton#menuButton::menu-indicator {{ image: none; }}
            #addButton {{
                background-color: {PRIMARY_COLOR};
                color: white;
                font-weight: bold;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }}
            #addButton:hover {{ background-color: {ACCENT_COLOR}; }}
            QScrollBar:vertical {{
                border: none;
                background: #f0f0f0;
                width: 8px;
                margin: 0px;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical {{
                background: #d0d0d0;
                min-height: 20px;
                border-radius: 4px;
            }}
            QScrollBar:horizontal {{
                border: none;
                background: #f0f0f0;
                height: 8px;
                margin: 0px;
                border-radius: 4px;
            }}
            QScrollBar::handle:horizontal {{
                background: #d0d0d0;
                min-width: 20px;
                border-radius: 4px;
            }}
            #emptyLabel {{
                color: #999;
                font-size: 12px;
                font-style: italic;
            }}
            QInputDialog, QMessageBox {{
                background-color: white;
                font-family: "{APP_FONT_NAME}";
            }}
        """)
    
    def setup_connections(self):
        self.search_input.textChanged.connect(self.filter_responses)
        self.sections_widget.dragEnterEvent = self.sections_drag_enter_event
        self.sections_widget.dragMoveEvent = self.sections_drag_move_event
        self.sections_widget.dropEvent = self.sections_drop_event
        self.responses_widget.dragEnterEvent = self.responses_drag_enter_event
        self.responses_widget.dragMoveEvent = self.responses_drag_move_event
        self.responses_widget.dropEvent = self.responses_drop_event

    def setup_shortcuts(self):
        shortcut_search = QShortcut(QKeySequence("Ctrl+F"), self)
        shortcut_search.activated.connect(lambda: self.search_input.setFocus())
        shortcut_new = QShortcut(QKeySequence("Ctrl+N"), self)
        shortcut_new.activated.connect(self.add_response)
        shortcut_save = QShortcut(QKeySequence("Ctrl+S"), self)
        shortcut_save.activated.connect(self.data_manager.save)
        shortcut_minimize = QShortcut(QKeySequence("Esc"), self)
        shortcut_minimize.activated.connect(self.minimize_window)
      
    def setup_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(resource_path('fctbi.ico')))
        self.tray_icon.setToolTip("FCTBI - Respostas Rápidas")
    
        tray_menu = QMenu(self)
        show_action = QAction("Abrir", self)
        show_action.triggered.connect(self.show_window)
    
        exit_action = QAction("Sair", self)
        exit_action.triggered.connect(self.close_window)
    
        tray_menu.addAction(show_action)
        tray_menu.addSeparator()
        tray_menu.addAction(exit_action)
    
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def sections_drag_enter_event(self, event: QMouseEvent):
        if event.mimeData().hasText() and event.mimeData().text().startswith("SECTION:"):
            event.acceptProposedAction()
            
    def sections_drag_move_event(self, event: QMouseEvent):
        event.acceptProposedAction()
        
    def sections_drop_event(self, event: QMouseEvent):
        """
        ### MÉTODO CORRIGIDO ###
        Manipula o evento de soltar uma seção para reordená-la,
        funcionando corretamente para ambas as direções (esquerda e direita).
        """
        mime_text = event.mimeData().text()
        if not mime_text.startswith("SECTION:"):
            event.ignore()
            return

        dragged_section_name = mime_text.split(":", 1)[1]
        
        current_sections = list(self.data_manager.data.keys())
        current_sections.remove(dragged_section_name)

        # Determina o índice de inserção baseado na posição do mouse
        target_index = -1
        drop_x = event.pos().x()

        for i in range(self.sections_layout.count()):
            widget = self.sections_layout.itemAt(i).widget()
            if widget and isinstance(widget, DraggableSectionButton):
                # O ponto de inserção é antes do widget cujo centro está à direita do cursor
                if drop_x < widget.x() + widget.width() / 2:
                    target_index = i
                    break
        
        # Insere o nome da seção na posição correta da lista
        if target_index != -1:
            # Pega o nome da seção alvo para encontrar a posição na lista de dados
            target_section_name = self.sections_layout.itemAt(target_index).widget().text()
            try:
                insert_pos = current_sections.index(target_section_name)
                current_sections.insert(insert_pos, dragged_section_name)
            except ValueError:
                # Fallback caso não encontre, adiciona no final
                current_sections.append(dragged_section_name)
        else:
            # Se nenhum índice foi encontrado, o item foi solto no final
            current_sections.append(dragged_section_name)

        # Salva a nova ordem e atualiza a UI
        if self.data_manager.reorder_sections(current_sections):
            self.update_sections_ui()
        
        event.acceptProposedAction()

    def responses_drag_enter_event(self, event: QMouseEvent):
        if event.mimeData().hasText() and event.mimeData().text().startswith("RESPONSE:"):
            event.acceptProposedAction()
            
    def responses_drag_move_event(self, event: QMouseEvent):
        event.acceptProposedAction()

    def responses_drop_event(self, event: QMouseEvent):
        """
        ### MÉTODO CORRIGIDO ###
        Manipula o evento de soltar uma resposta para reordená-la, funcionando
        corretamente mesmo com filtros de busca ativos.
        """
        mime_text = event.mimeData().text()
        if not mime_text.startswith("RESPONSE:"):
            event.ignore()
            return

        dragged_response_text = mime_text.split(":", 1)[1]

        # A fonte da verdade é sempre a lista completa do DataManager
        all_responses_texts = [resp["texto"] for resp in self.data_manager.data.get(self.current_section, [])]
        
        # Remove temporariamente o item arrastado da lista
        try:
            all_responses_texts.remove(dragged_response_text)
        except ValueError:
            event.ignore()
            return # O item arrastado não estava na lista de dados, ignora

        # Determina o widget de destino e a posição de inserção na UI
        target_index_in_layout = -1
        drop_y = event.pos().y()
        for i in range(self.responses_layout.count()):
            widget = self.responses_layout.itemAt(i).widget()
            if widget:
                if drop_y < widget.y() + widget.height() / 2:
                    target_index_in_layout = i
                    break
        
        # Insere o item na posição correta da lista completa de dados
        if target_index_in_layout != -1:
            # Pega o texto do widget de destino na UI
            target_widget = self.responses_layout.itemAt(target_index_in_layout).widget()
            target_text = target_widget.response_data['texto']
            try:
                # Encontra a posição real do widget de destino na lista completa
                insert_pos_in_all = all_responses_texts.index(target_text)
                all_responses_texts.insert(insert_pos_in_all, dragged_response_text)
            except ValueError:
                # Se o texto de destino não for encontrado, adiciona no final
                all_responses_texts.append(dragged_response_text)
        else:
            # Se não encontrou índice, soltou no final da lista visível
            all_responses_texts.append(dragged_response_text)

        # Salva a nova ordem e atualiza a UI
        if self.data_manager.reorder_responses(self.current_section, all_responses_texts):
            self.update_responses_ui()
            
        event.accept()

    def update_sections_ui(self):
        while self.sections_layout.count():
            child = self.sections_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        for section_name in self.data_manager.data.keys():
            btn = DraggableSectionButton(section_name)
            btn.setChecked(section_name == self.current_section)
            btn.clicked.connect(lambda _, s=section_name: self.select_section(s))
            btn.setContextMenuPolicy(Qt.CustomContextMenu)
            btn.customContextMenuRequested.connect(
                lambda pos, s=section_name: self.show_section_menu(s, pos))
            self.sections_layout.addWidget(btn)

    def update_responses_ui(self):
        while self.responses_layout.count():
            child = self.responses_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        responses = [
            resp for resp in self.data_manager.data.get(self.current_section, [])
            if not self.search_filter or self.search_filter.lower() in resp["texto"].lower()
        ]
        if not responses:
            empty_label = QLabel("Nenhuma resposta encontrada." if self.search_filter 
                               else "Nenhuma resposta nesta seção.")
            empty_label.setObjectName("emptyLabel")
            empty_label.setAlignment(Qt.AlignCenter)
            self.responses_layout.addWidget(empty_label)
        else:
            for response in responses:
                self.responses_layout.addWidget(DraggableResponseWidget(response, self))

    def select_section(self, section_name: str):
        if section_name in self.data_manager.data:
            self.current_section = section_name
            self.update_sections_ui()
            self.update_responses_ui()

    def filter_responses(self, search_text: str):
        self.search_filter = search_text
        self.update_responses_ui()
    
    def add_section(self):
        section_name, ok = QInputDialog.getText(
            self, 'Nova Seção', 'Digite o nome da nova seção:')
        if ok and section_name:
            if self.data_manager.add_section(section_name):
                self.select_section(section_name)
            else:
                QMessageBox.warning(self, "Erro", "Já existe uma seção com este nome.")
    
    def rename_section(self, section_name: str):
        new_name, ok = QInputDialog.getText(
            self, 'Renomear Seção', 
            f'Digite o novo nome para "{section_name}":',
            text=section_name)
        if ok and new_name and new_name != section_name:
            if self.data_manager.rename_section(section_name, new_name):
                self.select_section(new_name)
            else:
                QMessageBox.warning(self, "Erro", "Não foi possível renomear a seção.")
                
    def remove_section(self, section_name: str):
        if len(self.data_manager.data) <= 1:
            QMessageBox.warning(self, "Aviso", "Não é possível remover a última seção.")
            return
        reply = QMessageBox.question(
            self, 'Confirmar Remoção',
            f'Tem certeza que deseja remover a seção "{section_name}" e todas as suas respostas?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.data_manager.remove_section(section_name):
                new_section = next(iter(self.data_manager.data.keys()))
                self.select_section(new_section)
                
    def show_section_menu(self, section_name: str, pos: QPoint):
        menu = QMenu(self)
        rename_action = menu.addAction("Renomear")
        rename_action.triggered.connect(lambda: self.rename_section(section_name))
        remove_action = menu.addAction("Remover")
        remove_action.triggered.connect(lambda: self.remove_section(section_name))
        sender = self.sender()
        menu.exec_(sender.mapToGlobal(pos))
        
    def add_response(self):
        text, ok = QInputDialog.getText(
            self, 'Nova Resposta', 
            f'Digite a nova resposta para a seção "{self.current_section}":')
        if ok and text:
            if self.data_manager.add_response(self.current_section, text):
                self.update_responses_ui()
                
    def edit_response(self, old_text: str):
        new_text, ok = QInputDialog.getText(
            self, 'Editar Resposta', 'Edite a resposta:', text=old_text)
        if ok and new_text and new_text != old_text:
            if self.data_manager.edit_response(self.current_section, old_text, new_text):
                self.update_responses_ui()
                
    def remove_response(self, text: str):
        reply = QMessageBox.question(
            self, 'Confirmar Remoção',
            f'Tem certeza que deseja remover esta resposta?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.data_manager.remove_response(self.current_section, text):
                self.update_responses_ui()
                
    def copy_to_clipboard(self, text: str):
        QApplication.clipboard().setText(text)
        self.tray_icon.showMessage(
            "Copiado!",
            f'Resposta copiada: "{text[:30]}..."',
            QSystemTrayIcon.Information,
            2000
        )
        
    def show_help(self):
        help_dialog = HelpDialog(self)
        help_dialog.exec_()
        
    def show_window(self):
        """Restaura da bola flutuante ou do tray icon."""
        self.floating_button.fade_out()
        self.fade_in()
        self.activateWindow()
        self.raise_()

    def minimize_window(self):
        """Minimiza para a bola flutuante."""
        self.fade_out()
        self.floating_button.fade_in()

    def close_window(self):
        """Fecha completamente a aplicação."""
        self.data_manager.save()
        self.floating_button.close()
        self.tray_icon.hide()
        QApplication.quit()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.pos().y() < 45:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_position:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.drag_position = None
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Carrega a fonte usando a função resource_path
    font_path = resource_path(FONT_FILE)
    if os.path.exists(font_path):
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id < 0:
            print(f"Aviso: A fonte '{FONT_FILE}' não pôde ser carregada.")
    else:
        print(f"Aviso: Arquivo de fonte '{FONT_FILE}' não encontrado em {font_path}.")
    
    window = RespostaRapidaApp()
    window.show()
    
    sys.exit(app.exec_())