import timeit
import random
import sys
import copy
import json
import os
from avl_tree import AVLTree
from analysis_module import list_search, list_insert, list_delete_by_id
from data_loader import load_data_from_file

# Configuração
sys.setrecursionlimit(10000)

def load_products_for_benchmark():
    """Carrega produtos para o benchmark - versão fixa"""
    print("📁 Carregando dados para análise de performance...")
    
    products = load_data_from_file('banco_data.json')
    
    # Se não tiver dados, cria 10.000 produtos de exemplo
    if not products or len(products) < 10000:
        print("⚠️  Criando 10.000 produtos de exemplo para o teste...")
        products = []
        for i in range(1, 10001):
            products.append({
                'id': i,
                'nome': f'Produto Teste {i}',
                'categoria': f'Categoria {random.randint(1, 100)}',
                'preco': round(random.uniform(10.0, 1000.0), 2)
            })
    
    return products[:10000]  # Garante 10.000 produtos

def run_fixed_benchmark():
    """Executa benchmark com parâmetros FIXOS"""
    
    # CONFIGURAÇÃO FIXA
    TOTAL_ITEMS = 10000
    TEST_OPERATIONS = 10000
    

    print("⠀⠀⠀⠀⠀⠀⠀⠀🔬 ANÁLISE DE COMPLEXIDADE - TESTE FIXO")
    print("<"*50)
    print(f"⠀⠀⠀⠀⠀⠀⠀⠀📊 Configuração: {TOTAL_ITEMS:,} itens | {TEST_OPERATIONS:,} operações")
    print("")
    
    # Carrega dados
    all_products = load_products_for_benchmark()
    
    if len(all_products) < TOTAL_ITEMS:
        print("❌ Dados insuficientes para o teste")
        return
    
    # Prepara dados
    products_sample = all_products[:TOTAL_ITEMS]
    test_keys = random.sample([p['id'] for p in products_sample], TEST_OPERATIONS)
    
    results = {}
    
    # 1. TESTE DE INSERÇÃO - 10.000 ITENS
    # =========================================================================
    print(f"\n>>> TESTE PERFORMANCE - INSERÇÃO")
    print(f"    Inserindo {TOTAL_ITEMS:,} itens...")
    
    # AVL Tree - O(log n)
    avl = AVLTree()
    start_time = timeit.default_timer()
    for item in products_sample:
        avl.insert_item(item['id'], item)
    avl_insert_time = timeit.default_timer() - start_time
    results['avl_insert'] = avl_insert_time
    
    # Lista Simples - O(1)
    data_list = []
    start_time = timeit.default_timer()
    for item in products_sample:
        list_insert(data_list, item)
    list_insert_time = timeit.default_timer() - start_time
    results['list_insert'] = list_insert_time
    
    print(f"    ✅ AVL Tree (O(log n)): {avl_insert_time:.4f} segundos")
    print(f"    ✅ Lista Simples (O(1)): {list_insert_time:.4f} segundos")
    
    # =========================================================================
    # 2. TESTE DE BUSCA - 10.000 BUSCAS  
    # =========================================================================
    print(f"\n>>> TESTE PERFORMANCE - BUSCA")
    print(f"    Executando {TEST_OPERATIONS:,} buscas...")
    
    # AVL Tree - O(log n)
    start_time = timeit.default_timer()
    for key in test_keys:
        avl.search_item(key)
    avl_search_time = timeit.default_timer() - start_time
    results['avl_search'] = avl_search_time
    
    # Lista Simples - O(n)
    start_time = timeit.default_timer()
    for key in test_keys:
        list_search(data_list, key)
    list_search_time = timeit.default_timer() - start_time  
    results['list_search'] = list_search_time
    
    print(f"    ✅ AVL Tree (O(log n)): {avl_search_time:.4f} segundos")
    print(f"    ✅ Lista Simples (O(n)): {list_search_time:.4f} segundos")
    
    # =========================================================================
    # 3. TESTE DE REMOÇÃO - 10.000 REMOÇÕES
    # =========================================================================
    print(f"\n>>> TESTE PERFORMANCE - REMOÇÃO")
    print(f"    Executando {TEST_OPERATIONS:,} remoções...")
    
    # AVL Tree - O(log n)
    avl_copy = copy.deepcopy(avl)
    start_time = timeit.default_timer()
    for key in test_keys:
        avl_copy.delete_item(key)
    avl_delete_time = timeit.default_timer() - start_time
    results['avl_delete'] = avl_delete_time
    
    # Lista Simples - O(n)
    list_copy = copy.deepcopy(data_list)
    start_time = timeit.default_timer()
    for key in test_keys:
        list_delete_by_id(list_copy, key)
    list_delete_time = timeit.default_timer() - start_time
    results['list_delete'] = list_delete_time
    
    print(f"    ✅ AVL Tree (O(log n)): {avl_delete_time:.4f} segundos")
    print(f"    ✅ Lista Simples (O(n)): {list_delete_time:.4f} segundos")
    print("\n" *6)
    
    # =========================================================================
    # RESUMO FINAL
    # =========================================================================
  
    print("⠀⠀⠀⠀⠀⠀⠀⠀📈 RESUMO DA ANÁLISE DE COMPLEXIDADE")
    print("<"*50)

    # Cálculo de performance
    if list_search_time > 0:
        search_improvement = (list_search_time - avl_search_time) / list_search_time * 100
        print(f"🎯 BUSCA: AVL é {search_improvement:+.1f}% mais rápida")
    
    if list_delete_time > 0:
        delete_improvement = (list_delete_time - avl_delete_time) / list_delete_time * 100  
        print(f"🎯 REMOÇÃO: AVL é {delete_improvement:+.1f}% mais rápida")
        print("_" *50)
    print("\n" *4)
    print("<" *50)
    
    print(f"\n💡 CONCLUSÃO: Para {TOTAL_ITEMS:,} itens:")
    print("   - AVL Tree mantém O(log n) mesmo com grande volume de dados")
    print("   - Lista Simples sofre com O(n) em buscas e remoções")
    print("   - A diferença se torna MAIS SIGNIFICATIVA com mais dados")
    print("_"*50)
    print("\n" *5)

def run_analysis_and_report():
    """Função para integrar com seu main.py"""
    try:
        run_fixed_benchmark()
        return "✅ Análise de complexidade concluída com sucesso!"
    except Exception as e:
        return f"❌ Erro durante a análise: {e}"

if __name__ == "__main__":
    run_fixed_benchmark()