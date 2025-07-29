# Guia de Modificação e Entendimento do Código - App de Respostas Rápidas

Este documento serve como um guia para entender a estrutura do código e, principalmente, para saber onde fazer alterações no design e na funcionalidade do aplicativo.

##  Estrutura do Projeto

O projeto é composto por três arquivos principais:

-   `app.py`: Contém todo o código-fonte Python do aplicativo. É aqui que a lógica e a estrutura da interface são definidas.
-   `respostas.json`: É um pequeno "banco de dados" em formato de texto. Ele armazena as frases de resposta rápida que você adiciona.
-   [cite_start]`BLMelody-Regular.otf`: O arquivo da fonte personalizada utilizada no design do aplicativo [cite: 1-73].

---

## Parte 1: O Design (Como Alterar a Aparência)

A aparência do aplicativo é controlada principalmente por um grande bloco de estilos (QSS) e por algumas funções de desenho no código Python.

### 1.1. Cores, Fontes e Estilos Gerais (O Lugar Mais Importante)

A maneira mais fácil e rápida de mudar o visual do app é editando o bloco de estilos **QSS (Qt Style Sheets)**.

**Onde encontrar:** No arquivo `app.py`, procure pela linha `app.setStyleSheet(f"""...""")` quase no final do arquivo.

> **DICA:** Para mudar a cor principal de roxo para, por exemplo, um azul (`#007ACC`), você só precisa alterar a variável `PRIMARY_COLOR` no topo do arquivo.
> ```python
> # Altere esta linha no início do app.py
> PRIMARY_COLOR = "#007ACC"
> ```

**O que você pode alterar no bloco QSS:**

-   **`#responseButton`**: Estilo dos botões com as frases de resposta.
    -   `background-color`: Cor de fundo do botão.
    -   `color`: Cor do texto do botão.
    -   `padding`: Espaçamento interno.
    -   `border-radius`: Nível de arredondamento dos cantos.
-   **`#addButton`**: Estilo do botão "ADD+".
-   **`#titleLabel`**: Estilo do título "FCTBI" na barra superior.
-   **`QScrollBar`**: Aparência da barra de rolagem (largura, cor do trilho, cor da alça).
-   **`QMenu`**: Aparência do menu de "Editar/Remover".

### 1.2. Aparência da Janela Principal (Bordas e Cantos)

A forma da janela (cantos arredondados e a borda roxa) é desenhada manualmente.

**Onde encontrar:** No arquivo `app.py`, dentro da classe `RespostaRapidaApp`, procure pelo método `paintEvent`.

```python
# Dentro da classe RespostaRapidaApp
def paintEvent(self, event):
    # ...
    # Para alterar a espessura da borda, mude o número 3 aqui:
    painter.setPen(QPen(QColor(PRIMARY_COLOR), 3)) 
    # ...
    # Para alterar o arredondamento dos cantos, mude o valor 15 aqui:
    painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 15, 15)
```

### 1.3. O Botão Flutuante Circular

Assim como a janela principal, o botão flutuante também é desenhado manualmente para obter a forma de círculo.

**Onde encontrar:** No arquivo `app.py`, dentro da classe `FloatingButton`, procure pelo método `paintEvent`.

```python
# Dentro da classe FloatingButton
def paintEvent(self, event):
    # ...
    # Esta linha desenha o círculo roxo.
    painter.drawEllipse(5, 5, 60, 60)

    # Esta linha desenha o texto "FCTBI" no centro do botão.
    # Altere o texto aqui se desejar.
    painter.drawText(self.rect(), Qt.AlignCenter, "FCTBI") 
```

### 1.4. Ícones e Textos Fixos

Textos fixos, como o título da janela e os ícones dos botões de controle, são definidos diretamente na criação dos widgets.

**Onde encontrar:** No arquivo `app.py`, dentro do método `__init__` da classe `RespostaRapidaApp`.

```python
# Dentro de RespostaRapidaApp.__init__

# Alterar o texto do título
title_label = QLabel("FCTBI") 

# Alterar o ícone de minimizar
btn_minimize = QPushButton("–") 

# Alterar o ícone de fechar
btn_close = QPushButton("✕")
```

---

## Parte 2: A Lógica do Código (Como Alterar o Comportamento)

Esta seção mostra onde alterar as funcionalidades do aplicativo.

### 2.1. Gerenciamento de Respostas

As funções que lidam com a adição, edição e remoção das respostas são bem definidas.

**Onde encontrar:** No arquivo `app.py`, dentro da classe `RespostaRapidaApp`.

-   `adicionar_resposta()`: Chamada quando o botão "ADD+" é clicado. Abre a caixa de diálogo para inserir novo texto.
-   `editar_resposta()`: Chamada pelo menu "Editar".
-   `remover_resposta()`: Chamada pelo menu "Remover".
-   `copiar_para_area_transferencia()`: Chamada quando um botão de resposta é clicado. Copia o texto e mostra a notificação.

### 2.2. Animações (Fade In / Fade Out)

As animações de surgimento e desaparecimento são controladas pela classe `FaderWidget`.

**Onde encontrar:** No arquivo `app.py`, dentro da classe `FaderWidget`.

> **DICA:** Para deixar as animações mais rápidas ou mais lentas, altere o valor de `setDuration()`. O valor é em milissegundos (1000 = 1 segundo).

```python
# Dentro da classe FaderWidget
def __init__(self, parent=None):
    # ...
    # Altere o valor 300 para deixar a animação mais rápida (ex: 150) ou mais lenta (ex: 500)
    self.fade_animation.setDuration(300) 
```

### 2.3. Comportamento da Janela e Bandeja do Sistema (Tray)

As ações que acontecem ao minimizar, fechar ou interagir com o ícone na bandeja do sistema.

**Onde encontrar:** No arquivo `app.py`, dentro da classe `RespostaRapidaApp`.

-   `handle_minimize()`: Define o que acontece ao clicar no botão "–" (esconde a janela e mostra o botão flutuante).
-   `handle_close()`: Define o que acontece ao clicar no botão "✕" (inicia a animação de fechar e encerra o app).
-   `setup_tray_icon()`: Monta o menu que aparece ao clicar com o botão direito no ícone da bandeja do sistema ("Abrir", "Adicionar Resposta", "Sair").

Com este guia, você tem um mapa completo para navegar pelo código e adaptar tanto a aparência quanto o funcionamento do aplicativo às suas necessidades.