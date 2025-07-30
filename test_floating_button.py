#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

# Importar as classes do arquivo principal
from main_copy import FloatingButton, FaderWidget

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Teste da Bola Flutuante")
        self.setGeometry(100, 100, 300, 200)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Botão para testar a bola flutuante
        test_button = QPushButton("Minimizar para Bola Flutuante")
        test_button.clicked.connect(self.test_floating_button)
        layout.addWidget(test_button)
        
        # Criar a bola flutuante
        self.floating_button = FloatingButton(self.show_window)
        self.floating_button.hide()
        
    def test_floating_button(self):
        print("Testando bola flutuante...")
        self.hide()
        
        # Posicionar a bola flutuante
        screen = QApplication.primaryScreen().geometry()
        self.floating_button.move(screen.width() - 80, screen.height() - 80)
        self.floating_button.show()
        self.floating_button.fade_in()
        
    def show_window(self):
        print("Mostrando janela de teste...")
        self.floating_button.fade_out()
        self.show()

def main():
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 