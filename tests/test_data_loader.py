import json
import os
import pytest
from data_loader import load_data_from_file, insert_data_into_tree
from avl_tree import AVLTree

def test_load_valid_file(tmp_path):
    # cria arquivo temporário JSON válido
    data = [{"id": 1, "nome": "Teste"}]
    file = tmp_path / "dados.json"
    file.write_text(json.dumps(data), encoding="utf-8")

    result = load_data_from_file(str(file))
    assert len(result) == 1
    assert result[0]["nome"] == "Teste"

def test_load_invalid_json(tmp_path):
    file = tmp_path / "dados.json"
    file.write_text("{invalido}", encoding="utf-8")

    result = load_data_from_file(str(file))
    assert result == []

def test_insert_data_into_tree():
    dados = [
        {"id": 1, "nome": "A"},
        {"id": 2, "nome": "B", "pai_id": 1},
    ]

    arvore = AVLTree()
    insert_data_into_tree(arvore, dados)

    assert arvore.search_item(1) is not None
    assert arvore.search_item(2) is not None
def test_load_nonexistent_file():
    result = load_data_from_file("arquivo_que_nao_existe.json")
    assert result == []
def test_load_invalid_json(tmp_path):
    file = tmp_path / "bad.json"
    file.write_text("{não é json}", encoding="utf-8")

    data = load_data_from_file(str(file))
    assert data == []

def test_load_nonexistent_file():
    # arquivo não existe → deve retornar []
    result = load_data_from_file("nao_existe_123456.json")
    assert result == []

def test_load_invalid_json(tmp_path):
    # cria um arquivo inválido
    file = tmp_path / "invalido.json"
    file.write_text("{isso não é json}", encoding="utf-8")

    result = load_data_from_file(str(file))
    assert result == []

def test_load_unexpected_error(monkeypatch, tmp_path):
    file = tmp_path / "dummy.json"
    file.write_text("[]")  # válido, mas vamos simular erro

    # força um erro inesperado
    def fake_open(*args, **kwargs):
        raise RuntimeError("Erro inesperado")

    monkeypatch.setattr("builtins.open", fake_open)

    result = load_data_from_file(str(file))
    assert result == []  # em caso de erro → retorna []