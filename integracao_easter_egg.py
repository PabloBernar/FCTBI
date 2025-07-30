# Exemplo de como integrar o easter egg da Bianca no seu app principal usando PyQt5

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QInputDialog
from PyQt5.QtCore import Qt
from easter_egg_bianca import check_bianca_easter_egg

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("App com Easter Egg da Bianca 💕")
        self.setGeometry(100, 100, 500, 400)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout vertical
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Título
        title_label = QLabel("🎉 Easter Egg Especial da Bianca 🎉")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #FF69B4; margin: 20px;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Botão para criar seção
        self.btn_criar = QPushButton("Criar Nova Seção")
        self.btn_criar.setStyleSheet("""
            QPushButton {
                background-color: #FF69B4;
                color: white;
                border: none;
                padding: 15px;
                font-size: 16px;
                border-radius: 10px;
                margin: 20px;
            }
            QPushButton:hover {
                background-color: #FF1493;
            }
        """)
        self.btn_criar.clicked.connect(self.criar_secao_interface)
        layout.addWidget(self.btn_criar)
        
        # Dica
        dica_label = QLabel("💡 Dica: Tente criar uma seção chamada 'bianca'! 💕")
        dica_label.setStyleSheet("font-size: 14px; color: #666; margin: 20px;")
        dica_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(dica_label)
        
        # Instruções
        instrucoes_label = QLabel(
            "Como funciona:\n"
            "1. Clique em 'Criar Nova Seção'\n"
            "2. Digite 'bianca' como nome\n"
            "3. Veja a mágica acontecer! ✨"
        )
        instrucoes_label.setStyleSheet("font-size: 12px; color: #888; margin: 20px; background-color: #f0f0f0; padding: 15px; border-radius: 10px;")
        instrucoes_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(instrucoes_label)
        
        # Status
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("font-size: 12px; color: #666; margin: 10px;")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

    def criar_secao_interface(self):
        """Interface para criar uma nova seção"""
        nome, ok = QInputDialog.getText(self, "Nova Seção", "Digite o nome da seção:")
        if ok and nome:
            self.criar_secao(nome, self)

    def criar_secao(self, nome_secao, parent_window=None):
        """
        Função para criar uma nova seção no app
        """
        # Verifica se é o easter egg ANTES de criar a seção
        if check_bianca_easter_egg(nome_secao, parent_window):
            self.status_label.setText("🎉 Easter egg ativado! Te amo, Bianca! 💕")
            self.status_label.setStyleSheet("font-size: 14px; color: #FF69B4; font-weight: bold; margin: 10px;")
        else:
            self.status_label.setText(f"Seção '{nome_secao}' criada com sucesso!")
            self.status_label.setStyleSheet("font-size: 12px; color: #666; margin: 10px;")
        
        # Código normal para criar a seção
        print(f"Seção '{nome_secao}' criada com sucesso!")
        
        # ... resto do código para criar a seção ...

def main():
    app = QApplication(sys.argv)
    
    # Estilo global da aplicação
    app.setStyleSheet("""
        QMainWindow {
            background-color: #fafafa;
        }
    """)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 