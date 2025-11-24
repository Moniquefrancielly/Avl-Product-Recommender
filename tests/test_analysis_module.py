import pytest
from avl_tree import AVLTree
from analysis_module import run_performance_test

def test_performance_empty_list(capfd):
    """
    Deve exibir erro quando a lista de dados está vazia.
    """
    tree = AVLTree()
    
    run_performance_test(tree, [], num_tests=10)

    out = capfd.readouterr().out
    assert "Erro" in out or "🚫" in out


def test_performance_num_tests_larger_than_list(capfd):
    """
    Verifica se o módulo trata corretamente quando num_tests > número de IDs disponíveis.
    """
    data = [{"id": 1}]
    tree = AVLTree()
    tree.insert_item(1, data[0])

    run_performance_test(tree, data, num_tests=10)

    out = capfd.readouterr().out

    # Deve indicar que a análise rodou normalmente
    assert "ANÁLISE DE COMPLEXIDADE" in out

    # E deve exibir um aviso de ajuste
    assert "Ajustando" in out or "⚠️" in out


def test_performance_tree_only(capfd):
    """
    Verifica execução normal com árvore populada.
    """
    tree = AVLTree()
    data = [{"id": i} for i in range(5)]

    for item in data:
        tree.insert_item(item["id"], item)

    run_performance_test(tree, data, num_tests=3)

    out = capfd.readouterr().out
    assert "O(log n)" in out
    assert "ANÁLISE DE COMPLEXIDADE" in out


def test_performance_stress_small(capfd):
    """
    Caso simples apenas para cobrir mais caminhos do módulo.
    """
    tree = AVLTree()
    data = [{"id": i} for i in range(3)]

    for item in data:
        tree.insert_item(item["id"], item)

    run_performance_test(tree, data, num_tests=2)

    out = capfd.readouterr().out

    # precisa aparecer informações básicas do relatório
    assert "Número de itens no catálogo" in out
    assert "Número de buscas aleatórias testadas" in out
