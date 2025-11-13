import sys
# Adiciona o diretório atual ao path para garantir que as importações funcionem 
# se você não tiver feito 'pip install -e .' ou configurado o ambiente.
# Este é um truque comum em projetos pequenos.
sys.path.append('.') 

from avl_tree import AVLTree
from data_loader import load_data_into_tree 
# Assumimos que o Integrante 2 colocará a lógica de recomendação na AVLTree.
# Se ele criar um módulo separado (ex: recommendation_module), importe-o aqui.

def main():
    """Função principal que inicializa e executa o loop da CLI."""
    srhp_tree = AVLTree()
    
    # --- 1. CARREGAMENTO INICIAL DOS DADOS (Obrigatório) ---
    print("\n--- INICIALIZAÇÃO DO SISTEMA DE RECOMENDAÇÃO SRHP ---")
    load_data_into_tree(srhp_tree) # Carrega os 10.000 itens do banco_data.json
    print("-" * 50)
    
    while True:
        # --- 2. MENU DE INTERAÇÃO (Entrada e Saída) ---
        print("\n--- MENU SRHP - Catálogo AVL ---")
        print("1. Inserir Nova Categoria/Produto (O(log n))")
        print("2. Buscar Categoria/Produto (O(log n))")
        print("3. Remover Categoria/Produto (O(log n))")
        print("4. Visualizar Estrutura Hierárquica")
        print("5. Módulo de Recomendação (Integr. 2)")
        print("6. Módulo de Análise de Complexidade (Integr. 3)")
        print("7. Sair")
        
        choice = input("\nEscolha uma opção: ")

        try:
            if choice == '1':
                # --- FUNCIONALIDADE INSERÇÃO (Integr. 1) ---
                key = int(input("  Digite o ID (Key) numérico: "))
                data = input("  Digite o Nome/Descrição: ")
                srhp_tree.insert_item(key, data)
                print(f"✅ Item '{data}' (ID: {key}) inserido e árvore rebalanceada.")
                
            elif choice == '2':
                # --- FUNCIONALIDADE BUSCA (Integr. 1) ---
                key = int(input("  Digite o ID (Key) para busca: "))
                result = srhp_tree.search_item(key)
                if result:
                    print(f"🔎 Encontrado: ID {result.key}, Nome: {result.data} (AVL garantida!)")
                else:
                    print(f"🚫 ID {key} não encontrado no catálogo.")

            elif choice == '3':
                # --- FUNCIONALIDADE REMOÇÃO (Integr. 1) ---
                key = int(input("  Digite o ID (Key) do item a ser removido: "))
                # A sua função delete deve ser encapsulada em um método público, assim como o insert:
                srhp_tree.root = srhp_tree.delete(srhp_tree.root, key)
                print(f"🗑️ Item com ID {key} removido (se existente) e árvore rebalanceada.")

            elif choice == '4':
                # --- FUNCIONALIDADE IMPRESSÃO (Integr. 1) ---
                print("\n" + "="*20 + " ESTRUTURA HIERÁRQUICA " + "="*20)
                srhp_tree.print_hierarchy(srhp_tree.root)
                print("="*64)

            elif choice == '5':
                # --- LÓGICA DE NEGÓCIO (Responsabilidade Integr. 2) ---
                key = int(input("  ID do produto/categoria para obter sugestões: "))
                # O Integrante 2 implementará este método na AVLTree
                # recommendations = srhp_tree.recommend_products_item(key) 
                
                print("\n... Chamada para o Módulo de Recomendação Recursiva ...")
                # EXEMPLO DE CHAMADA, DEPENDENDO DA IMPLEMENTAÇÃO DO Integr. 2:
                # if srhp_tree.root:
                #    srhp_tree.recommend_products(srhp_tree.root, key) 
                print("⏳ Módulo em desenvolvimento. Integrante 2 deve conectar a lógica recursiva aqui.")


            elif choice == '6':
                # --- ANÁLISE DE DESEMPENHO (Responsabilidade Integr. 3) ---
                print("\n... Chamada para o Módulo de Análise de Complexidade ...")
                # O Integrante 3 fará a medição de tempo e a comparação O(n) vs O(log n)
                # Exemplo: analysis_module.run_performance_test(srhp_tree, 10000)
                print("⏳ Módulo em desenvolvimento. Integrante 3 deve implementar a comparação Big-O aqui.")

            elif choice == '7':
                print("👋 Encerrando o Sistema de Recomendação SRHP. Trabalho em equipe concluído!")
                break
                
            else:
                print("❌ Opção inválida. Por favor, escolha um número de 1 a 7.")

        except ValueError:
            print("❌ Entrada inválida. Por favor, digite um número inteiro.")
        except Exception as e:
            print(f"❌ Ocorreu um erro inesperado: {e}")


if __name__ == "__main__":
    main()