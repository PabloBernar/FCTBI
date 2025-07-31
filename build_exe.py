#!/usr/bin/env python3
"""
Script para criar o executável da aplicação FCTBI
"""

import subprocess
import sys
import os
from pathlib import Path

def install_pyinstaller():
    """Instala o PyInstaller se não estiver instalado"""
    try:
        import PyInstaller
        print("PyInstaller já está instalado.")
        return True
    except ImportError:
        print("Instalando PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("PyInstaller instalado com sucesso!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Erro ao instalar PyInstaller: {e}")
            return False

def build_executable():
    """Cria o executável usando o arquivo .spec"""
    spec_file = "FCTBI_Respostas.spec"
    
    if not os.path.exists(spec_file):
        print(f"Arquivo {spec_file} não encontrado!")
        return False
    
    print("Criando executável...")
    try:
        subprocess.check_call([sys.executable, "-m", "PyInstaller", spec_file])
        print("Executável criado com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erro ao criar executável: {e}")
        return False

def main():
    print("=== Script de Build do FCTBI ===")
    
    # Instala PyInstaller se necessário
    if not install_pyinstaller():
        print("Falha ao instalar PyInstaller. Abortando...")
        return
    
    # Cria o executável
    if build_executable():
        print("\n✅ Executável criado com sucesso!")
        print("📁 O arquivo .exe está na pasta 'dist'")
        print("🎉 Você pode executar o FCTBI_Respostas.exe")
    else:
        print("\n❌ Falha ao criar o executável.")

if __name__ == "__main__":
    main() 