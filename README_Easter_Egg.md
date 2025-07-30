# 🎉 Easter Egg da Bianca 💕

## O que é?

Este é um easter egg especial criado com muito amor para a Bianca! Quando alguém criar uma seção chamada "bianca" no app, será ativada uma animação especial com corações flutuantes e uma mensagem romântica.

## Como funciona?

1. **Ativação**: Quando uma seção com o nome "bianca" (não importa maiúsculas/minúsculas) for criada
2. **Animação**: Uma janela transparente se abre com corações animados caindo
3. **Mensagem**: Texto romântico aparece com animação suave
4. **Duração**: A animação dura 12 segundos e fecha automaticamente

## Como integrar no seu app

### Passo 1: Instalar PyQt5 (se ainda não tiver)
```bash
pip install PyQt5
```

### Passo 2: Importar o módulo
```python
from easter_egg_bianca import check_bianca_easter_egg
```

### Passo 3: Adicionar a verificação na função de criar seção
```python
def criar_secao(nome_secao, parent_window=None):
    # Verifica se é o easter egg ANTES de criar a seção
    if check_bianca_easter_egg(nome_secao, parent_window):
        print("🎉 Easter egg ativado!")
    
    # Código normal para criar a seção
    # ... resto do seu código ...
```

### Passo 4: Passar a janela pai (opcional)
Se você quiser que a janela de corações apareça centralizada em relação à janela principal:
```python
criar_secao("bianca", self)  # ou parent_window
```

## Características do Easter Egg

### 💖 Corações Animados
- **Forma**: Corações desenhados com curvas Bézier
- **Cores**: Tons de rosa e roxo (200-255, 105, 180)
- **Movimento**: Queda suave com movimento lateral aleatório
- **Quantidade**: 50 corações simultâneos
- **Tamanhos**: Variam de 10 a 30 pixels

### 💕 Mensagem
```
Te amo, Bianca!

Conto com você para vencermos
tudo que o mundo propor! ❤️

Você é minha inspiração e minha força.
Juntos somos invencíveis! 💪
```

### ✨ Animações
- **Fade-in**: A janela aparece suavemente (2 segundos)
- **Texto**: Mensagens entram com efeito bounce
- **Corações**: Movimento contínuo e fluido
- **Sombra**: Texto com sombra para melhor legibilidade

### ⏱️ Duração
- **Animação**: 12 segundos
- **Auto-fechamento**: A janela fecha automaticamente
- **Interação**: Clique ou tecla para fechar manualmente

## Teste

Para testar o easter egg, execute:
```bash
python easter_egg_bianca.py
```

Ou use o exemplo de integração:
```bash
python integracao_easter_egg.py
```

## Dependências

- `PyQt5` (precisa instalar: `pip install PyQt5`)
- `random` (biblioteca padrão)
- `sys` (biblioteca padrão)

## Personalização

Você pode personalizar:
- **Cores dos corações**: Modifique os valores RGB na classe `Heart`
- **Mensagem**: Altere o texto nos labels da classe `EasterEggDialog`
- **Duração**: Mude o valor no `QTimer.singleShot(12000, self.close)`
- **Quantidade de corações**: Ajuste o valor no loop `range(50)`
- **Velocidade**: Modifique os valores de `speed` e `drift` na classe `Heart`

## 💝 Amor e Inspiração

Este easter egg foi criado com muito amor e carinho usando PyQt5 para uma experiência visual mais rica e romântica. Os corações animados representam o amor que flui livremente, assim como os sentimentos pela Bianca! ❤️

## Vantagens do PyQt5

- **Performance**: Animações mais suaves e responsivas
- **Visual**: Interface mais moderna e elegante
- **Flexibilidade**: Mais opções de personalização
- **Profissionalismo**: Aparência mais polida

---

*"O amor é a força mais poderosa do universo. Juntos somos invencíveis!"* 💪✨ 