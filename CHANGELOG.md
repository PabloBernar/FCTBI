# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [2.0.0] - 2024-01-XX

### Adicionado
- **Estrutura de projeto melhorada** com organização em módulos
- **Type hints** completos em todas as funções e classes
- **Documentação** com docstrings detalhadas
- **Configuração de projeto** com `pyproject.toml`
- **Sistema de testes** com pytest e cobertura
- **Pre-commit hooks** para qualidade de código
- **Configuração de linting** com black, flake8 e mypy
- **Setup.py** para distribuição do pacote
- **Script de build** para PyInstaller
- **Gitignore** completo e otimizado

### Melhorado
- **Organização do código** com separação clara de responsabilidades
- **Tratamento de erros** mais robusto com funções seguras
- **Performance** otimizada com remoção de código duplicado
- **Constantes** organizadas em dataclass `AppConfig`
- **Funções utilitárias** para operações comuns
- **Gerenciadores de dados** com melhor estrutura
- **Drag and drop** otimizado com funções genéricas
- **Sistema de backup** mais confiável
- **Interface de usuário** mais responsiva

### Refatorado
- **ConfigManager** com melhor tratamento de erros
- **StatsManager** com funções mais eficientes
- **DataManager** com operações otimizadas
- **Funções de movimento** consolidadas em métodos genéricos
- **Sistema de drag and drop** unificado
- **Funções de atalhos** simplificadas
- **Gerenciamento de bola flutuante** otimizado

### Removido
- **Código duplicado** em várias funções
- **Função save()** duplicada na classe principal
- **Variáveis globais** desnecessárias
- **Comentários** obsoletos e código morto

### Corrigido
- **Problemas de tipagem** em várias funções
- **Tratamento de erros** em operações de arquivo
- **Vazamentos de memória** em widgets
- **Problemas de performance** em operações de drag and drop

### Segurança
- **Validação de entrada** melhorada
- **Tratamento seguro de arquivos** JSON
- **Proteção contra** operações inválidas

## [1.0.0] - 2023-XX-XX

### Adicionado
- Interface gráfica moderna com PyQt5
- Sistema de seções para organizar respostas
- Drag and drop para reorganizar respostas e seções
- Bola flutuante para acesso rápido
- Sistema de estatísticas de uso
- Temas claro e escuro
- Backup automático
- Importação e exportação de dados
- Atalhos de teclado
- Easter egg especial

### Funcionalidades
- Cópia rápida de respostas para área de transferência
- Busca e filtragem de respostas
- Ordenação por diferentes critérios
- Configurações personalizáveis
- Sistema de ajuda integrado 