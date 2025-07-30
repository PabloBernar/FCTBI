# Bola Flutuante - FCTBI Respostas Rápidas

## Como Funciona

A bola flutuante é uma funcionalidade que permite minimizar o aplicativo FCTBI para uma pequena bola circular que fica sempre visível na tela.

### Funcionalidades

1. **Minimização**: Quando você clica no botão "–" (minimizar) na barra de título, o aplicativo é minimizado para a bola flutuante
2. **Restauração**: Clique na bola flutuante para restaurar o aplicativo
3. **Movimento**: Arraste a bola flutuante para movê-la para qualquer posição da tela
4. **Posição Salva**: A posição da bola flutuante é salva automaticamente e restaurada na próxima execução

### Como Usar

1. **Minimizar o App**:
   - Clique no botão "–" na barra de título
   - Ou pressione `ESC` no teclado
   - O app desaparecerá e a bola flutuante aparecerá no canto inferior direito

2. **Restaurar o App**:
   - Clique na bola flutuante
   - O app voltará com uma animação suave

3. **Mover a Bola**:
   - Arraste a bola flutuante para qualquer posição
   - A posição será salva automaticamente

### Características Visuais

- **Formato**: Círculo com 60x60 pixels
- **Cor**: Roxo (#463e91) com borda branca
- **Texto**: "FCTBI" em branco
- **Sombra**: Efeito de sombra para melhor visibilidade
- **Tooltip**: "Clique para abrir o FCTBI\nArraste para mover"

### Posicionamento

- **Padrão**: Canto inferior direito da tela
- **Personalizado**: Pode ser movida para qualquer posição
- **Persistente**: A posição é salva entre as execuções

### Atalhos de Teclado

- `ESC`: Minimizar para bola flutuante
- Clique na bola: Restaurar aplicativo

### Solução de Problemas

Se a bola flutuante não aparecer:

1. Verifique se o aplicativo foi minimizado corretamente
2. Procure pela bola no canto inferior direito da tela
3. Se não encontrar, tente pressionar `ESC` novamente
4. Verifique se não há outros aplicativos cobrindo a bola

### Teste

Para testar a funcionalidade da bola flutuante, execute:

```bash
python test_floating_button.py
```

Este arquivo de teste permite verificar se a bola flutuante está funcionando corretamente.

### Configuração

A posição da bola flutuante é salva automaticamente no arquivo de configuração:
- Localização: `Documents/FCTBI_data/config.json`
- Chave: `floating_button_position`
- Formato: `[x, y]` (coordenadas da tela) 