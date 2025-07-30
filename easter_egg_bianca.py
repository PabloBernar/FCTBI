import sys
import random
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QGraphicsDropShadowEffect
from PyQt5.QtGui import QPainter, QColor, QFont, QPainterPath, QPen
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRectF, pyqtProperty

class Heart:
    """
    Classe para representar um único coração animado.
    """
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.reset()

    def reset(self):
        """ Reinicia a posição e as propriedades do coração. """
        self.x = random.randint(0, self.screen_width)
        self.y = random.randint(-self.screen_height, 0)
        self.size = random.randint(10, 30)
        self.speed = random.uniform(1.0, 3.0)
        self.color = QColor(random.randint(200, 255), 105, 180, random.randint(100, 200)) # Tons de rosa/roxo
        self.drift = random.uniform(-0.5, 0.5) # Movimento lateral

    def move(self):
        """ Move o coração para baixo. """
        self.y += self.speed
        self.x += self.drift
        if self.y > self.screen_height or self.x < -self.size or self.x > self.screen_width:
            self.reset()

    def draw(self, painter):
        """ Desenha o coração na tela. """
        path = QPainterPath()
        path.moveTo(self.x, self.y + self.size * 0.25)
        path.cubicTo(self.x, self.y,
                      self.x - self.size * 0.5, self.y,
                      self.x - self.size * 0.5, self.y + self.size * 0.25)
        path.cubicTo(self.x - self.size * 0.5, self.y + self.size * 0.60,
                      self.x, self.y + self.size * 0.80,
                      self.x, self.y + self.size)
        path.cubicTo(self.x, self.y + self.size * 0.80,
                      self.x + self.size * 0.5, self.y + self.size * 0.60,
                      self.x + self.size * 0.5, self.y + self.size * 0.25)
        path.cubicTo(self.x + self.size * 0.5, self.y,
                      self.x, self.y,
                      self.x, self.y + self.size * 0.25)
        
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.color)
        painter.drawPath(path)


class EasterEggDialog(QWidget):
    """
    A janela do easter egg, com animação de corações e mensagem.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Posiciona a janela no centro da janela pai
        if parent:
            parent_rect = parent.geometry()
            self.setGeometry(parent_rect.x(), parent_rect.y(), parent_rect.width(), parent_rect.height())
        else:
            self.resize(800, 600)

        self.hearts = [Heart(self.width(), self.height()) for _ in range(50)]
        self.opacity = 0.0

        # Label para a mensagem principal
        self.message_label = QLabel("Te amo, Bianca!\n\nConto com você para vencermos\ntudo que o mundo propor! ❤️", self)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setFont(QFont("Segoe Script", 20, QFont.Bold)) # Uma fonte romântica
        self.message_label.setStyleSheet("color: white; background-color: transparent;")
        self.message_label.setGeometry(0, -self.height() // 2, self.width(), self.height()) # Começa fora da tela
        self.message_label.setGraphicsEffect(self.create_shadow())

        # Label para a mensagem secundária
        self.sub_message_label = QLabel("Você é minha inspiração e minha força.\nJuntos somos invencíveis! 💪", self)
        self.sub_message_label.setAlignment(Qt.AlignCenter)
        self.sub_message_label.setFont(QFont("Segoe Script", 14, QFont.Normal))
        self.sub_message_label.setStyleSheet("color: #FFB6C1; background-color: transparent;")
        self.sub_message_label.setGeometry(0, self.height() + 50, self.width(), 100) # Começa abaixo da tela
        self.sub_message_label.setGraphicsEffect(self.create_shadow())

        # Timer para a animação dos corações
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(30) # ~30 FPS

        # Animação de fade-in da janela
        self.fade_in_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_animation.setDuration(2000)
        self.fade_in_animation.setStartValue(0.0)
        self.fade_in_animation.setEndValue(1.0)
        self.fade_in_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.fade_in_animation.start()
        
        # Animação da mensagem principal
        self.message_animation = QPropertyAnimation(self.message_label, b"geometry")
        self.message_animation.setDuration(1500)
        self.message_animation.setStartValue(self.message_label.geometry())
        self.message_animation.setEndValue(QRectF(0, self.height()//4, self.width(), self.height()//2))
        self.message_animation.setEasingCurve(QEasingCurve.OutBounce)
        
        # Animação da mensagem secundária
        self.sub_message_animation = QPropertyAnimation(self.sub_message_label, b"geometry")
        self.sub_message_animation.setDuration(1500)
        self.sub_message_animation.setStartValue(self.sub_message_label.geometry())
        self.sub_message_animation.setEndValue(QRectF(0, self.height()*3//4, self.width(), 100))
        self.sub_message_animation.setEasingCurve(QEasingCurve.OutBounce)
        
        # Inicia a animação da mensagem após um pequeno delay
        QTimer.singleShot(500, self.message_animation.start)
        QTimer.singleShot(1000, self.sub_message_animation.start)

        # Timer para fechar automaticamente após 12 segundos
        QTimer.singleShot(12000, self.close)

    def create_shadow(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(2, 2)
        return shadow

    @pyqtProperty(float)
    def windowOpacity(self):
        return self.opacity

    @windowOpacity.setter
    def windowOpacity(self, value):
        self.opacity = value
        self.setWindowOpacity(value)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Fundo semi-transparente com gradiente
        gradient = QPainterPath()
        gradient.addRect(QRectF(self.rect()))
        
        # Fundo escuro e romântico
        painter.setBrush(QColor(22, 12, 41, int(220 * self.opacity)))
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

        # Desenha os corações
        for heart in self.hearts:
            heart.draw(painter)

    def update_animation(self):
        """ Atualiza a posição de todos os corações e redesenha. """
        for heart in self.hearts:
            heart.move()
        self.update() # Agenda um repaint

    def mousePressEvent(self, event):
        """ Fecha a janela ao clicar. """
        self.close()

    def keyPressEvent(self, event):
        """ Fecha a janela ao pressionar qualquer tecla. """
        self.close()

def check_bianca_easter_egg(section_name, parent_window=None):
    """
    Verifica se o nome da seção ativa o easter egg e o exibe.
    Retorna True se o easter egg foi ativado, False caso contrário.
    """
    if section_name.lower().strip() == "bianca":
        # Usamos 'global' para que a janela não seja destruída pelo garbage collector
        global easter_egg_window
        easter_egg_window = EasterEggDialog(parent_window)
        easter_egg_window.show()
        return True
    return False

# Exemplo de uso:
if __name__ == "__main__":
    # Teste do easter egg
    app = QApplication(sys.argv)
    
    # Simula a criação de uma seção chamada "bianca"
    check_bianca_easter_egg("bianca")
    
    sys.exit(app.exec_()) 