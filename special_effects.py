import sys
import random
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QGraphicsDropShadowEffect
from PyQt5.QtGui import QPainter, QColor, QFont, QPainterPath, QPen
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRectF, pyqtProperty

class Particle:
    """
    Classe para representar uma partícula animada.
    """
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.reset()

    def reset(self):
        """ Reinicia a posição e as propriedades da partícula. """
        self.x = random.randint(0, self.screen_width)
        self.y = random.randint(-self.screen_height, 0)
        self.size = random.randint(10, 30)
        self.speed = random.uniform(1.0, 3.0)
        self.color = QColor(random.randint(200, 255), 105, 180, random.randint(100, 200)) # Tons de rosa/roxo
        self.drift = random.uniform(-0.5, 0.5) # Movimento lateral

    def move(self):
        """ Move a partícula para baixo. """
        self.y += self.speed
        self.x += self.drift
        if self.y > self.screen_height or self.x < -self.size or self.x > self.screen_width:
            self.reset()

    def draw(self, painter):
        """ Desenha a partícula na tela. """
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


class SpecialEffectWindow(QWidget):
    """
    Janela de efeito especial com animação de partículas e mensagem.
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

        self.particles = [Particle(self.width(), self.height()) for _ in range(50)]
        self.opacity = 0.0

        # Label para a mensagem principal
        self.message_label = QLabel("", self)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setFont(QFont("Segoe Script", 14, QFont.Bold)) # Uma fonte romântica
        self.message_label.setStyleSheet("color: white; background-color: transparent; line-height: 1.5;")
        # Centraliza perfeitamente a mensagem com mais espaço
        message_width = self.width()
        message_height = 300  # Altura maior para acomodar o texto
        x = 0
        y = (self.height() - message_height) // 2  # Centraliza verticalmente
        self.message_label.setGeometry(x, y, message_width, message_height)
        self.message_label.setGraphicsEffect(self.create_shadow())
        self.message_label.setWindowOpacity(0.0)  # Começa invisível

        # Timer para a animação das partículas
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
        
        # Configuração para animação de digitação
        self.full_text = "Te amo, Bianca.\n\n\"Há sempre alguma loucura no amor.\nHá sempre um pouco de razão na loucura.\"\n\nAss: Pablo."
        self.current_text = ""
        self.char_index = 0
        self.typewriter_timer = QTimer(self)
        self.typewriter_timer.timeout.connect(self.typewriter_effect)
        
        # Inicia a animação de digitação após o fade-in da janela
        QTimer.singleShot(500, self.start_typewriter_animation)

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

        # Desenha as partículas
        for particle in self.particles:
            particle.draw(painter)

    def start_typewriter_animation(self):
        """Inicia a animação de digitação"""
        self.typewriter_timer.start(50)  # 50ms entre cada caractere (mais rápido)
        
    def typewriter_effect(self):
        """Efeito de digitação letra por letra"""
        if self.char_index < len(self.full_text):
            self.current_text += self.full_text[self.char_index]
            self.message_label.setText(self.current_text)
            self.char_index += 1
        else:
            self.typewriter_timer.stop()
            # Adiciona um pequeno efeito de brilho no final
            QTimer.singleShot(200, self.add_final_glow)
    
    def add_final_glow(self):
        """Adiciona um efeito de brilho final na mensagem"""
        glow_effect = QGraphicsDropShadowEffect()
        glow_effect.setBlurRadius(20)
        glow_effect.setColor(QColor(255, 182, 193, 200))  # Rosa claro
        glow_effect.setOffset(0, 0)
        self.message_label.setGraphicsEffect(glow_effect)

    def update_animation(self):
        """ Atualiza a posição de todas as partículas e redesenha. """
        for particle in self.particles:
            particle.move()
        self.update() # Agenda um repaint

    def mousePressEvent(self, event):
        """ Fecha a janela ao clicar. """
        self.close()

    def keyPressEvent(self, event):
        """ Fecha a janela ao pressionar qualquer tecla. """
        self.close()

def validate_section_name(section_name, parent_window=None):
    """
    Valida o nome da seção e executa efeitos especiais se necessário.
    Retorna True se um efeito especial foi ativado, False caso contrário.
    """
    if section_name.lower().strip() == "bianca":
        # Usamos 'global' para que a janela não seja destruída pelo garbage collector
        global special_effect_window
        special_effect_window = SpecialEffectWindow(parent_window)
        special_effect_window.show()
        return True
    return False

# Exemplo de uso:
if __name__ == "__main__":
    # Teste do efeito especial
    app = QApplication(sys.argv)
    
    # Simula a criação de uma seção chamada "bianca"
    validate_section_name("bianca")
    
    sys.exit(app.exec_()) 