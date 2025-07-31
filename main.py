# main.py - FCTBI Respostas Rápidas - Versão Otimizada
"""
FCTBI - Ferramenta de Cópia de Textos para Bianca e Interação
Aplicativo para gerenciar e acessar rapidamente respostas pré-definidas.

Autor: Pablo Bernar
Versão: 2.0 - Otimizada com boas práticas
"""

import sys
import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QInputDialog, QMenu,
    QAction, QSystemTrayIcon, QStyle, QLabel, QScrollArea, QHBoxLayout,
    QMessageBox, QLineEdit, QMainWindow, QSizePolicy, QShortcut,
    QTextEdit, QTextBrowser, QDialog, QCheckBox, QSpinBox, QFormLayout, QGroupBox,
    QFileDialog, QProgressBar, QSplitter, QFrame, QToolTip, QComboBox
)
from PyQt5.QtGui import (
    QIcon, QPainter, QColor, QFontDatabase, QFont,
    QCursor, QDrag, QPixmap, QMouseEvent, QKeySequence, QPen
)
from PyQt5.QtCore import (
    Qt, QSize, QPropertyAnimation, QEasingCurve, QTimer,
    pyqtProperty, QPoint, QMimeData, QRect, pyqtSignal
)

# Importação de validação de seções
from special_effects import validate_section_name

# =============================================================================
# CONSTANTES E CONFIGURAÇÕES
# =============================================================================

@dataclass
class AppConfig:
    """Configurações da aplicação"""
    APP_DATA_DIR: Path = field(default_factory=lambda: Path.home() / "Documents" / "FCTBI_data")
    DATA_FILE: str = field(init=False)
    BACKUP_FILE: str = field(init=False)
    CONFIG_FILE: str = field(init=False)
    STATS_FILE: str = field(init=False)
    FONT_FILE: str = "BLMelody-Regular.otf"
    APP_FONT_NAME: str = "BL Melody Regular"
    WINDOW_WIDTH: int = 480
    WINDOW_HEIGHT: int = 720
    MIN_WINDOW_WIDTH: int = 420
    MIN_WINDOW_HEIGHT: int = 580
    
    def __post_init__(self):
        self.DATA_FILE = str(self.APP_DATA_DIR / "respostas.json")
        self.BACKUP_FILE = str(self.APP_DATA_DIR / "respostas_backup.json")
        self.CONFIG_FILE = str(self.APP_DATA_DIR / "config.json")
        self.STATS_FILE = str(self.APP_DATA_DIR / "stats.json")

# Instância global de configuração
CONFIG = AppConfig()

# Temas modernizados
THEMES = {
    "light": {
        "PRIMARY_COLOR": "#6366f1",      # Indigo moderno
        "SECONDARY_COLOR": "#f8fafc",    # Slate 50
        "ACCENT_COLOR": "#4f46e5",       # Indigo 600
        "BACKGROUND": "#ffffff",         # Branco puro
        "TEXT_COLOR": "#1e293b",         # Slate 800
        "BORDER_COLOR": "#e2e8f0",       # Slate 200
        "SUCCESS_COLOR": "#10b981",      # Emerald 500
        "WARNING_COLOR": "#f59e0b",      # Amber 500
        "ERROR_COLOR": "#ef4444",        # Red 500
        "CARD_BG": "#ffffff",            # Branco para cards
        "CARD_SHADOW": "rgba(0, 0, 0, 0.1)",
        "HOVER_BG": "#f1f5f9"           # Slate 100
    },
    "dark": {
        "PRIMARY_COLOR": "#8b5cf6",      # Violet 500
        "SECONDARY_COLOR": "#1e293b",    # Slate 800
        "ACCENT_COLOR": "#7c3aed",       # Violet 600
        "BACKGROUND": "#0f172a",         # Slate 900
        "TEXT_COLOR": "#f8fafc",         # Slate 50
        "BORDER_COLOR": "#334155",       # Slate 700
        "SUCCESS_COLOR": "#10b981",      # Emerald 500
        "WARNING_COLOR": "#f59e0b",      # Amber 500
        "ERROR_COLOR": "#ef4444",        # Red 500
        "CARD_BG": "#1e293b",            # Slate 800 para cards
        "CARD_SHADOW": "rgba(0, 0, 0, 0.3)",
        "HOVER_BG": "#334155"           # Slate 700
    }
}

# =============================================================================
# UTILITÁRIOS
# =============================================================================

def resource_path(relative_path: str) -> str:
    """
    Obtém o caminho absoluto para o recurso, funciona para dev e para PyInstaller
    
    Args:
        relative_path: Caminho relativo do recurso
        
    Returns:
        Caminho absoluto do recurso
    """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def safe_json_load(file_path: str, default_data: Any) -> Any:
    """
    Carrega dados JSON de forma segura
    
    Args:
        file_path: Caminho do arquivo
        default_data: Dados padrão em caso de erro
        
    Returns:
        Dados carregados ou dados padrão
    """
    try:
        if not os.path.exists(file_path):
            return default_data
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Erro ao carregar {file_path}: {e}")
        return default_data

def safe_json_save(file_path: str, data: Any) -> bool:
    """
    Salva dados JSON de forma segura
    
    Args:
        file_path: Caminho do arquivo
        data: Dados para salvar
        
    Returns:
        True se salvou com sucesso, False caso contrário
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except IOError as e:
        print(f"Erro ao salvar {file_path}: {e}")
        return False

# =============================================================================
# GERENCIADORES DE DADOS
# =============================================================================

class ConfigManager:
    """Gerenciador de configurações da aplicação"""
    
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Carrega configurações do arquivo"""
        default_config = {
            "theme": "light",
            "auto_backup": True,
            "backup_interval": 60,  # minutos
            "show_copy_confirmation": True,
            "play_copy_sound": False,
            "sort_responses_by": "creation",  # creation, alphabetical, usage
            "window_position": None,
            "window_size": [CONFIG.WINDOW_WIDTH, CONFIG.WINDOW_HEIGHT]
        }
        
        config = safe_json_load(self.config_file, default_config)
        
        # Merge com default para garantir todas as chaves
        for key, value in default_config.items():
            if key not in config:
                config[key] = value
                
        return config

    def save_config(self, config: Optional[Dict[str, Any]] = None) -> bool:
        """Salva configurações no arquivo"""
        config_to_save = config or self.config
        if safe_json_save(self.config_file, config_to_save):
            if config:
                self.config = config
            return True
        return False

    def get(self, key: str, default: Any = None) -> Any:
        """Obtém valor de configuração"""
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Define valor de configuração"""
        self.config[key] = value
        self.save_config()

class StatsManager:
    """Gerenciador de estatísticas de uso"""
    
    def __init__(self, stats_file: str):
        self.stats_file = stats_file
        self.stats = self._load_stats()

    def _load_stats(self) -> Dict[str, Any]:
        """Carrega estatísticas do arquivo"""
        default_stats = {
            "response_usage": {},  # {texto: count}
            "section_usage": {},   # {section: count}
            "total_copies": 0,
            "daily_usage": {},     # {date: count}
            "created_responses": 0,
            "deleted_responses": 0
        }
        
        stats = safe_json_load(self.stats_file, default_stats)
        
        # Salvar default se arquivo não existia
        if not os.path.exists(self.stats_file):
            safe_json_save(self.stats_file, default_stats)
            
        return stats

    def save_stats(self) -> bool:
        """Salva estatísticas no arquivo"""
        return safe_json_save(self.stats_file, self.stats)

    def record_copy(self, text: str, section: str) -> None:
        """Registra uma cópia de resposta"""
        self.stats["total_copies"] += 1
        self.stats["response_usage"][text] = self.stats["response_usage"].get(text, 0) + 1
        self.stats["section_usage"][section] = self.stats["section_usage"].get(section, 0) + 1
        
        today = datetime.now().strftime("%Y-%m-%d")
        self.stats["daily_usage"][today] = self.stats["daily_usage"].get(today, 0) + 1
        
        self.save_stats()

    def record_response_created(self) -> None:
        """Registra criação de resposta"""
        self.stats["created_responses"] += 1
        self.save_stats()

    def record_response_deleted(self) -> None:
        """Registra remoção de resposta"""
        self.stats["deleted_responses"] += 1
        self.save_stats()

    def get_most_used_responses(self, limit: int = 10) -> List[Tuple[str, int]]:
        """Retorna lista de (texto, uso) das respostas mais usadas"""
        return sorted(self.stats["response_usage"].items(), 
                     key=lambda x: x[1], reverse=True)[:limit]

class DataManager:
    """Gerenciador de dados das respostas"""
    
    def __init__(self, data_file: str):
        self.data_file = data_file
        self.data = self._load_data()

    def _load_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """Carrega dados das respostas"""
        default_data = {"Geral": []}
        
        if not os.path.exists(self.data_file):
            safe_json_save(self.data_file, default_data)
            return default_data
            
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if not data:
                return default_data
                
            # Migração de formato antigo (lista) para novo (dicionário)
            if isinstance(data, list):
                migrated = {
                    "Geral": [
                        {"texto": item, "data": datetime.now().isoformat()} 
                        for item in data
                    ]
                }
                safe_json_save(self.data_file, migrated)
                return migrated
                
            return data
            
        except (json.JSONDecodeError, IOError) as e:
            print(f"Erro ao carregar dados: {e}")
            # Tentar usar backup se existir
            if os.path.exists(CONFIG.BACKUP_FILE):
                backup_data = safe_json_load(CONFIG.BACKUP_FILE, default_data)
                if backup_data != default_data:
                    return backup_data
            return default_data

    def save(self) -> bool:
        """Salva dados no arquivo com backup automático"""
        try:
            if os.path.exists(self.data_file): 
                # Criar backup com timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"{CONFIG.BACKUP_FILE}_{timestamp}"
                shutil.copy2(self.data_file, backup_name)
                
                # Manter apenas os 5 backups mais recentes
                backup_dir = Path(self.data_file).parent
                backup_files = sorted(backup_dir.glob("respostas_backup.json_*"))
                if len(backup_files) > 5:
                    for old_backup in backup_files[:-5]:
                        old_backup.unlink()
                        
            return safe_json_save(self.data_file, self.data)
        except IOError as e:
            print(f"Erro ao salvar dados: {e}")
            return False

    def add_section(self, section_name: str) -> bool:
        """Adiciona nova seção"""
        if section_name and section_name not in self.data:
            self.data[section_name] = []
            return self.save()
        return False

    def rename_section(self, old_name: str, new_name: str) -> bool:
        """Renomeia uma seção"""
        if (old_name not in self.data or 
            new_name in self.data or 
            not new_name):
            return False
            
        self.data[new_name] = self.data.pop(old_name)
        return self.save()

    def remove_section(self, section_name: str) -> bool:
        """Remove uma seção"""
        if len(self.data) <= 1 or section_name not in self.data:
            return False
            
        del self.data[section_name]
        return self.save()

    def add_response(self, section_name: str, text: str) -> bool:
        """Adiciona nova resposta"""
        if section_name not in self.data or not text:
            return False
            
        self.data[section_name].append({
            "texto": text, 
            "data": datetime.now().isoformat()
        })
        return self.save()

    def edit_response(self, section_name: str, old_text: str, new_text: str) -> bool:
        """Edita uma resposta existente"""
        if section_name not in self.data or not new_text:
            return False
            
        for item in self.data[section_name]:
            if item["texto"] == old_text:
                item["texto"] = new_text
                item["data"] = datetime.now().isoformat()
                return self.save()
        return False

    def duplicate_response(self, section_name: str, text: str) -> bool:
        """Duplica uma resposta"""
        if section_name not in self.data:
            return False
            
        new_text = f"{text} (cópia)"
        counter = 1
        while any(item["texto"] == new_text for item in self.data[section_name]):
            new_text = f"{text} (cópia {counter})"
            counter += 1
            
        return self.add_response(section_name, new_text)

    def remove_response(self, section_name: str, text: str) -> bool:
        """Remove uma resposta"""
        if section_name not in self.data:
            return False
            
        self.data[section_name] = [
            item for item in self.data[section_name] 
            if item["texto"] != text
        ]
        return self.save()

    def reorder_sections(self, new_order: List[str]) -> bool:
        """Reordena seções"""
        if set(new_order) != set(self.data.keys()):
            return False
            
        self.data = {section: self.data[section] for section in new_order}
        return self.save()

    def reorder_responses(self, section_name: str, new_order: List[str]) -> bool:
        """Reordena respostas em uma seção"""
        if section_name not in self.data:
            return False

        item_map = {item["texto"]: item for item in self.data[section_name]}
        new_list = [item_map[text] for text in new_order if text in item_map]
        
        # Adicionar itens que não estão na nova ordem
        new_order_set = set(new_order)
        for text, item in item_map.items():
            if text not in new_order_set:
                new_list.append(item)

        self.data[section_name] = new_list
        return self.save()

    def sort_responses(self, section_name: str, sort_by: str, usage_stats: Dict[str, int]) -> bool:
        """Ordena respostas por critério especificado"""
        if section_name not in self.data:
            return False
            
        responses = self.data[section_name]
        
        if sort_by == "alphabetical":
            responses.sort(key=lambda x: x["texto"].lower())
        elif sort_by == "creation":
            responses.sort(key=lambda x: x.get("data", ""))
        elif sort_by == "usage":
            responses.sort(key=lambda x: usage_stats.get(x["texto"], 0), reverse=True)
            
        return self.save()

    def export_data(self, file_path: str, section_name: Optional[str] = None) -> bool:
        """Exporta dados para arquivo"""
        try:
            if section_name and section_name in self.data:
                export_data = {section_name: self.data[section_name]}
            else:
                export_data = self.data
                
            with open(file_path, 'w', encoding='utf-8') as f:
                if file_path.endswith('.json'):
                    json.dump(export_data, f, ensure_ascii=False, indent=4)
                else:  # .txt
                    for section, responses in export_data.items():
                        f.write(f"=== {section} ===\n\n")
                        for response in responses:
                            f.write(f"{response['texto']}\n\n")
                        f.write("\n" + "="*50 + "\n\n")
            return True
        except IOError:
            return False

    def import_data(self, file_path: str) -> bool:
        """Importa dados de arquivo"""
        try:
            if file_path.endswith('.json'):
                imported_data = safe_json_load(file_path, {})
                
                # Merge com dados existentes
                for section, responses in imported_data.items():
                    if section not in self.data:
                        self.data[section] = []
                    
                    existing_texts = {r["texto"] for r in self.data[section]}
                    for response in responses:
                        if isinstance(response, str):
                            response = {
                                "texto": response, 
                                "data": datetime.now().isoformat()
                            }
                        if response["texto"] not in existing_texts:
                            self.data[section].append(response)
                            
            else:  # .txt
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Processar arquivo texto simples
                if "Geral" not in self.data:
                    self.data["Geral"] = []
                    
                existing_texts = {r["texto"] for r in self.data["Geral"]}
                lines = [line.strip() for line in content.split('\n') if line.strip()]
                
                for line in lines:
                    if line not in existing_texts and not line.startswith('==='):
                        self.data["Geral"].append({
                            "texto": line,
                            "data": datetime.now().isoformat()
                        })
                        
            return self.save()
        except (IOError, json.JSONDecodeError):
            return False

# =============================================================================
# WIDGETS PERSONALIZADOS
# =============================================================================

class DragDropIndicator(QWidget):
    """Widget para mostrar onde o item será inserido durante o drag"""
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setFixedHeight(3)
        self.hide()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Gradiente moderno
        gradient = QColor("#6366f1")
        painter.fillRect(self.rect(), gradient)

class FaderWidget(QWidget):
    """Widget com animação de fade in/out"""
    
    def __init__(self, parent: Optional[QWidget] = None):
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
        """Anima fade in"""
        self._is_hiding = False
        self.fade_animation.stop()
        self.setWindowOpacity(0.0)
        self.show()
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.start()

    def fade_out(self):
        """Anima fade out"""
        self._is_hiding = True
        self.fade_animation.stop()
        self.fade_animation.setStartValue(1.0)
        self.fade_animation.setEndValue(0.0)
        self.fade_animation.start()

    def _on_fade_out_finished(self):
        """Callback quando fade out termina"""
        if self._is_hiding:
            self.hide()

class FloatingButton(FaderWidget):
    """Botão flutuante para minimizar aplicação"""
    
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.setup_ui()

    def setup_ui(self):
        """Configura interface do botão flutuante"""
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(70, 70)
        self.drag_position = None
        self._was_click = False
        self.setToolTip("Clique para abrir o FCTBI\nArraste para mover")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Sombra externa
        painter.setBrush(QColor(0, 0, 0, 80))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(8, 10, 54, 54)
        
        # Gradiente principal
        gradient = QColor("#6366f1")
        painter.setBrush(gradient)
        painter.drawEllipse(5, 5, 60, 60)
        
        # Borda interna
        painter.setPen(QPen(QColor("#ffffff"), 2))
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(5, 5, 60, 60)
        
        # Texto
        painter.setPen(QColor("#ffffff"))
        font = QFont(CONFIG.APP_FONT_NAME, 9, QFont.Bold)
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
            self.callback()
            event.accept()
        else:
            # Salvar posição quando a bola for movida
            if hasattr(self.callback, '__self__') and hasattr(self.callback.__self__, 'config_manager'):
                config_manager = self.callback.__self__.config_manager
                config_manager.set("floating_button_position", [self.x(), self.y()])
        
        self._was_click = False
        self.drag_position = None

class SettingsDialog(QDialog):
    def __init__(self, config_manager: ConfigManager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.setWindowTitle("Configurações")
        self.setFixedSize(420, 380)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Grupo Aparência
        appearance_group = QGroupBox("Aparência")
        appearance_layout = QFormLayout()
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["light", "dark"])
        self.theme_combo.setCurrentText(self.config_manager.get("theme"))
        appearance_layout.addRow("Tema:", self.theme_combo)
        
        appearance_group.setLayout(appearance_layout)
        
        # Grupo Comportamento
        behavior_group = QGroupBox("Comportamento")
        behavior_layout = QFormLayout()
        
        self.copy_confirmation = QCheckBox()
        self.copy_confirmation.setChecked(self.config_manager.get("show_copy_confirmation"))
        behavior_layout.addRow("Confirmar ao copiar:", self.copy_confirmation)
        
        self.play_sound = QCheckBox()
        self.play_sound.setChecked(self.config_manager.get("play_copy_sound"))
        behavior_layout.addRow("Som ao copiar:", self.play_sound)
        
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["creation", "alphabetical", "usage"])
        self.sort_combo.setCurrentText(self.config_manager.get("sort_responses_by"))
        behavior_layout.addRow("Ordenar por:", self.sort_combo)
        
        behavior_group.setLayout(behavior_layout)
        
        # Grupo Backup
        backup_group = QGroupBox("Backup")
        backup_layout = QFormLayout()
        
        self.auto_backup = QCheckBox()
        self.auto_backup.setChecked(self.config_manager.get("auto_backup"))
        backup_layout.addRow("Backup automático:", self.auto_backup)
        
        self.backup_interval = QSpinBox()
        self.backup_interval.setRange(5, 1440)  # 5 min a 24h
        self.backup_interval.setSuffix(" min")
        self.backup_interval.setValue(self.config_manager.get("backup_interval"))
        backup_layout.addRow("Intervalo:", self.backup_interval)
        
        backup_group.setLayout(backup_layout)
        
        # Botões
        buttons_layout = QHBoxLayout()
        save_btn = QPushButton("Salvar")
        cancel_btn = QPushButton("Cancelar")
        
        save_btn.clicked.connect(self.save_settings)
        cancel_btn.clicked.connect(self.reject)
        
        buttons_layout.addWidget(save_btn)
        buttons_layout.addWidget(cancel_btn)
        
        layout.addWidget(appearance_group)
        layout.addWidget(behavior_group)
        layout.addWidget(backup_group)
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)

    def save_settings(self):
        config = {
            "theme": self.theme_combo.currentText(),
            "show_copy_confirmation": self.copy_confirmation.isChecked(),
            "play_copy_sound": self.play_sound.isChecked(),
            "sort_responses_by": self.sort_combo.currentText(),
            "auto_backup": self.auto_backup.isChecked(),
            "backup_interval": self.backup_interval.value()
        }
        
        # Preservar configurações existentes
        for key, value in self.config_manager.config.items():
            if key not in config:
                config[key] = value
                
        self.config_manager.save_config(config)
        self.accept()

class StatsDialog(QDialog):
    def __init__(self, stats_manager: StatsManager, parent=None):
        super().__init__(parent)
        self.stats_manager = stats_manager
        self.setWindowTitle("Estatísticas de Uso")
        self.setFixedSize(520, 420)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Estatísticas gerais
        general_group = QGroupBox("Estatísticas Gerais")
        general_layout = QFormLayout()
        
        stats = self.stats_manager.stats
        general_layout.addRow("Total de cópias:", QLabel(str(stats["total_copies"])))
        general_layout.addRow("Respostas criadas:", QLabel(str(stats["created_responses"])))
        general_layout.addRow("Respostas removidas:", QLabel(str(stats["deleted_responses"])))
        
        general_group.setLayout(general_layout)
        
        # Respostas mais usadas
        most_used_group = QGroupBox("Respostas Mais Usadas")
        most_used_layout = QVBoxLayout()
        
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        most_used = self.stats_manager.get_most_used_responses(10)
        for i, (text, count) in enumerate(most_used, 1):
            label = QLabel(f"{i}. {text[:50]}{'...' if len(text) > 50 else ''} ({count}x)")
            label.setWordWrap(True)
            scroll_layout.addWidget(label)
        
        scroll_area.setWidget(scroll_widget)
        scroll_area.setMaximumHeight(150)
        most_used_layout.addWidget(scroll_area)
        most_used_group.setLayout(most_used_layout)
        
        # Botão fechar
        close_btn = QPushButton("Fechar")
        close_btn.clicked.connect(self.close)
        
        layout.addWidget(general_group)
        layout.addWidget(most_used_group)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)

class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajuda - FCTBI Respostas Rápidas")
        self.setFixedSize(570, 470)
        layout = QVBoxLayout()
        text_browser = QTextBrowser()
        text_browser.setOpenExternalLinks(True)
        text_browser.setHtml("""
            <h1>Manual do Usuário - FCTBI</h1>
            <h2>Como usar o FCTBI Respostas Rápidas</h2>
            <p>Este aplicativo permite gerenciar e acessar rapidamente respostas pré-definidas organizadas em seções.</p>
            <h3>Funcionalidades Principais:</h3>
            <ul>
                <li><b>Seções:</b> Organize suas respostas em diferentes categorias</li>
                <li><b>Busca:</b> Encontre respostas rapidamente pelo conteúdo</li>
                <li><b>Cópia rápida:</b> Clique em uma resposta para copiar para a área de transferência</li>
                <li><b>Setas de organização:</b> Use as setas ↑ e ↓ para mover respostas para cima ou baixo</li>
                <li><b>Arrastar e soltar livre:</b> Arraste respostas e seções para reorganizá-las livremente</li>
                <li><b>Mover entre seções:</b> Arraste respostas para outras seções</li>
                <li><b>Reordenar seções:</b> Arraste seções para reorganizar a ordem</li>
                <li><b>Estatísticas:</b> Veja quais respostas são mais utilizadas</li>
                <li><b>Temas:</b> Escolha entre modo claro e escuro</li>
                <li><b>Backup automático:</b> Seus dados são salvos automaticamente</li>
            </ul>
            <h3>Drag and Drop - Organização Livre:</h3>
            <ul>
                <li><b>Reordenar respostas:</b> Arraste respostas dentro da mesma seção para reorganizar</li>
                <li><b>Mover respostas:</b> Arraste respostas para outras seções para movê-las</li>
                <li><b>Reordenar seções:</b> Arraste seções para reorganizar a ordem das abas</li>
                <li><b>Feedback visual:</b> Indicadores mostram onde o item será inserido</li>
            </ul>
            <h3>Atalhos de Teclado:</h3>
            <ul>
                <li><b>Ctrl+F:</b> Focar no campo de busca</li>
                <li><b>Ctrl+N:</b> Adicionar nova resposta</li>
                <li><b>Ctrl+S:</b> Salvar manualmente</li>
                <li><b>Ctrl+D:</b> Duplicar resposta selecionada</li>
                <li><b>Ctrl+Shift+N:</b> Nova seção</li>
                <li><b>Ctrl+1-9:</b> Alternar entre seções</li>
                <li><b>Delete:</b> Remover item selecionado</li>
                <li><b>F2:</b> Editar item selecionado</li>
                <li><b>Ctrl+↑:</b> Mover resposta selecionada para cima</li>
                <li><b>Ctrl+↓:</b> Mover resposta selecionada para baixo</li>
                <li><b>ESC:</b> Minimizar para a bola flutuante</li>
            </ul>
            <h3>Novidades:</h3>
            <ul>
                <li>Design moderno e intuitivo</li>
                <li>Drag and drop livre e intuitivo</li>
                <li>Mover respostas entre seções</li>
                <li>Reordenar seções livremente</li>
                <li>Feedback visual aprimorado</li>
                <li>Sistema de estatísticas de uso</li>
                <li>Temas claro e escuro</li>
                <li>Configurações personalizáveis</li>
                <li>Backup automático</li>
                <li>Ordenação por diferentes critérios</li>
                <li>Importação e exportação de dados</li>
            </ul>
            <p><b>Oferecimento <a href="https://github.com/PabloBernar">github.com/PabloBernar</a><br>de Pablo p/Bianca s2.</b></p>
        """)
        close_btn = QPushButton("Fechar")
        close_btn.clicked.connect(self.close)
        layout.addWidget(text_browser)
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
        self.is_dragging = False

    def set_dragging(self, dragging: bool):
        self.is_dragging = dragging
        self.setProperty("dragging", dragging)
        self.style().unpolish(self)
        self.style().polish(self)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if not (event.buttons() & Qt.LeftButton) or not self.drag_start_position:
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
            
        self.is_dragging = True
        self.set_dragging(True)
        self.setCursor(Qt.ClosedHandCursor)
        
        # Notificar o main_window sobre o início do drag
        if hasattr(self.parent().parent().parent(), 'start_drag_operation'):
            self.parent().parent().parent().start_drag_operation()
        
        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(f"SECTION:{self.text()}")
        
        # Criar pixmap com efeito visual
        pixmap = QPixmap(self.size())
        pixmap.fill(Qt.transparent)
        self.render(pixmap)
        
        # Adicionar efeito de transparência
        transparent_pixmap = QPixmap(pixmap.size())
        transparent_pixmap.fill(Qt.transparent)
        painter = QPainter(transparent_pixmap)
        painter.setOpacity(0.7)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()
        
        drag.setPixmap(transparent_pixmap)
        drag.setHotSpot(event.pos())
        drag.setMimeData(mime_data)
        
        result = drag.exec_(Qt.MoveAction)
        
        # Notificar o main_window sobre o fim do drag
        parent = self.parent()
        if parent and hasattr(parent.parent(), 'parent') and parent.parent().parent():
            main_window = parent.parent().parent()
            if hasattr(main_window, 'end_drag_operation'):
                main_window.end_drag_operation()
        
        self.is_dragging = False
        self.set_dragging(False)
        self.setCursor(Qt.OpenHandCursor)

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.is_dragging = False
        self.set_dragging(False)
        self.setCursor(Qt.OpenHandCursor)
        super().mouseReleaseEvent(event)

class EnhancedDraggableResponseWidget(QWidget):
    """Versão melhorada com melhor feedback visual e funcionalidades"""
    
    def __init__(self, response_data, main_window):
        super().__init__()
        self.response_data = response_data
        self.main_window = main_window
        self.drag_start_position = None
        self.setCursor(Qt.ArrowCursor)
        self.is_selected = False
        self.is_dragging = False
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(8)
        
        # Botões de seta modernizados
        self.up_arrow_btn = QPushButton("▲")
        self.up_arrow_btn.setObjectName("arrowButton")
        self.up_arrow_btn.setToolTip("Mover para cima")
        self.up_arrow_btn.setFixedSize(28, 28)
        self.up_arrow_btn.clicked.connect(self.move_up)
        
        self.down_arrow_btn = QPushButton("▼")
        self.down_arrow_btn.setObjectName("arrowButton")
        self.down_arrow_btn.setToolTip("Mover para baixo")
        self.down_arrow_btn.setFixedSize(28, 28)
        self.down_arrow_btn.clicked.connect(self.move_down)
        
        # Botão principal da resposta
        self.response_btn = QPushButton(self.response_data["texto"])
        self.response_btn.setObjectName("responseButton")
        
        # Tooltip com informações adicionais
        tooltip_text = f"Texto: {self.response_data['texto']}\n"
        tooltip_text += f"Criado: {self.response_data.get('data', 'N/A')}\n"
        usage_count = self.main_window.stats_manager.stats["response_usage"].get(
            self.response_data["texto"], 0)
        tooltip_text += f"Usado: {usage_count}x\n"
        tooltip_text += "Clique para copiar | Arraste para reordenar ou mover entre seções"
        self.response_btn.setToolTip(tooltip_text)
        
        self.response_btn.clicked.connect(self.on_copy_clicked)
        self.response_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        # Botão de menu modernizado
        self.menu_btn = QPushButton("⋯")
        self.menu_btn.setObjectName("menuButton")
        self.menu_btn.setToolTip("Opções")
        self.menu_btn.setFixedSize(32, 32)
        
        menu = QMenu(self)
        edit_action = menu.addAction("✏️ Editar (F2)")
        edit_action.triggered.connect(self.on_edit_clicked)
        
        duplicate_action = menu.addAction("📋 Duplicar (Ctrl+D)")
        duplicate_action.triggered.connect(self.on_duplicate_clicked)
        
        remove_action = menu.addAction("🗑️ Remover (Del)")
        remove_action.triggered.connect(self.on_remove_clicked)
        
        menu.addSeparator()
        
        stats_action = menu.addAction(f"📊 Usado {usage_count}x")
        stats_action.setEnabled(False)
        
        self.menu_btn.setMenu(menu)
        
        layout.addWidget(self.up_arrow_btn)
        layout.addWidget(self.down_arrow_btn)
        layout.addWidget(self.response_btn)
        layout.addWidget(self.menu_btn)
        
        # Estilo para seleção - removido para usar estilos globais do tema
        # self.setStyleSheet("""
        #     EnhancedDraggableResponseWidget[selected="true"] {
        #         background-color: rgba(99, 102, 241, 0.1);
        #         border: 1px solid #6366f1;
        #         border-radius: 8px;
        #     }
        #     EnhancedDraggableResponseWidget[dragging="true"] {
        #         background-color: rgba(99, 102, 241, 0.2);
        #         border: 2px solid #6366f1;
        #         border-radius: 8px;
        #         opacity: 0.8;
        #     }
        # """)

    def move_up(self):
        """Move a resposta para cima na lista"""
        self.main_window.move_response_up(self.response_data["texto"])

    def move_down(self):
        """Move a resposta para baixo na lista"""
        self.main_window.move_response_down(self.response_data["texto"])

    def update_arrow_buttons(self, is_first=False, is_last=False):
        """Atualiza o estado dos botões de seta"""
        self.up_arrow_btn.setEnabled(not is_first)
        self.down_arrow_btn.setEnabled(not is_last)

    def set_selected(self, selected: bool):
        self.is_selected = selected
        self.setProperty("selected", selected)
        self.style().unpolish(self)
        self.style().polish(self)

    def set_dragging(self, dragging: bool):
        self.is_dragging = dragging
        self.setProperty("dragging", dragging)
        self.style().unpolish(self)
        self.style().polish(self)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()
            # Notificar o main_window sobre a seleção
            self.main_window.set_selected_response(self)
        event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if not (event.buttons() & Qt.LeftButton) or not self.drag_start_position:
            return
        
        # Reduzir a distância mínima para iniciar o drag
        min_distance = max(5, QApplication.startDragDistance() // 2)
        if (event.pos() - self.drag_start_position).manhattanLength() < min_distance:
            return
            
        self.setCursor(Qt.ClosedHandCursor)
        self.set_dragging(True)
        
        # Notificar o main_window sobre o início do drag
        if hasattr(self.main_window, 'start_drag_operation'):
            self.main_window.start_drag_operation()
        
        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(f"RESPONSE:{self.response_data['texto']}")
        
        # Criar pixmap com efeito visual
        pixmap = QPixmap(self.size())
        pixmap.fill(Qt.transparent)
        self.render(pixmap)
        
        # Adicionar efeito de transparência
        transparent_pixmap = QPixmap(pixmap.size())
        transparent_pixmap.fill(Qt.transparent)
        painter = QPainter(transparent_pixmap)
        painter.setOpacity(0.7)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()
        
        drag.setPixmap(transparent_pixmap)
        drag.setHotSpot(event.pos())
        drag.setMimeData(mime_data)
        
        result = drag.exec_(Qt.MoveAction)
        
        # Notificar o main_window sobre o fim do drag
        if hasattr(self.main_window, 'end_drag_operation'):
            self.main_window.end_drag_operation()
        
        self.set_dragging(False)
        self.setCursor(Qt.OpenHandCursor)

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.set_dragging(False)
        self.setCursor(Qt.OpenHandCursor)
        
        # Notificar o main_window sobre o fim do drag se necessário
        if hasattr(self.main_window, 'end_drag_operation'):
            self.main_window.end_drag_operation()
        
        super().mouseReleaseEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.on_remove_clicked()
        elif event.key() == Qt.Key_F2:
            self.on_edit_clicked()
        elif event.matches(QKeySequence.Copy):
            self.on_copy_clicked()
        else:
            super().keyPressEvent(event)

    def on_copy_clicked(self):
        self.main_window.copy_to_clipboard(self.response_data["texto"])

    def on_edit_clicked(self):
        self.main_window.edit_response(self.response_data["texto"])

    def on_duplicate_clicked(self):
        self.main_window.duplicate_response(self.response_data["texto"])

    def on_remove_clicked(self):
        self.main_window.remove_response(self.response_data["texto"])

class RespostaRapidaApp(QMainWindow, FaderWidget):
    def __init__(self):
        QMainWindow.__init__(self)
        FaderWidget.__init__(self)

        CONFIG.APP_DATA_DIR.mkdir(parents=True, exist_ok=True)
        
        # Managers
        self.config_manager = ConfigManager(CONFIG.CONFIG_FILE)
        self.stats_manager = StatsManager(CONFIG.STATS_FILE)
        self.data_manager = DataManager(CONFIG.DATA_FILE)
        
        self.current_section = list(self.data_manager.data.keys())[0] if self.data_manager.data else "Geral"
        self.search_filter = ""
        self.drag_position = None
        self.selected_response_widget = None
        self.drop_indicator = None
        self.section_drop_indicator = None
        self.is_dragging = False

        # Configurar tema
        self.current_theme = THEMES[self.config_manager.get("theme", "light")]

        # Configurar o ícone da janela
        self.setWindowIcon(QIcon(resource_path('fctbi.ico')))

        self.setup_ui()
        self.setup_connections()
        self.setup_tray_icon()
        self.setup_shortcuts()
        self.setup_timers()
        
        self.floating_button = FloatingButton(self.show_window)
        # Garantir que a bola flutuante seja sempre visível quando necessário
        self.floating_button.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        
        # Posicionar bola flutuante
        self._position_floating_button()

        # Restaurar posição e tamanho da janela
        window_pos = self.config_manager.get("window_position")
        window_size = self.config_manager.get("window_size", [CONFIG.WINDOW_WIDTH, CONFIG.WINDOW_HEIGHT])
        
        if window_pos:
            self.move(window_pos[0], window_pos[1])
        self.resize(window_size[0], window_size[1])

        self.update_sections_ui()
        self.update_responses_ui()

    def setup_timers(self):
        """Configura timers para backup automático e verificação da bola flutuante"""
        # Timer para backup automático
        if self.config_manager.get("auto_backup"):
            self.backup_timer = QTimer()
            self.backup_timer.timeout.connect(self.data_manager.save)
            interval = self.config_manager.get("backup_interval", 60) * 60000  # converter para ms
            self.backup_timer.start(interval)
        
        # Timer para verificar visibilidade da bola flutuante
        self.floating_check_timer = QTimer()
        self.floating_check_timer.timeout.connect(self._update_floating_button_visibility)
        self.floating_check_timer.start(1000)  # Verificar a cada segundo

    def _update_floating_button_visibility(self):
        """Atualiza visibilidade da bola flutuante baseado no estado da janela principal"""
        main_visible = self.isVisible()
        floating_visible = self.floating_button.isVisible()
        
        if not main_visible and not floating_visible:
            self.floating_button.show()
            self.floating_button.raise_()
        elif main_visible and floating_visible:
            self.floating_button.hide()

    def set_selected_response(self, widget):
        """Define o widget de resposta selecionado"""
        if self.selected_response_widget:
            self.selected_response_widget.set_selected(False)
        
        self.selected_response_widget = widget
        if widget:
            widget.set_selected(True)

    def start_drag_operation(self):
        """Inicia operação de drag"""
        self.is_dragging = True
        if not self.drop_indicator:
            self.drop_indicator = DragDropIndicator(self.responses_widget)
        if not self.section_drop_indicator:
            self.section_drop_indicator = DragDropIndicator(self.sections_widget)

    def end_drag_operation(self):
        """Finaliza operação de drag"""
        self.is_dragging = False
        if self.drop_indicator:
            self.drop_indicator.hide()
        if self.section_drop_indicator:
            self.section_drop_indicator.hide()

    def show_drop_indicator(self, position: int):
        """Mostra indicador de drop na posição especificada"""
        if not self.drop_indicator or not self.is_dragging:
            return
            
        # Permitir posição 0 mesmo quando não há widgets
        if position < 0:
            self.drop_indicator.hide()
            return
            
        # Se a posição é maior que o número de widgets, inserir no final
        if position > self.responses_layout.count():
            position = self.responses_layout.count()
            
        # Posicionar o indicador
        if position == 0:
            y = 0
        else:
            widget = self.responses_layout.itemAt(position - 1).widget()
            if widget:
                widget_rect = widget.geometry()
                y = widget_rect.y() + widget_rect.height()
            else:
                y = 0
                
        self.drop_indicator.setGeometry(0, y, self.responses_widget.width(), 2)
        self.drop_indicator.show()
        self.drop_indicator.raise_()

    def show_section_drop_indicator(self, position: int):
        """Mostra indicador de drop para seções na posição especificada"""
        if not self.section_drop_indicator or not self.is_dragging:
            return
            
        if position < 0 or position >= self.sections_layout.count():
            self.section_drop_indicator.hide()
            return
            
        # Posicionar o indicador
        if position == 0:
            x = 0
        else:
            widget = self.sections_layout.itemAt(position - 1).widget()
            if widget:
                x = widget.x() + widget.width()
            else:
                x = 0
                
        self.section_drop_indicator.setGeometry(x, 0, 2, self.sections_widget.height())
        self.section_drop_indicator.show()
        self.section_drop_indicator.raise_()

    def setup_ui(self):
        self.setWindowTitle('FCTBI - Respostas Rápidas')
        self.setMinimumSize(CONFIG.MIN_WINDOW_WIDTH, CONFIG.MIN_WINDOW_HEIGHT)
        self.resize(CONFIG.WINDOW_WIDTH, CONFIG.WINDOW_HEIGHT)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Barra de título moderna
        self.title_bar = QWidget()
        self.title_bar.setObjectName("titleBar")
        self.title_bar.setFixedHeight(50)
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(18, 0, 18, 0)
        
        title_label = QLabel("🚀 FCTBI")
        title_label.setObjectName("titleLabel")
        
        # Botões da barra de título com ícones modernos
        btn_stats = QPushButton("📊")
        btn_stats.setObjectName("titleButton")
        btn_stats.setFixedSize(32, 32)
        btn_stats.setToolTip("Estatísticas de uso")
        
        btn_settings = QPushButton("⚙️")
        btn_settings.setObjectName("titleButton")
        btn_settings.setFixedSize(32, 32)
        btn_settings.setToolTip("Configurações")
        
        btn_help = QPushButton("❓")
        btn_help.setObjectName("titleButton")
        btn_help.setFixedSize(32, 32)
        btn_help.setToolTip("Ajuda e manual")
        
        btn_minimize = QPushButton("➖")
        btn_minimize.setObjectName("titleButton")
        btn_minimize.setFixedSize(32, 32)
        btn_minimize.setToolTip("Minimizar para bola flutuante")
        
        btn_close = QPushButton("✖")
        btn_close.setObjectName("titleButton")
        btn_close.setFixedSize(32, 32)
        btn_close.setToolTip("Fechar aplicação")
        
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(btn_stats)
        title_layout.addWidget(btn_settings)
        title_layout.addWidget(btn_help)
        title_layout.addWidget(btn_minimize)
        title_layout.addWidget(btn_close)
        
        main_layout.addWidget(self.title_bar)
        
        # Conectar botões
        btn_stats.clicked.connect(self.show_stats)
        btn_settings.clicked.connect(self.show_settings)
        btn_help.clicked.connect(self.show_help)
        btn_minimize.clicked.connect(self.minimize_window)
        btn_close.clicked.connect(self.close_window)
        
        # Barra de busca moderna
        search_bar = QWidget()
        search_bar.setObjectName("searchBar")
        search_bar.setFixedHeight(65)
        search_layout = QHBoxLayout(search_bar)
        search_layout.setContentsMargins(18, 8, 18, 8)
        
        self.search_input = QLineEdit()
        self.search_input.setObjectName("searchInput")
        self.search_input.setPlaceholderText("🔍 Buscar respostas... (Ctrl+F)")
        
        # Botão limpar busca
        self.clear_search_btn = QPushButton("✕")
        self.clear_search_btn.setObjectName("clearSearchButton")
        self.clear_search_btn.setFixedSize(28, 28)
        self.clear_search_btn.setToolTip("Limpar busca")
        self.clear_search_btn.clicked.connect(self.clear_search)
        self.clear_search_btn.setVisible(False)
        
        # Combo de ordenação
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["📅 Criação", "🔤 Alfabética", "⭐ Mais Usadas"])
        self.sort_combo.setCurrentIndex(0)
        self.sort_combo.setToolTip("Ordenar respostas por...")
        self.sort_combo.currentTextChanged.connect(self.sort_responses)
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.clear_search_btn)
        search_layout.addWidget(self.sort_combo)
        
        main_layout.addWidget(search_bar)
        
        # Container de seções moderno
        self.sections_container = QWidget()
        self.sections_container.setObjectName("sectionsContainer")
        self.sections_container.setFixedHeight(70)
        sections_layout = QHBoxLayout(self.sections_container)
        sections_layout.setContentsMargins(12, 8, 12, 8)
        
        self.sections_scroll = QScrollArea()
        self.sections_scroll.setWidgetResizable(True)
        self.sections_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.sections_widget = QWidget()
        self.sections_widget.setAcceptDrops(True)
        self.sections_layout = QHBoxLayout(self.sections_widget)
        self.sections_layout.setAlignment(Qt.AlignLeft)
        self.sections_layout.setContentsMargins(0, 0, 0, 0)
        
        self.sections_scroll.setWidget(self.sections_widget)
        
        # Botões de ação com ícones modernos
        btn_import = QPushButton("📁")
        btn_import.setObjectName("importButton")
        btn_import.setFixedSize(32, 32)
        btn_import.setToolTip("Importar dados de arquivo")
        
        btn_export = QPushButton("💾")
        btn_export.setObjectName("exportButton")
        btn_export.setFixedSize(32, 32)
        btn_export.setToolTip("Exportar dados para arquivo")
        
        btn_add_section = QPushButton("➕")
        btn_add_section.setObjectName("addSectionButton")
        btn_add_section.setFixedSize(32, 32)
        btn_add_section.setToolTip("Adicionar nova seção (Ctrl+Shift+N)")
        
        sections_layout.addWidget(self.sections_scroll)
        sections_layout.addWidget(btn_import)
        sections_layout.addWidget(btn_export)
        sections_layout.addWidget(btn_add_section)
        
        main_layout.addWidget(self.sections_container)
        
        btn_add_section.clicked.connect(self.add_section)
        btn_import.clicked.connect(self.import_data)
        btn_export.clicked.connect(self.export_data)
        
        # Container de conteúdo moderno
        self.content_container = QWidget()
        self.content_container.setObjectName("contentContainer")
        content_layout = QVBoxLayout(self.content_container)
        content_layout.setContentsMargins(18, 8, 18, 18)
        
        # Info da seção atual
        self.section_info = QLabel()
        self.section_info.setObjectName("sectionInfo")
        self.section_info.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(self.section_info)
        
        # Área de respostas
        self.responses_scroll = QScrollArea()
        self.responses_scroll.setWidgetResizable(True)
        
        self.responses_widget = QWidget()
        self.responses_widget.setAcceptDrops(True)
        self.responses_layout = QVBoxLayout(self.responses_widget)
        self.responses_layout.setAlignment(Qt.AlignTop)
        self.responses_layout.setContentsMargins(0, 0, 8, 0)
        self.responses_layout.setSpacing(6)
        
        self.responses_scroll.setWidget(self.responses_widget)
        
        # Botão adicionar resposta moderno
        self.btn_add_response = QPushButton("➕ Adicionar Resposta (Ctrl+N)")
        self.btn_add_response.setObjectName("addButton")
        
        content_layout.addWidget(self.responses_scroll)
        content_layout.addWidget(self.btn_add_response)
        
        main_layout.addWidget(self.content_container)
        
        self.btn_add_response.clicked.connect(self.add_response)
        
        self.apply_styles()

    def apply_styles(self):
        theme = self.current_theme
        stylesheet = f"""
            #centralWidget {{
                background-color: {theme['BACKGROUND']};
                border: 3px solid {theme['PRIMARY_COLOR']};
                border-radius: 16px;
            }}
            #titleBar {{ 
                background-color: transparent; 
                border-bottom: 1px solid {theme['BORDER_COLOR']};
            }}
            #titleLabel {{
                font-family: "{CONFIG.APP_FONT_NAME}";
                color: {theme['PRIMARY_COLOR']};
                font-size: 18px;
                font-weight: bold;
                letter-spacing: 0.5px;
            }}
            #titleButton {{
                background-color: transparent;
                color: {theme['PRIMARY_COLOR']};
                border: none;
                font-size: 16px;
                font-weight: bold;
                min-width: 32px;
                min-height: 32px;
                border-radius: 8px;
            }}
            #titleButton:hover {{ 
                background-color: {theme['HOVER_BG']}; 
            }}
            #searchBar {{ 
                background-color: transparent; 
                padding: 8px 0;
            }}
            #searchInput {{
                border: 2px solid {theme['BORDER_COLOR']};
                border-radius: 12px;
                padding: 10px 16px;
                font-size: 13px;
                background-color: {theme['BACKGROUND']};
                color: {theme['TEXT_COLOR']};
                font-family: "{CONFIG.APP_FONT_NAME}";
            }}
            #searchInput:focus {{ 
                border-color: {theme['PRIMARY_COLOR']}; 
            }}
            #clearSearchButton {{
                background-color: {theme['SECONDARY_COLOR']};
                color: {theme['TEXT_COLOR']};
                border: none;
                border-radius: 10px;
                font-size: 12px;
                font-weight: bold;
            }}
            #clearSearchButton:hover {{
                background-color: {theme['PRIMARY_COLOR']};
                color: white;
            }}
            QComboBox {{
                border: 2px solid {theme['BORDER_COLOR']};
                border-radius: 10px;
                padding: 8px 12px;
                background-color: {theme['BACKGROUND']};
                color: {theme['TEXT_COLOR']};
                min-width: 110px;
                font-family: "{CONFIG.APP_FONT_NAME}";
                font-size: 12px;
            }}
            QComboBox:hover {{
                border-color: {theme['PRIMARY_COLOR']};
            }}
            QComboBox:focus {{
                border-color: {theme['PRIMARY_COLOR']};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 20px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid {theme['TEXT_COLOR']};
                margin-right: 8px;
            }}
            #sectionsContainer {{ 
                background-color: transparent; 
                border-bottom: 1px solid {theme['BORDER_COLOR']}; 
                padding: 8px 0;
            }}
            #addSectionButton, #importButton, #exportButton {{
                background-color: {theme['PRIMARY_COLOR']};
                color: white;
                border: none;
                border-radius: 12px;
                font-weight: bold;
                font-size: 13px;
                min-width: 32px;
                min-height: 32px;
            }}
            #addSectionButton:hover, #importButton:hover, #exportButton:hover {{ 
                background-color: {theme['ACCENT_COLOR']}; 
            }}
            #addSectionButton {{
                color: white !important;
            }}
            QPushButton#sectionButton {{
                background-color: {theme['SECONDARY_COLOR']};
                color: {theme['TEXT_COLOR']};
                border: 2px solid {theme['BORDER_COLOR']};
                padding: 8px 14px;
                border-radius: 12px;
                font-size: 12px;
                font-family: "{CONFIG.APP_FONT_NAME}";
                min-width: 70px;
            }}
            QPushButton#sectionButton:hover {{ 
                background-color: {theme['HOVER_BG']}; 
                border-color: {theme['PRIMARY_COLOR']};
            }}
            QPushButton#sectionButton:checked {{
                background-color: {theme['PRIMARY_COLOR']};
                color: white;
                font-weight: bold;
                border-color: {theme['PRIMARY_COLOR']};
            }}
            QPushButton#sectionButton[dragging="true"] {{
                background-color: {theme['ACCENT_COLOR']};
                color: white;
                border: 2px solid {theme['PRIMARY_COLOR']};
            }}
            #contentContainer {{ 
                background-color: transparent; 
                padding: 8px 0;
            }}
            #sectionInfo {{
                color: {theme['TEXT_COLOR']};
                font-size: 12px;
                font-family: "{CONFIG.APP_FONT_NAME}";
                margin: 8px 0;
                opacity: 0.8;
                font-weight: 500;
            }}
            QPushButton#responseButton {{
                background-color: {theme['PRIMARY_COLOR']};
                color: white;
                border: none;
                padding: 14px 16px;
                text-align: left;
                border-radius: 10px;
                font-size: 13px;
                font-family: "{CONFIG.APP_FONT_NAME}";
                min-height: 24px;
            }}
            QPushButton#responseButton:hover {{ 
                background-color: {theme['ACCENT_COLOR']}; 
            }}
            QPushButton#menuButton {{
                background-color: {theme['PRIMARY_COLOR']};
                color: white;
                border: none;
                border-radius: 10px;
                min-width: 32px;
                max-width: 32px;
                font-weight: bold;
                font-size: 16px;
            }}
            QPushButton#menuButton:hover {{ 
                background-color: {theme['ACCENT_COLOR']}; 
            }}
            QPushButton#menuButton::menu-indicator {{ 
                image: none; 
            }}
            QPushButton#arrowButton {{
                background-color: {theme['SECONDARY_COLOR']};
                color: {theme['TEXT_COLOR']};
                border: 2px solid {theme['BORDER_COLOR']};
                border-radius: 10px;
                font-weight: bold;
                font-size: 12px;
            }}
            QPushButton#arrowButton:hover {{
                background-color: {theme['PRIMARY_COLOR']};
                color: white;
                border-color: {theme['PRIMARY_COLOR']};
            }}
            QPushButton#arrowButton:disabled {{
                background-color: {theme['BORDER_COLOR']};
                color: {theme['TEXT_COLOR']};
                opacity: 0.4;
                border-color: {theme['BORDER_COLOR']};
            }}
            #addButton {{
                background-color: {theme['PRIMARY_COLOR']};
                color: white !important;
                font-weight: bold;
                border: none;
                padding: 14px;
                border-radius: 10px;
                font-size: 14px;
                font-family: "{CONFIG.APP_FONT_NAME}";
            }}
            #addButton:hover {{ 
                background-color: {theme['ACCENT_COLOR']}; 
            }}
            QScrollBar:vertical {{
                border: none;
                background: {theme['SECONDARY_COLOR']};
                width: 10px;
                margin: 0px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical {{
                background: {theme['BORDER_COLOR']};
                min-height: 30px;
                border-radius: 5px;
                margin: 2px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {theme['PRIMARY_COLOR']};
            }}
            QScrollBar:horizontal {{
                border: none;
                background: {theme['SECONDARY_COLOR']};
                height: 10px;
                margin: 0px;
                border-radius: 5px;
            }}
            QScrollBar::handle:horizontal {{
                background: {theme['BORDER_COLOR']};
                min-width: 30px;
                border-radius: 5px;
                margin: 2px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background: {theme['PRIMARY_COLOR']};
            }}
            #emptyLabel {{
                color: {theme['TEXT_COLOR']};
                font-size: 13px;
                font-family: "{CONFIG.APP_FONT_NAME}";
                font-style: italic;
                opacity: 0.6;
                text-align: center;
                padding: 20px;
            }}
            QMenu {{
                background-color: {theme['CARD_BG']};
                color: {theme['TEXT_COLOR']};
                border: 1px solid {theme['BORDER_COLOR']};
                border-radius: 8px;
                padding: 4px;
                font-family: "{CONFIG.APP_FONT_NAME}";
                font-size: 12px;
            }}
            QMenu::item {{
                padding: 8px 12px;
                border-radius: 4px;
                margin: 1px;
            }}
            QMenu::item:selected {{
                background-color: {theme['PRIMARY_COLOR']};
                color: white;
            }}
            QGroupBox {{
                font-family: "{CONFIG.APP_FONT_NAME}";
                font-weight: bold;
                font-size: 13px;
                color: {theme['PRIMARY_COLOR']};
                border: 2px solid {theme['BORDER_COLOR']};
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
            }}
            QDialog {{
                background-color: {theme['BACKGROUND']};
                border: 2px solid {theme['BORDER_COLOR']};
                border-radius: 12px;
            }}
            QLabel {{
                font-family: "{CONFIG.APP_FONT_NAME}";
                color: {theme['TEXT_COLOR']};
            }}
            QLineEdit, QTextEdit {{
                font-family: "{CONFIG.APP_FONT_NAME}";
                border: 2px solid {theme['BORDER_COLOR']};
                border-radius: 8px;
                padding: 8px;
                background-color: {theme['BACKGROUND']};
                color: {theme['TEXT_COLOR']};
            }}
            QLineEdit:focus, QTextEdit:focus {{
                border-color: {theme['PRIMARY_COLOR']};
            }}
            EnhancedDraggableResponseWidget {{
                background-color: {theme['CARD_BG']};
                border: 1px solid {theme['BORDER_COLOR']};
                border-radius: 8px;
                margin: 2px 0;
            }}
            EnhancedDraggableResponseWidget:hover {{
                background-color: {theme['HOVER_BG']};
                border-color: {theme['PRIMARY_COLOR']};
            }}
            EnhancedDraggableResponseWidget[selected="true"] {{
                background-color: {theme['PRIMARY_COLOR']}20;
                border: 1px solid {theme['PRIMARY_COLOR']};
                border-radius: 8px;
            }}
            EnhancedDraggableResponseWidget[dragging="true"] {{
                background-color: {theme['PRIMARY_COLOR']}40;
                border: 2px solid {theme['PRIMARY_COLOR']};
                border-radius: 8px;
                opacity: 0.8;
            }}
        """
        self.setStyleSheet(stylesheet)

    def setup_connections(self):
        self.search_input.textChanged.connect(self.filter_responses)
        self.search_input.textChanged.connect(self.toggle_clear_button)
        
        # Drag and drop para seções
        self.sections_widget.dragEnterEvent = self.sections_drag_enter_event
        self.sections_widget.dragMoveEvent = self.sections_drag_move_event
        self.sections_widget.dropEvent = self.sections_drop_event
        
        # Drag and drop para respostas - versão melhorada
        self.responses_widget.dragEnterEvent = self.responses_drag_enter_event
        self.responses_widget.dragMoveEvent = self.responses_drag_move_event_enhanced
        self.responses_widget.dropEvent = self.responses_drop_event_enhanced

    def sections_drag_enter_event(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def sections_drag_move_event(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
            
            # Mostrar indicador de drop para seções
            pos = event.pos()
            drop_position = self.calculate_section_drop_position(pos)
            self.show_section_drop_indicator(drop_position)

    def sections_drop_event(self, event):
        mime_text = event.mimeData().text()
        pos = event.pos()
        
        if mime_text.startswith("SECTION:"):
            # Reordenar seções
            section_name = mime_text[8:]
            drop_position = self.calculate_section_drop_position(pos)
            self.reorder_section(section_name, drop_position)
        elif mime_text.startswith("RESPONSE:"):
            # Mover resposta para nova seção
            response_text = mime_text[9:]
            target_section = self.get_section_at_position(pos)
            if target_section and target_section != self.current_section:
                self.move_response_to_section(response_text, target_section)
        
        # Esconder indicador
        if self.section_drop_indicator:
            self.section_drop_indicator.hide()
        
        event.acceptProposedAction()

    def responses_drag_enter_event(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def responses_drag_move_event_enhanced(self, event):
        if not event.mimeData().hasText():
            return
            
        event.acceptProposedAction()
        
        # Calcular posição de inserção
        pos = event.pos()
        drop_position = self.calculate_drop_position(pos)
        self.show_drop_indicator(drop_position)
        
        # Scroll automático
        self._auto_scroll_during_drag(pos)

    def responses_drop_event_enhanced(self, event):
        mime_text = event.mimeData().text()
        pos = event.pos()
        
        if mime_text.startswith("RESPONSE:"):
            response_text = mime_text[9:]
            drop_position = self.calculate_drop_position(pos)
            
            # Reordenar respostas na seção atual
            self.reorder_response(response_text, drop_position)
        elif mime_text.startswith("SECTION:"):
            # Mover seção para dentro da área de respostas (não permitido)
            pass
        
        # Esconder indicador
        if self.drop_indicator:
            self.drop_indicator.hide()
        
        event.acceptProposedAction()

    def _calculate_drop_position(self, pos: QPoint, layout, is_horizontal: bool = False) -> int:
        """
        Calcula a posição onde o item será inserido
        
        Args:
            pos: Posição do cursor
            layout: Layout a ser verificado
            is_horizontal: Se True, calcula posição horizontal (para seções)
            
        Returns:
            Posição de inserção
        """
        if layout.count() == 0:
            return 0
            
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                widget_rect = widget.geometry()
                
                if is_horizontal:
                    # Para seções (horizontal)
                    if pos.x() < widget_rect.x() + widget_rect.width() // 2:
                        return i
                else:
                    # Para respostas (vertical)
                    if pos.y() < widget_rect.y() + widget_rect.height() // 2:
                        return i
        
        return layout.count()

    def _get_widget_at_position(self, pos: QPoint, layout) -> Optional[str]:
        """
        Retorna o texto do widget na posição especificada
        
        Args:
            pos: Posição do cursor
            layout: Layout a ser verificado
            
        Returns:
            Texto do widget ou None
        """
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                if widget.geometry().contains(pos):
                    return widget.text()
        return None

    def _reorder_items(self, item_name: str, new_position: int, 
                      items_list: List, save_func) -> bool:
        """
        Reordena itens em uma lista
        
        Args:
            item_name: Nome do item a ser movido
            new_position: Nova posição
            items_list: Lista de itens
            save_func: Função para salvar mudanças
            
        Returns:
            True se reordenou com sucesso
        """
        try:
            current_index = next(i for i, item in enumerate(items_list) 
                               if item["texto"] == item_name)
        except StopIteration:
            return False
            
        if current_index == new_position:
            return True
            
        # Remover da posição atual
        item = items_list.pop(current_index)
        
        # Ajustar nova posição se necessário
        if current_index < new_position:
            new_position -= 1
        
        # Inserir na nova posição
        if new_position >= len(items_list):
            items_list.append(item)
        else:
            items_list.insert(new_position, item)
            
        return save_func()

    def calculate_section_drop_position(self, pos: QPoint) -> int:
        """Calcula a posição onde a seção será inserida"""
        return self._calculate_drop_position(pos, self.sections_layout, is_horizontal=True)

    def get_section_at_position(self, pos: QPoint) -> Optional[str]:
        """Retorna o nome da seção na posição especificada"""
        return self._get_widget_at_position(pos, self.sections_layout)

    def reorder_section(self, section_name: str, new_position: int) -> None:
        """Reordena uma seção para nova posição"""
        sections = list(self.data_manager.data.keys())
        
        if self._reorder_items(section_name, new_position, sections, 
                             lambda: self.data_manager.reorder_sections(sections)):
            self.update_sections_ui()

    def move_response_to_section(self, response_text: str, target_section: str) -> None:
        """Move uma resposta de uma seção para outra"""
        current_responses = self.data_manager.data[self.current_section]
        
        # Encontrar a resposta na seção atual
        response_data = next((item for item in current_responses 
                            if item["texto"] == response_text), None)
        
        if response_data:
            # Remover da seção atual e adicionar na nova
            if (self.data_manager.remove_response(self.current_section, response_text) and
                self.data_manager.add_response(target_section, response_text)):
                self.update_sections_ui()
                self.update_responses_ui()

    def calculate_drop_position(self, pos: QPoint) -> int:
        """Calcula a posição onde o item será inserido"""
        return self._calculate_drop_position(pos, self.responses_layout)

    def _auto_scroll_during_drag(self, pos: QPoint) -> None:
        """Scroll automático durante drag"""
        scroll_area = self.responses_scroll
        viewport = scroll_area.viewport()
        viewport_rect = viewport.rect()
        
        scroll_margin = 30
        scroll_speed = 5
        
        if pos.y() < viewport_rect.top() + scroll_margin:
            # Scroll para cima
            scroll_area.verticalScrollBar().setValue(
                scroll_area.verticalScrollBar().value() - scroll_speed
            )
        elif pos.y() > viewport_rect.bottom() - scroll_margin:
            # Scroll para baixo
            scroll_area.verticalScrollBar().setValue(
                scroll_area.verticalScrollBar().value() + scroll_speed
            )

    def reorder_response(self, response_text: str, new_position: int) -> None:
        """Reordena uma resposta para nova posição"""
        current_responses = self.data_manager.data[self.current_section]
        
        if self._reorder_items(response_text, new_position, current_responses,
                             self.data_manager.save):
            self.update_responses_ui()

    def _move_response(self, response_text: str, direction: int) -> None:
        """
        Move uma resposta para cima ou baixo na lista
        
        Args:
            response_text: Texto da resposta a ser movida
            direction: 1 para baixo, -1 para cima
        """
        current_responses = self.data_manager.data[self.current_section]
        
        try:
            current_index = next(i for i, item in enumerate(current_responses) 
                               if item["texto"] == response_text)
        except StopIteration:
            return
            
        new_index = current_index + direction
        
        # Verificar limites
        if new_index < 0 or new_index >= len(current_responses):
            return
            
        # Trocar posições
        current_responses[current_index], current_responses[new_index] = \
            current_responses[new_index], current_responses[current_index]
        
        # Salvar e atualizar UI
        if self.data_manager.save():
            self.update_responses_ui()

    def move_response_up(self, response_text: str) -> None:
        """Move uma resposta para cima na lista"""
        self._move_response(response_text, -1)

    def move_response_down(self, response_text: str) -> None:
        """Move uma resposta para baixo na lista"""
        self._move_response(response_text, 1)

    def toggle_clear_button(self, text):
        """Mostra/esconde botão de limpar busca"""
        self.clear_search_btn.setVisible(bool(text))

    def clear_search(self):
        """Limpa o campo de busca"""
        self.search_input.clear()
        self.search_input.setFocus()

    def sort_responses(self, sort_text):
        """Ordena as respostas conforme critério selecionado"""
        sort_map = {
            "📅 Criação": "creation",
            "🔤 Alfabética": "alphabetical", 
            "⭐ Mais Usadas": "usage"
        }
        
        sort_by = sort_map.get(sort_text, "creation")
        if self.data_manager.sort_responses(
            self.current_section, 
            sort_by, 
            self.stats_manager.stats["response_usage"]
        ):
            self.update_responses_ui()

    def setup_shortcuts(self):
        # Atalhos existentes
        shortcut_search = QShortcut(QKeySequence("Ctrl+F"), self)
        shortcut_search.activated.connect(lambda: self.search_input.setFocus())
        
        shortcut_new = QShortcut(QKeySequence("Ctrl+N"), self)
        shortcut_new.activated.connect(self.add_response)
        
        shortcut_save = QShortcut(QKeySequence("Ctrl+S"), self)
        shortcut_save.activated.connect(self.data_manager.save)
        
        shortcut_minimize = QShortcut(QKeySequence("Esc"), self)
        shortcut_minimize.activated.connect(self.minimize_window)
        
        # Novos atalhos
        shortcut_new_section = QShortcut(QKeySequence("Ctrl+Shift+N"), self)
        shortcut_new_section.activated.connect(self.add_section)
        
        shortcut_duplicate = QShortcut(QKeySequence("Ctrl+D"), self)
        shortcut_duplicate.activated.connect(self.duplicate_selected_response)
        
        shortcut_delete = QShortcut(QKeySequence("Delete"), self)
        shortcut_delete.activated.connect(self.remove_selected_response)
        
        shortcut_edit = QShortcut(QKeySequence("F2"), self)
        shortcut_edit.activated.connect(self.edit_selected_response)
        
        # Atalhos para setas (mover respostas)
        shortcut_up = QShortcut(QKeySequence("Ctrl+Up"), self)
        shortcut_up.activated.connect(self.move_selected_response_up)
        
        shortcut_down = QShortcut(QKeySequence("Ctrl+Down"), self)
        shortcut_down.activated.connect(self.move_selected_response_down)
        
        # Atalhos para alternar seções (Ctrl+1 a Ctrl+9)
        for i in range(1, 10):
            shortcut = QShortcut(QKeySequence(f"Ctrl+{i}"), self)
            shortcut.activated.connect(lambda idx=i-1: self.select_section_by_index(idx))

    def select_section_by_index(self, index: int) -> None:
        """Seleciona seção pelo índice"""
        sections = list(self.data_manager.data.keys())
        if 0 <= index < len(sections):
            self.select_section(sections[index])

    def _execute_on_selected_response(self, action_func) -> None:
        """
        Executa uma ação na resposta selecionada
        
        Args:
            action_func: Função a ser executada com o texto da resposta
        """
        if self.selected_response_widget:
            action_func(self.selected_response_widget.response_data["texto"])

    def duplicate_selected_response(self) -> None:
        """Duplica a resposta selecionada"""
        self._execute_on_selected_response(self.duplicate_response)

    def remove_selected_response(self) -> None:
        """Remove a resposta selecionada"""
        self._execute_on_selected_response(self.remove_response)

    def edit_selected_response(self) -> None:
        """Edita a resposta selecionada"""
        self._execute_on_selected_response(self.edit_response)

    def move_selected_response_up(self) -> None:
        """Move a resposta selecionada para cima"""
        self._execute_on_selected_response(self.move_response_up)

    def move_selected_response_down(self) -> None:
        """Move a resposta selecionada para baixo"""
        self._execute_on_selected_response(self.move_response_down)

    def update_sections_ui(self):
        """Atualiza a interface das seções"""
        # Limpar seções existentes
        for i in reversed(range(self.sections_layout.count())):
            child = self.sections_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        # Adicionar seções
        for section_name in self.data_manager.data.keys():
            section_btn = DraggableSectionButton(section_name)
            section_btn.clicked.connect(lambda checked, name=section_name: self.select_section(name))
            section_btn.setContextMenuPolicy(Qt.CustomContextMenu)
            section_btn.customContextMenuRequested.connect(
                lambda pos, name=section_name: self.show_section_menu(name, pos)
            )
            
            if section_name == self.current_section:
                section_btn.setChecked(True)
            
            self.sections_layout.addWidget(section_btn)
        
        # Adicionar spacer
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.sections_layout.addWidget(spacer)
        
        # Se não há seções, mostrar mensagem
        if not self.data_manager.data:
            no_sections_label = QLabel("📁 Nenhuma seção criada")
            no_sections_label.setObjectName("emptyLabel")
            no_sections_label.setAlignment(Qt.AlignCenter)
            self.sections_layout.addWidget(no_sections_label)

    def update_responses_ui(self):
        """Atualiza a interface das respostas"""
        # Limpar respostas existentes
        for i in reversed(range(self.responses_layout.count())):
            child = self.responses_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        # Filtrar respostas se necessário
        responses = self.data_manager.data.get(self.current_section, [])
        if self.search_filter:
            filtered_responses = []
            for response in responses:
                if self.search_filter.lower() in response["texto"].lower():
                    filtered_responses.append(response)
            responses = filtered_responses
        
        # Adicionar respostas
        response_widgets = []
        for response_data in responses:
            response_widget = EnhancedDraggableResponseWidget(response_data, self)
            self.responses_layout.addWidget(response_widget)
            response_widgets.append(response_widget)
        
        # Configurar botões de seta
        for i, widget in enumerate(response_widgets):
            is_first = (i == 0)
            is_last = (i == len(response_widgets) - 1)
            widget.update_arrow_buttons(is_first, is_last)
        
        # Mostrar mensagem se não há respostas
        if not responses:
            empty_label = QLabel("📝 Nenhuma resposta encontrada\nClique em 'Adicionar Resposta' para começar")
            empty_label.setObjectName("emptyLabel")
            empty_label.setAlignment(Qt.AlignCenter)
            self.responses_layout.addWidget(empty_label)
        
        # Atualizar info da seção (removido o texto da seção)
        total_responses = len(self.data_manager.data.get(self.current_section, []))
        filtered_count = len(responses) if self.search_filter else total_responses
        # self.section_info.setText(f"Seção: {self.current_section} ({filtered_count}/{total_responses} respostas)")
        self.section_info.setText("")

    def select_section(self, section_name: str):
        """Seleciona uma seção"""
        if section_name in self.data_manager.data:
            self.current_section = section_name
            self.update_sections_ui()
            self.update_responses_ui()

    def filter_responses(self, search_text: str):
        """Filtra respostas baseado no texto de busca"""
        self.search_filter = search_text
        self.update_responses_ui()

    def add_section(self):
        """Adiciona nova seção"""
        name, ok = QInputDialog.getText(self, "Nova Seção", "Nome da seção:")
        if ok and name:
            # Verifica se há efeitos especiais para este nome de seção
            if validate_section_name(name, self):
                print("🎉 Efeito especial ativado!")
                return  # Não cria a seção, apenas mostra o efeito especial
            
            # Só cria a seção se não for o easter egg
            if self.data_manager.add_section(name):
                self.update_sections_ui()
                self.select_section(name)

    def rename_section(self, section_name: str):
        """Renomeia uma seção"""
        new_name, ok = QInputDialog.getText(self, "Renomear Seção", "Novo nome:", text=section_name)
        if ok and new_name and new_name != section_name:
            if self.data_manager.rename_section(section_name, new_name):
                self.current_section = new_name
                self.update_sections_ui()
                self.update_responses_ui()

    def remove_section(self, section_name: str):
        """Remove uma seção"""
        if len(self.data_manager.data) <= 1:
            QMessageBox.warning(self, "⚠️ Erro", "Não é possível remover a última seção.")
            return
            
        reply = QMessageBox.question(self, "🗑️ Confirmar", 
                                   f"Remover a seção '{section_name}' e todas as suas respostas?",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.data_manager.remove_section(section_name):
                self.current_section = list(self.data_manager.data.keys())[0]
                self.update_sections_ui()
                self.update_responses_ui()

    def show_section_menu(self, section_name: str, pos: QPoint):
        """Mostra menu de contexto da seção"""
        menu = QMenu(self)
        rename_action = menu.addAction("Renomear")
        remove_action = menu.addAction("Remover")
        
        action = menu.exec_(pos)
        if action == rename_action:
            self.rename_section(section_name)
        elif action == remove_action:
            self.remove_section(section_name)

    def add_response(self):
        """Adiciona nova resposta"""
        text, ok = QInputDialog.getText(self, "Nova Resposta", "Texto da resposta:")
        if ok and text:
            if self.data_manager.add_response(self.current_section, text):
                self.stats_manager.record_response_created()
                self.update_responses_ui()

    def edit_response(self, old_text: str):
        """Edita uma resposta"""
        new_text, ok = QInputDialog.getText(self, "Editar Resposta", "Novo texto:", text=old_text)
        if ok and new_text and new_text != old_text:
            if self.data_manager.edit_response(self.current_section, old_text, new_text):
                self.update_responses_ui()

    def duplicate_response(self, text: str):
        """Duplica uma resposta"""
        if self.data_manager.duplicate_response(self.current_section, text):
            self.stats_manager.record_response_created()
            self.update_responses_ui()

    def remove_response(self, text: str):
        """Remove uma resposta"""
        reply = QMessageBox.question(self, "🗑️ Confirmar", 
                                   f"Remover a resposta '{text[:50]}{'...' if len(text) > 50 else ''}'?",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.data_manager.remove_response(self.current_section, text):
                self.stats_manager.record_response_deleted()
                self.update_responses_ui()

    def copy_to_clipboard(self, text: str):
        """Copia texto para área de transferência"""
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        
        # Registrar uso
        self.stats_manager.record_copy(text, self.current_section)
        
        # Mostrar confirmação se configurado
        if self.config_manager.get("show_copy_confirmation", True):
            QMessageBox.information(self, "✅ Copiado!", "Texto copiado para área de transferência!")

    def show_stats(self):
        """Mostra diálogo de estatísticas"""
        dialog = StatsDialog(self.stats_manager, self)
        dialog.exec_()

    def show_settings(self):
        """Mostra diálogo de configurações"""
        dialog = SettingsDialog(self.config_manager, self)
        if dialog.exec_() == QDialog.Accepted:
            # Aplicar novo tema se necessário
            new_theme = self.config_manager.get("theme", "light")
            if new_theme != self.current_theme:
                self.current_theme = THEMES[new_theme]
                self.apply_styles()

    def show_help(self):
        """Mostra diálogo de ajuda"""
        dialog = HelpDialog(self)
        dialog.exec_()

    def show_window(self):
        """Mostra a janela principal"""
        # Esconder a bola flutuante
        if self.floating_button.isVisible():
            self.floating_button.fade_out()
            self.floating_button.hide()
        
        # Mostrar a janela principal
        self.show()
        self.raise_()
        self.activateWindow()
        self.fade_in()

    def _position_floating_button(self) -> None:
        """Posiciona a bola flutuante na tela"""
        # Garantir que a bola flutuante esteja configurada corretamente
        self.floating_button.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        
        # Usar a posição salva ou posição padrão
        floating_pos = self.config_manager.get("floating_button_position")
        if floating_pos:
            self.floating_button.move(floating_pos[0], floating_pos[1])
        else:
            # Posição padrão no canto inferior direito
            screen = QApplication.primaryScreen().geometry()
            self.floating_button.move(screen.width() - 90, screen.height() - 90)

    def minimize_window(self) -> None:
        """Minimiza para a bola flutuante"""
        self.hide()
        self._position_floating_button()
        
        # Mostrar a bola flutuante com delay para garantir visibilidade
        QTimer.singleShot(100, self.show_floating_button)

    def show_floating_button(self) -> None:
        """Mostra a bola flutuante"""
        self.floating_button.show()
        self.floating_button.raise_()
        self.floating_button.fade_in()

    def close_window(self):
        """Fecha a aplicação"""
        self.close()

    def mousePressEvent(self, event):
        """Permite arrastar a janela apenas pela barra de título"""
        if event.button() == Qt.LeftButton:
            # Verificar se o clique ocorreu dentro da barra de título
            if self.title_bar.geometry().contains(event.pos()):
                self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
                event.accept()
            else:
                # Se não foi na barra de título, ignorar o evento para permitir que widgets filhos o recebam
                event.ignore()

    def mouseMoveEvent(self, event):
        """Move a janela durante o arraste"""
        if event.buttons() & Qt.LeftButton and self.drag_position:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        """Finaliza o arraste da janela"""
        self.drag_position = None

    def import_data(self):
        """Importa dados de arquivo"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Importar Dados", "", 
            "Arquivos JSON (*.json);;Arquivos de Texto (*.txt);;Todos os Arquivos (*)"
        )
        if file_path:
            if self.data_manager.import_data(file_path):
                QMessageBox.information(self, "✅ Sucesso", "Dados importados com sucesso!")
                self.update_sections_ui()
                self.update_responses_ui()
            else:
                QMessageBox.warning(self, "❌ Erro", "Erro ao importar dados.")

    def export_data(self):
        """Exporta dados para arquivo"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Exportar Dados", "", 
            "Arquivos JSON (*.json);;Arquivos de Texto (*.txt);;Todos os Arquivos (*)"
        )
        if file_path:
            if self.data_manager.export_data(file_path):
                QMessageBox.information(self, "✅ Sucesso", "Dados exportados com sucesso!")
            else:
                QMessageBox.warning(self, "❌ Erro", "Erro ao exportar dados.")

    def setup_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(resource_path('fctbi.ico')))
        self.tray_icon.setToolTip("FCTBI Respostas Rápidas")
        self.tray_icon.activated.connect(self.tray_icon_activated)
        self.tray_icon.show()

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_window()

    def closeEvent(self, event):
        """Evento chamado quando a janela é fechada"""
        # Salvar configurações da janela
        self.config_manager.set("window_position", [self.x(), self.y()])
        self.config_manager.set("window_size", [self.width(), self.height()])
        
        # Esconder a bola flutuante se estiver visível
        if self.floating_button.isVisible():
            self.floating_button.hide()
        
        event.accept()
        QApplication.quit()




# --- FUNÇÃO PRINCIPAL ---
def main():
    app = QApplication(sys.argv)
    
    # Configurar fonte personalizada
    font_id = QFontDatabase.addApplicationFont(resource_path(CONFIG.FONT_FILE))
    if font_id >= 0:
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        app.setFont(QFont(font_family, 9))
    
    # Criar e mostrar a aplicação
    window = RespostaRapidaApp()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()