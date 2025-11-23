import time

class RecursionCounter:
    """Contador de chamadas recursivas"""
    
    def __init__(self):
        self.count = 0
        self.max_depth = 0
        self.current_depth = 0
    
    def reset(self):
        self.count = 0
        self.max_depth = 0
        self.current_depth = 0
    
    def enter_recursion(self):
        self.count += 1
        self.current_depth += 1
        if self.current_depth > self.max_depth:
            self.max_depth = self.current_depth
    
    def exit_recursion(self):
        self.current_depth -= 1

# Instância global do contador
recursion_counter = RecursionCounter()

def analyze_recursion_performance(avl_tree, test_data):
    """
    Analisa a recursividade nas operações da AVL Tree
    """
    print("\n" + ">•"*40)
    print("           🔍 ANÁLISE DE RECURSIVIDADE - AVL TREE")
    print("="*60)
    
    results = {}
    
    # Teste de inserção recursiva
    print(f"\n>>> ANALISANDO RECURSIVIDADE - INSERÇÃO")
    recursion_counter.reset()
    
    # Instrumentar a árvore para contar recursão
    original_insert = avl_tree._insert
    def instrumented_insert(node, key, value):
        recursion_counter.enter_recursion()
        result = original_insert(node, key, value)
        recursion_counter.exit_recursion()
        return result
    
    avl_tree._insert_recursive = instrumented_insert
    
    # Executar inserções de teste
    test_items = test_data[:100]  # Usa 100 itens para teste
    for item in test_items:
        avl_tree.insert_item(item['id'], item)
    
    results['insert_calls'] = recursion_counter.count
    results['insert_max_depth'] = recursion_counter.max_depth
    results['insert_avg_depth'] = recursion_counter.count / len(test_items) if test_items else 0
    
    print(f"    📞 Chamadas recursivas totais: {recursion_counter.count:,}")
    print(f"    📊 Profundidade máxima: {recursion_counter.max_depth}")
    print(f"    📈 Profundidade média por inserção: {results['insert_avg_depth']:.2f}")
    time.sleep(6)
    
    # Teste de busca recursiva
    print(f"\n>>> ANALISANDO RECURSIVIDADE - BUSCA")
    recursion_counter.reset()
    
    original_search = avl_tree._search
    def instrumented_search(node, key):
        recursion_counter.enter_recursion()
        result = original_search(node, key)
        recursion_counter.exit_recursion()
        return result
    
    avl_tree._search = instrumented_search
    
    # Executar buscas de teste
    test_keys = [item['id'] for item in test_items]
    for key in test_keys:
        avl_tree.search_item(key)
    
    results['search_calls'] = recursion_counter.count
    results['search_max_depth'] = recursion_counter.max_depth
    results['search_avg_depth'] = recursion_counter.count / len(test_keys) if test_keys else 0
    
    print(f"    📞 Chamadas recursivas totais: {recursion_counter.count:,}")
    print(f"    📊 Profundidade máxima: {recursion_counter.max_depth}")
    print(f"    📈 Profundidade média por busca: {results['search_avg_depth']:.2f}")
    
    # Restaurar métodos originais
    avl_tree._insert = original_insert
    avl_tree._search = original_search
    
    return results
time.sleep(6)

def print_recursion_complexity():
    """
    Explica a complexidade da recursividade na AVL Tree
    """
    print("\n" + ">•"*40)
    print("           🧠 COMPLEXIDADE DA RECURSIVIDADE")
    print("•<"*40)
    
    print("\n🎯 POR QUE RECURSIVIDADE É EFICIENTE EM AVL:")
    print("   ✅ Divide o problema pela metade a cada chamada")
    print("   ✅ Complexidade O(log n) garante performance")
    print("   ✅ Natural para estruturas hierárquicas (árvores)")
    
    print("\n💡 VANTAGENS NA IMPLEMENTAÇÃO:")
    print("   • Código mais limpo e legível")
    print("   • Alinhado com a natureza hierárquica das árvores")
    print("   • Facilita implementação de balanceamento")