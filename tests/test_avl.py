import pytest
from avl_tree import AVLTree
from node import Node

# ---------------------------
# TESTES BÁSICOS DE INSERÇÃO
# ---------------------------

def test_insert_single_node():
    tree = AVLTree()
    tree.insert_item(10, {"id": 10, "nome": "Item A", "pai_id": 0})
    assert tree.root.key == 10
    assert tree.root.data["nome"] == "Item A"

def test_insert_duplicate_key():
    tree = AVLTree()
    tree.insert_item(10, {"id": 10, "nome": "Item A", "pai_id": 0})
    tree.insert_item(10, {"id": 10, "nome": "Item B", "pai_id": 0})
    # Chave duplicada NÃO deve criar novos nós
    assert tree.root.data["nome"] == "Item A"

# ---------------------------
# TESTES DE BUSCA
# ---------------------------

def test_search_existing():
    tree = AVLTree()
    tree.insert_item(5, {"id": 5, "nome": "Item", "pai_id": 0})
    assert tree.search_item(5).key == 5

def test_search_nonexistent():
    tree = AVLTree()
    tree.insert_item(5, {"id": 5, "nome": "Item", "pai_id": 0})
    assert tree.search_item(99) is None

# ---------------------------
# TESTE DELETAR EM CENÁRIOS
# ---------------------------

def test_delete_root_only_node():
    tree = AVLTree()
    tree.insert_item(10, {"id": 10})
    tree.delete_item(10)
    assert tree.root is None

def test_delete_root_with_two_children():
    tree = AVLTree()
    tree.insert_item(10, {"id": 10})
    tree.insert_item(5, {"id": 5})
    tree.insert_item(15, {"id": 15})

    tree.delete_item(10)
    # A raiz deve ser substituída pelo sucessor
    assert tree.root.key in (5, 15)

# ---------------------------
# TESTES DE BALANCEAMENTO
# ---------------------------

def test_tree_is_balanced_after_many_insertions():
    tree = AVLTree()
    for i in range(1, 1000):
        tree.insert_item(i, {"id": i})

    height = tree._get_height(tree.root)
    # Em AVL, a altura deve ser O(log n)
    assert height < 30     # log2(1000) ≈ 10, com margem de segurança

# ---------------------------
# TESTE DE BUSCA POR NOME (O(n))
# ---------------------------

def test_search_by_name():
    tree = AVLTree()
    tree.insert_item(1, {"id": 1, "nome": "Camisa Azul", "pai_id": 0})
    tree.insert_item(2, {"id": 2, "nome": "Calça", "pai_id": 0})
    tree.insert_item(3, {"id": 3, "nome": "Camiseta Vermelha", "pai_id": 0})

    results = tree.search_by_name("cami")
    assert len(results) == 2

# ---------------------------
# TESTE DE PERFORMANCE (10k + 100k)
# ---------------------------

def test_insert_10000_items(benchmark):
    def insert_items():
        tree = AVLTree()
        for i in range(1, 10001):
            tree.insert_item(i, {"id": i})
        return tree

    tree = benchmark(insert_items)
    assert tree._get_height(tree.root) < 40  # ainda O(log n)

# ---------------------------
# TESTE DE RECOMENDAÇÃO
# ---------------------------

def test_recommendation_basic():
    tree = AVLTree()

    tree.insert_item(1, {"id": 1, "nome": "Pai", "pai_id": 0})
    tree.insert_item(2, {"id": 2, "nome": "Filho A", "pai_id": 1})
    tree.insert_item(3, {"id": 3, "nome": "Filho B", "pai_id": 1})
    tree.insert_item(4, {"id": 4, "nome": "Outro", "pai_id": 0})

    rec = tree.recommend_item(2, limit=3)

    # deve sugerir irmão primeiro
    ids = [r["id"] for r in rec]
    assert 3 in ids

def test_avl_ll_rotation():
    tree = AVLTree()
    tree.insert_item(30, {})
    tree.insert_item(20, {})
    tree.insert_item(10, {})
    assert tree.root.key == 20
def test_avl_rr_rotation():
    tree = AVLTree()
    tree.insert_item(10, {})
    tree.insert_item(20, {})
    tree.insert_item(30, {})
    assert tree.root.key == 20
def test_avl_lr_rotation():
    tree = AVLTree()
    tree.insert_item(30, {})
    tree.insert_item(10, {})
    tree.insert_item(20, {})
    assert tree.root.key == 20
def test_avl_rl_rotation():
    tree = AVLTree()
    tree.insert_item(10, {})
    tree.insert_item(30, {})
    tree.insert_item(20, {})
    assert tree.root.key == 20
def test_avl_delete_two_children():
    tree = AVLTree()
    tree.insert_item(20, {})
    tree.insert_item(10, {})
    tree.insert_item(30, {})
    tree.insert_item(25, {})
    tree.insert_item(40, {})

    tree.delete_item(20)
    assert tree.search_item(20) is None
def test_avl_delete_rebalance():
    tree = AVLTree()
    for x in [50, 30, 70, 20, 40, 60, 80]:
        tree.insert_item(x, {})

    tree.delete_item(20)
    assert tree.root.key == 50

