from data_loader import load_data_from_file, insert_data_into_tree
from avl_tree import AVLTree
from analysis_module import run_performance_test

# 1. CARREGAMENTO DOS DADOS (Executado uma vez na inicialização)
srhp_tree = AVLTree()

data_file_path = "Avl-Product-Recommender/banco_data.json"
print("Iniciando o Sistema de Recomendação...")
dados = load_data_from_file(data_file_path)
insert_data_into_tree(srhp_tree, dados)
print("-" * 50)
print("✅ Carregamento inicial concluído. Árvore pronta para uso!")

def get_positive_int_input(prompt):
    """Lê uma entrada do usuário e garante que seja um ID inteiro positivo."""
    while True:
        try:
            value = input(prompt)
            # Verifica se o valor é numérico e converte para inteiro
            num = int(value) 
            if num <= 0:
                print("⚠️ O ID deve ser um número inteiro positivo (maior que zero).")
            else:
                return num
        except ValueError:
            print("❌ Entrada inválida. Por favor, digite apenas números inteiros.")

def main():
    """Função principal que inicializa e executa o loop da CLI."""


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
                key = get_positive_int_input(" Digite o ID (Key) numérico: ")
                data = input("  Digite o Nome/Descrição: ")
                srhp_tree.insert_item(key, data)
                print(f"✅ Item '{data}' (ID: {key}) inserido e árvore rebalanceada.")
                
            elif choice == '2':
                # --- FUNCIONALIDADE BUSCA (Integr. 1) ---
                key = get_positive_int_input(" Digite o ID (Key) para busca: ")
                result = srhp_tree.search_item(key)
                if result:
                    print(f"🔎 Encontrado: ID {result.key}, Nome: {result.data} (AVL garantida!)")
                else:
                    print(f"🚫 ID {key} não encontrado no catálogo.")

            elif choice == '3':
                # --- FUNCIONALIDADE REMOÇÃO (Integr. 1) ---
                key = get_positive_int_input(" Digite o ID (Key)do item a ser removido: ")
                # A sua função delete deve ser encapsulada em um método público, assim como o insert:
                srhp_tree.delete_item(key)
                print(f"🗑️ Item com ID {key} removido (se existente) e árvore rebalanceada.")

            elif choice == '4':
                # --- FUNCIONALIDADE IMPRESSÃO (Integr. 1) ---
                print("\n" + "="*20 + " ESTRUTURA HIERÁRQUICA " + "="*20)
                srhp_tree.print_hierarchy(srhp_tree.root)
                print("="*64)

            elif choice == '5':
                # --- LÓGICA DE NEGÓCIO (Responsabilidade Integr. 2) ---
                key = get_positive_int_input(" Digite o ID do produto/categoria para obter sugestões: ")
                # O Integrante 2 implementará este método na AVLTree
                # recommendations = srhp_tree.recommend_products_item(key) 
                
                print("\n... Chamada para o Módulo de Recomendação Recursiva ...")
                # EXEMPLO DE CHAMADA, DEPENDENDO DA IMPLEMENTAÇÃO DO Integr. 2:
                # if srhp_tree.root:
                #    srhp_tree.recommend_products(srhp_tree.root, key) 
                print("⏳ Módulo em desenvolvimento. Integrante 2 deve conectar a lógica recursiva aqui.")


            elif choice == '6':

                print("\n--- INICIANDO TESTES DE COMPLEXIDADE BIG-O ---")
                # Chama a função de análise, passando a árvore e a lista de dados
                run_performance_test(srhp_tree, dados)
                print("--- ANÁLISE CONCLUÍDA ---")
                
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