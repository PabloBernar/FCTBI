"""
Setup script para FCTBI - Ferramenta de Cópia de Textos para Bianca e Interação
"""

from setuptools import setup, find_packages
import os

# Ler o README
def read_readme():
    with open("readme.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Ler requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="fctbi",
    version="2.0.0",
    author="Pablo Bernar",
    author_email="pablo.bernar@example.com",
    description="Ferramenta de Cópia de Textos para Bianca e Interação - Respostas Rápidas",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/PabloBernar/FCTBI",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Desktop Environment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "fctbi=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.ico", "*.otf", "*.json"],
    },
    keywords="desktop, clipboard, productivity, responses, quick-copy",
    project_urls={
        "Bug Reports": "https://github.com/PabloBernar/FCTBI/issues",
        "Source": "https://github.com/PabloBernar/FCTBI",
        "Documentation": "https://github.com/PabloBernar/FCTBI/blob/main/readme.md",
    },
) 