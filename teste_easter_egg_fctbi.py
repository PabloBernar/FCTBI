#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste do Easter Egg da Bianca integrado no FCTBI
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QInputDialog, QLabel
from PyQt5.QtCore import Qt

# Importa o easter egg
from easter_egg_bianca import check_bianca_easter_egg

class TesteEasterEgg(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Teste do Easter Egg da Bianca - FCTBI")
        self.setGeometry(100, 100, 400, 300)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Título
        title = QLabel("🎉 Teste do Easter Egg da Bianca 🎉")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #FF69B4; margin: 10px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Instruções
        instructions = QLabel(
            "Para testar o easter egg:\n"
            "1. Clique no botão abaixo\n"
            "2. Digite 'bianca' (ou 'Bianca')\n"
            "3. Veja a mágica acontecer! ✨\n\n"
            "💕 Este é um presente especial para a Bianca! 💕"
        )
        instructions.setStyleSheet("font-size: 12px; color: #666; margin: 20px; background-color: #f0f0f0; padding: 15px; border-radius: 10px;")
        instructions.setAlignment(Qt.AlignCenter)
        layout.addWidget(instructions)
        
        # Botão para testar
        btn_test = QPushButton("Criar Nova Seção (Teste)")
        btn_test.setStyleSheet("""
            QPushButton {
                background-color: #FF69B4;
                color: white;
                border: none;
                padding: 15px;
                font-size: 14px;
                border-radius: 10px;
                margin: 20px;
            }
            QPushButton:hover {
                background-color: #FF1493;
            }
        """)
        btn_test.clicked.connect(self.testar_easter_egg)
        layout.addWidget(btn_test)
        
        # Status
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("font-size: 12px; color: #666; margin: 10px;")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

    def testar_easter_egg(self):
        """Testa a criação de uma seção com o easter egg"""
        name, ok = QInputDialog.getText(self, "Nova Seção", "Nome da seção:")
        if ok and name:
            # Verifica se é o easter egg da Bianca
            if check_bianca_easter_egg(name, self):
                self.status_label.setText("🎉 Easter egg ativado! Te amo, Bianca! 💕")
                self.status_label.setStyleSheet("font-size: 14px; color: #FF69B4; font-weight: bold; margin: 10px;")
                print(f"🎉 Easter egg ativado para a seção: '{name}'")
            else:
                self.status_label.setText(f"Seção '{name}' criada normalmente")
                self.status_label.setStyleSheet("font-size: 12px; color: #666; margin: 10px;")
                print(f"Seção '{name}' criada normalmente")

def main():
    app = QApplication(sys.argv)
    
    # Estilo global
    app.setStyleSheet("""
        QMainWindow {
            background-color: #fafafa;
        }
    """)
    
    window = TesteEasterEgg()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 