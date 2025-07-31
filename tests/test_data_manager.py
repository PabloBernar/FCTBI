"""
Testes unitários para o DataManager
"""

import unittest
import tempfile
import os
import json
from datetime import datetime
from unittest.mock import patch, MagicMock

# Importar o módulo a ser testado
import sys
sys.path.append('..')
from main import DataManager


class TestDataManager(unittest.TestCase):
    """Testes para a classe DataManager"""
    
    def setUp(self):
        """Configuração inicial para cada teste"""
        # Criar arquivo temporário para testes
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.data_manager = DataManager(self.temp_file.name)
    
    def tearDown(self):
        """Limpeza após cada teste"""
        # Remover arquivo temporário
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_load_data_new_file(self):
        """Testa carregamento de arquivo novo"""
        # Remover arquivo para simular arquivo novo
        os.unlink(self.temp_file.name)
        data_manager = DataManager(self.temp_file.name)
        
        self.assertEqual(data_manager.data, {"Geral": []})
    
    def test_load_data_existing_file(self):
        """Testa carregamento de arquivo existente"""
        test_data = {"Geral": [{"texto": "teste", "data": "2023-01-01"}]}
        with open(self.temp_file.name, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)
        
        data_manager = DataManager(self.temp_file.name)
        self.assertEqual(data_manager.data, test_data)
    
    def test_add_section(self):
        """Testa adição de seção"""
        result = self.data_manager.add_section("Nova Seção")
        self.assertTrue(result)
        self.assertIn("Nova Seção", self.data_manager.data)
        self.assertEqual(self.data_manager.data["Nova Seção"], [])
    
    def test_add_section_empty_name(self):
        """Testa adição de seção com nome vazio"""
        result = self.data_manager.add_section("")
        self.assertFalse(result)
    
    def test_add_section_duplicate(self):
        """Testa adição de seção duplicada"""
        self.data_manager.add_section("Seção")
        result = self.data_manager.add_section("Seção")
        self.assertFalse(result)
    
    def test_remove_section(self):
        """Testa remoção de seção"""
        self.data_manager.add_section("Seção")
        result = self.data_manager.remove_section("Seção")
        self.assertTrue(result)
        self.assertNotIn("Seção", self.data_manager.data)
    
    def test_remove_last_section(self):
        """Testa remoção da última seção"""
        result = self.data_manager.remove_section("Geral")
        self.assertFalse(result)  # Não deve permitir remover a última seção
    
    def test_add_response(self):
        """Testa adição de resposta"""
        result = self.data_manager.add_response("Geral", "Nova resposta")
        self.assertTrue(result)
        self.assertEqual(len(self.data_manager.data["Geral"]), 1)
        self.assertEqual(self.data_manager.data["Geral"][0]["texto"], "Nova resposta")
    
    def test_add_response_empty_text(self):
        """Testa adição de resposta com texto vazio"""
        result = self.data_manager.add_response("Geral", "")
        self.assertFalse(result)
    
    def test_remove_response(self):
        """Testa remoção de resposta"""
        self.data_manager.add_response("Geral", "Resposta")
        result = self.data_manager.remove_response("Geral", "Resposta")
        self.assertTrue(result)
        self.assertEqual(len(self.data_manager.data["Geral"]), 0)
    
    def test_edit_response(self):
        """Testa edição de resposta"""
        self.data_manager.add_response("Geral", "Resposta original")
        result = self.data_manager.edit_response("Geral", "Resposta original", "Resposta editada")
        self.assertTrue(result)
        self.assertEqual(self.data_manager.data["Geral"][0]["texto"], "Resposta editada")
    
    def test_duplicate_response(self):
        """Testa duplicação de resposta"""
        self.data_manager.add_response("Geral", "Resposta")
        result = self.data_manager.duplicate_response("Geral", "Resposta")
        self.assertTrue(result)
        self.assertEqual(len(self.data_manager.data["Geral"]), 2)
        self.assertEqual(self.data_manager.data["Geral"][1]["texto"], "Resposta (cópia)")


if __name__ == '__main__':
    unittest.main() 