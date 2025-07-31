"""
Script de configuração para build com PyInstaller
"""

import PyInstaller.__main__
import os
import sys

def build_executable():
    """Compila o executável usando PyInstaller"""
    
    # Configurações do PyInstaller
    args = [
        'main.py',                          # Script principal
        '--onefile',                        # Arquivo único
        '--windowed',                       # Sem console (GUI)
        '--name=FCTBI',                     # Nome do executável
        '--icon=fctbi.ico',                 # Ícone
        '--add-data=BLMelody-Regular.otf;.',  # Fonte
        '--add-data=fctbi.ico;.',           # Ícone
        '--hidden-import=PyQt5.sip',        # Import necessário
        '--clean',                          # Limpar cache
        '--noconfirm',                      # Não confirmar overwrite
    ]
    
    # Adicionar argumentos específicos do sistema operacional
    if sys.platform.startswith('win'):
        args.extend([
            '--runtime-hook=windows_hook.py',
        ])
    elif sys.platform.startswith('linux'):
        args.extend([
            '--runtime-hook=linux_hook.py',
        ])
    elif sys.platform.startswith('darwin'):
        args.extend([
            '--runtime-hook=macos_hook.py',
        ])
    
    # Executar PyInstaller
    PyInstaller.__main__.run(args)

if __name__ == "__main__":
    build_executable() 