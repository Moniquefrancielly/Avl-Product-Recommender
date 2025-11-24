import random
from avl_tree import AVLTree
from analysis_module import run_performance_test

def test_performance_small_dataset(capfd):
    # cria dados simples
    data = [{"id": i} for i in range(500)]
    
    tree = AVLTree()
    for item in data:
        tree.insert_item(item["id"], item)

    # Executa performance (não verificamos o valor, só se roda sem erro)
    run_performance_test(tree, data, num_tests=50)

    # garante que não quebrou
    captured = capfd.readouterr()
    assert "ANÁLISE DE COMPLEXIDADE" in captured.out
