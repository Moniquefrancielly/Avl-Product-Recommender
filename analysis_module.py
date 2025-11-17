import timeit
import random

def list_search(data_list, target_key):
    """Função de busca linear (O(n)) em uma lista simples, buscando pelo 'id'."""
    for item in data_list:
        if item['id'] == target_key: 
            return item
    return None

def run_performance_test(avl_tree, data_list, num_tests=1000):
    """
    Mede e compara o tempo de busca em Lista Simples (O(n)) e AVL Tree (O(log n)).
    """
    
    print("\n[DEBUG] Função de performance iniciada. Executando testes...")
    
    # Prepara a lista de IDs
    all_keys = [item['id'] for item in data_list] 
    
    # ... (restante da validação de num_tests) ...

    if not all_keys:
        print("🚫 Erro: Não há IDs carregados na lista para realizar o teste.")
        return
        
    test_keys = random.sample(all_keys, num_tests)
    
    # ----------------------------------------------------
    # 2. Teste 1: Lista Simples (O(n)) - SEM SETUP
    # ----------------------------------------------------
    
    # O setup é vazio. O Timer usará as variáveis passadas no 'globals'.
    stmt_list = "for k in test_keys: list_search(data_list, k)"
    
    list_timer = timeit.Timer(stmt_list, 
                              globals={'data_list': data_list, 'list_search': list_search, 'test_keys': test_keys})

    list_time = list_timer.timeit(number=1)
    
    # ----------------------------------------------------
    # 3. Teste 2: AVL Tree (O(log n)) - SEM SETUP
    # ----------------------------------------------------

    # O setup é vazio. O Timer usará as variáveis passadas no 'globals'.
    stmt_avl = "for k in test_keys: avl_tree.search_item(k)"

    avl_timer = timeit.Timer(stmt_avl, 
                             globals={'avl_tree': avl_tree, 'test_keys': test_keys})
    
    avl_time = avl_timer.timeit(number=1)
    
    # ----------------------------------------------------
    # 4. Resultados
    # ----------------------------------------------------
    
    print("\n" + "="*50)
    print("        📊 ANÁLISE DE COMPLEXIDADE (O(n) vs O(log n))")
    print("="*50)
    print(f"Número de itens no catálogo: {len(data_list)}")
    print(f"Número de buscas aleatórias testadas: {num_tests}\n")

    print(f"Busca em Lista Simples (O(n)): {list_time:.6f} segundos")
    print(f"Busca na AVL Tree (O(log n)): {avl_time:.6f} segundos\n")
    
    if avl_time < list_time:
        diferenca = (list_time - avl_time) / list_time * 100
        print(f"🏆 A AVL Tree (O(log n)) é {diferenca:.2f}% mais rápida para buscas.")
    else:
        print("⚠️ A AVL Tree foi mais lenta. Verifique o tamanho dos dados ou a implementação.")

    print("="*50)