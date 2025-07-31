#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar executável do FCTBI Respostas Rápidas
Autor: Pablo Bernar
Versão: 2.0 - Otimizada para todas as aplicações
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def check_dependencies():
    """Verifica se as dependências necessárias estão instaladas"""
    print("🔍 Verificando dependências...")
    
    try:
        import PyInstaller
        print("✅ PyInstaller encontrado")
    except ImportError:
        print("❌ PyInstaller não encontrado. Instalando...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    try:
        import PyQt5
        print("✅ PyQt5 encontrado")
    except ImportError:
        print("❌ PyQt5 não encontrado. Instalando...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt5>=5.15.0,<6.0.0"])

def create_spec_file():
    """Cria arquivo de especificação otimizado para PyInstaller"""
    print("📝 Criando arquivo de especificação...")
    
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-
"""
Especificação PyInstaller para FCTBI Respostas Rápidas
Versão: 2.0 - Otimizada com todas as aplicações
"""

import sys
from pathlib import Path

# Configurações de análise
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('fctbi.ico', '.'),
        ('BLMelody-Regular.otf', '.'),
        ('special_effects.py', '.'),
    ],
    hiddenimports=[
        'PyQt5.QtCore',
        'PyQt5.QtGui', 
        'PyQt5.QtWidgets',
        'PyQt5.sip',
        'typing_extensions',
        'json',
        'pathlib',
        'datetime',
        'shutil',
        'sys',
        'os',
        'dataclasses',
        'typing',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'tkinter',
        'PIL',
        'cv2',
        'requests',
        'urllib3',
        'certifi',
        'charset_normalizer',
        'idna',
        'ssl',
        'http',
        'email',
        'xml',
        'html',
        'xmlrpc',
        'ftplib',
        'smtplib',
        'poplib',
        'imaplib',
        'nntplib',
        'telnetlib',
        'socketserver',
        'multiprocessing',
        'concurrent',
        'asyncio',
        'threading',
        'queue',
        'subprocess',
        'signal',
        'select',
        'socket',
        'tempfile',
        'zipfile',
        'tarfile',
        'gzip',
        'bz2',
        'lzma',
        'zlib',
        'hashlib',
        'hmac',
        'secrets',
        'base64',
        'binascii',
        'struct',
        'array',
        'weakref',
        'copyreg',
        'pickle',
        'shelve',
        'dbm',
        'sqlite3',
        'pydoc',
        'doctest',
        'unittest',
        'test',
        'distutils',
        'setuptools',
        'pkg_resources',
        'pkgutil',
        'importlib',
        'importlib.metadata',
        'importlib.util',
        'importlib.abc',
        'importlib.machinery',
        'importlib.resources',
        'runpy',
        'compileall',
        'py_compile',
        'tokenize',
        'ast',
        'symtable',
        'code',
        'codeop',
        'dis',
        'pickletools',
        'tabnanny',
        'py_compile',
        'compileall',
        'pyclbr',
        'filecmp',
        'difflib',
        'inspect',
        'ast',
        'symtable',
        'code',
        'codeop',
        'dis',
        'pickletools',
        'tabnanny',
        'py_compile',
        'compileall',
        'pyclbr',
        'filecmp',
        'difflib',
        'inspect',
        'traceback',
        'linecache',
        'locale',
        'gettext',
        'string',
        're',
        'difflib',
        'textwrap',
        'unicodedata',
        'stringprep',
        'readline',
        'rlcompleter',
        'code',
        'codeop',
        'dis',
        'pickletools',
        'tabnanny',
        'py_compile',
        'compileall',
        'pyclbr',
        'filecmp',
        'difflib',
        'inspect',
        'traceback',
        'linecache',
        'locale',
        'gettext',
        'string',
        're',
        'difflib',
        'textwrap',
        'unicodedata',
        'stringprep',
        'readline',
        'rlcompleter',
    ],
    noarchive=False,
    optimize=2,  # Otimização máxima
)

# Configurações do PYZ
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=None,
    exclude_binaries=False,
)

# Configurações do executável
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='FCTBI_Respostas_Rapidas',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Sem console para aplicação GUI
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='fctbi.ico',
    version_file=None,
    uac_admin=False,
    uac_uiaccess=False,
)

# Configurações da coleção (para distribuição)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='FCTBI_Respostas_Rapidas',
)
'''
    
    with open('FCTBI_Respostas_Rapidas.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ Arquivo de especificação criado: FCTBI_Respostas_Rapidas.spec")

def clean_build_dirs():
    """Limpa diretórios de build anteriores"""
    print("🧹 Limpando diretórios de build anteriores...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"✅ Removido: {dir_name}")
            except PermissionError:
                print(f"⚠️ Não foi possível remover {dir_name} (arquivos em uso)")
            except Exception as e:
                print(f"⚠️ Erro ao remover {dir_name}: {e}")

def build_executable():
    """Constrói o executável usando PyInstaller"""
    print("🔨 Iniciando construção do executável...")
    
    # Comando PyInstaller com otimizações
    cmd = [
        'pyinstaller',
        '--clean',  # Limpa cache
        '--noconfirm',  # Não pede confirmação
        '--log-level=INFO',  # Log detalhado
        'FCTBI_Respostas_Rapidas.spec'
    ]
    
    try:
        print("🚀 Executando PyInstaller...")
        print(f"Comando: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("✅ Build concluído com sucesso!")
        print("📋 Log do build:")
        print(result.stdout)
        
        if result.stderr:
            print("⚠️ Avisos:")
            print(result.stderr)
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro durante o build: {e}")
        print("📋 Log de erro:")
        print(e.stdout)
        print(e.stderr)
        return False
    
    return True

def verify_executable():
    """Verifica se o executável foi criado corretamente"""
    print("🔍 Verificando executável...")
    
    exe_path = Path('dist/FCTBI_Respostas_Rapidas/FCTBI_Respostas_Rapidas.exe')
    
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"✅ Executável criado: {exe_path}")
        print(f"📏 Tamanho: {size_mb:.1f} MB")
        
        # Verificar arquivos incluídos
        dist_dir = Path('dist/FCTBI_Respostas_Rapidas')
        if dist_dir.exists():
            files = list(dist_dir.rglob('*'))
            print(f"📁 Total de arquivos incluídos: {len(files)}")
            
            # Listar arquivos principais
            main_files = [f for f in files if f.is_file() and f.suffix in ['.exe', '.dll', '.pyd', '.ico', '.otf']]
            print("📋 Arquivos principais:")
            for file in main_files:
                print(f"   - {file.name}")
        
        return True
    else:
        print(f"❌ Executável não encontrado: {exe_path}")
        return False

def create_installer_script():
    """Cria script de instalação simples"""
    print("📝 Criando script de instalação...")
    
    installer_content = '''@echo off
echo ========================================
echo    FCTBI Respostas Rapidas - Instalador
echo ========================================
echo.

echo Instalando FCTBI Respostas Rapidas...
echo.

REM Criar diretório de instalação
if not exist "%USERPROFILE%\\Documents\\FCTBI" mkdir "%USERPROFILE%\\Documents\\FCTBI"

REM Copiar arquivos
xcopy /E /I /Y "FCTBI_Respostas_Rapidas" "%USERPROFILE%\\Documents\\FCTBI\\"

REM Criar atalho na área de trabalho
echo Criando atalho na area de trabalho...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\FCTBI Respostas Rapidas.lnk'); $Shortcut.TargetPath = '%USERPROFILE%\\Documents\\FCTBI\\FCTBI_Respostas_Rapidas.exe'; $Shortcut.Save()"

echo.
echo ========================================
echo    Instalacao concluida com sucesso!
echo ========================================
echo.
echo O FCTBI Respostas Rapidas foi instalado em:
echo %USERPROFILE%\\Documents\\FCTBI\\
echo.
echo Um atalho foi criado na area de trabalho.
echo.
pause
'''
    
    with open('instalar_fctbi.bat', 'w', encoding='utf-8') as f:
        f.write(installer_content)
    
    print("✅ Script de instalação criado: instalar_fctbi.bat")

def create_readme():
    """Cria README para o executável"""
    print("📝 Criando README...")
    
    readme_content = '''# FCTBI Respostas Rápidas - Executável

## 📋 Sobre
FCTBI (Ferramenta de Cópia de Textos para Bianca e Interação) é uma aplicação para gerenciar e acessar rapidamente respostas pré-definidas.

## 🚀 Como Usar

### Instalação Automática
1. Execute o arquivo `instalar_fctbi.bat` como administrador
2. O FCTBI será instalado em `Documents/FCTBI/`
3. Um atalho será criado na área de trabalho

### Instalação Manual
1. Copie a pasta `FCTBI_Respostas_Rapidas` para qualquer local
2. Execute `FCTBI_Respostas_Rapidas.exe`

## ✨ Funcionalidades

### Principais
- 📝 Gerenciamento de respostas organizadas em seções
- 🔍 Busca rápida de respostas
- 📋 Cópia com um clique para área de transferência
- 🎨 Temas claro e escuro
- 📊 Estatísticas de uso
- 💾 Backup automático

### Organização
- ⬆️⬇️ Setas para mover respostas
- 🖱️ Drag and drop livre
- 🔄 Mover respostas entre seções
- 📁 Reordenar seções
- 📤📥 Importar/exportar dados

### Atalhos de Teclado
- `Ctrl+F`: Buscar
- `Ctrl+N`: Nova resposta
- `Ctrl+Shift+N`: Nova seção
- `Ctrl+D`: Duplicar resposta
- `F2`: Editar resposta
- `Delete`: Remover item
- `Ctrl+↑/↓`: Mover resposta
- `Ctrl+1-9`: Alternar seções
- `ESC`: Minimizar

## 🎯 Características Especiais

### Bola Flutuante
- Minimiza para uma bola flutuante
- Sempre visível e acessível
- Arrastável para qualquer posição

### Easter Egg
- Digite "Bianca" como nome de seção para ativar efeito especial

### Configurações
- Tema claro/escuro
- Confirmação de cópia
- Som ao copiar
- Ordenação personalizada
- Backup automático

## 📁 Estrutura de Arquivos
```
FCTBI_Respostas_Rapidas/
├── FCTBI_Respostas_Rapidas.exe    # Executável principal
├── fctbi.ico                      # Ícone da aplicação
├── BLMelody-Regular.otf           # Fonte personalizada
└── [arquivos do sistema]          # Bibliotecas e dependências
```

## 🔧 Dados da Aplicação
Os dados são salvos automaticamente em:
`%USERPROFILE%\\Documents\\FCTBI_data\\`

- `respostas.json`: Respostas e seções
- `config.json`: Configurações da aplicação
- `stats.json`: Estatísticas de uso
- `respostas_backup.json_*`: Backups automáticos

## 🐛 Solução de Problemas

### Executável não abre
1. Verifique se o antivírus não está bloqueando
2. Execute como administrador
3. Verifique se todos os arquivos estão presentes

### Dados perdidos
1. Verifique a pasta `FCTBI_data` em Documents
2. Use os arquivos de backup automático
3. Restaure de uma exportação anterior

### Problemas de performance
1. Feche outras aplicações pesadas
2. Reinicie o FCTBI
3. Limpe dados antigos se necessário

## 📞 Suporte
- **Autor**: Pablo Bernar
- **GitHub**: github.com/PabloBernar
- **Versão**: 2.0 - Otimizada

## 📄 Licença
Oferecimento de Pablo p/Bianca s2 ❤️

---
*FCTBI Respostas Rápidas - Versão 2.0*
'''
    
    with open('README_EXECUTAVEL.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ README criado: README_EXECUTAVEL.md")

def main():
    """Função principal"""
    print("🚀 FCTBI Respostas Rápidas - Gerador de Executável")
    print("=" * 60)
    print()
    
    # Verificar dependências
    check_dependencies()
    print()
    
    # Limpar builds anteriores
    clean_build_dirs()
    print()
    
    # Criar arquivo de especificação
    create_spec_file()
    print()
    
    # Construir executável
    if build_executable():
        print()
        
        # Verificar resultado
        if verify_executable():
            print()
            
            # Criar arquivos adicionais
            create_installer_script()
            create_readme()
            
            print()
            print("🎉 Processo concluído com sucesso!")
            print("=" * 60)
            print("📁 Executável criado em: dist/FCTBI_Respostas_Rapidas/")
            print("📋 Arquivos gerados:")
            print("   - FCTBI_Respostas_Rapidas.exe")
            print("   - instalar_fctbi.bat (instalador)")
            print("   - README_EXECUTAVEL.md (documentação)")
            print()
            print("🚀 Para instalar, execute: instalar_fctbi.bat")
            print("📖 Para mais informações, leia: README_EXECUTAVEL.md")
        else:
            print("❌ Falha na verificação do executável")
            return 1
    else:
        print("❌ Falha na construção do executável")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 