from data_loader import load_data_from_file, insert_data_into_tree
from avl_tree import AVLTree
from analysis_module import run_performance_test

# 1. CARREGAMENTO DOS DADOS (Executado uma vez na inicialização)
srhp_tree = AVLTree()

data_file_path = 'banco_data.json'
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

def get_parent_selection(srhp_tree):
    """Guia o usuário através da busca e seleção da Categoria PAI usando o método O(n).
    Retorna o dicionário de dados do item pai selecionado ou None em caso de falha"""
    print("\n--- NOVO CADASTRO HIERÁRQUICO - PASSO 1 ---")

    while True:
        procura = input("Digite o NOME da Categoria PAI para pesquisar (Ex: Masculino, Calçados): ")
        results = srhp_tree.search_by_name(procura)

        if results:
             print(f"\n✅ {len(results)} Item(s) Encontrado(s). Escolha o item PAI:")
             for i, res in enumerate(results):
                print(f"  [{i+1}] ID: {res['id']} | Nome: {res.get('nome', 'N/A')} | Tipo: {res.get('tipo', 'N/A')}")
             selecao = input(f"\nSelecione o número do item [1-{len(results)}] ou 'n' para nova busca: ") 
             if selecao.lower() == 'n':  
                 continue 

             try:
                idx = int(selecao) - 1

                if 0 <= idx < len(results):
                     # Retorna o dicionário completo do item selecionado
                     selected_parent = results[idx]
                     print(f"\nPAI SELECIONADO: {selected_parent['nome']} (ID: {selected_parent['id']})")
                     return selected_parent
                else:
                    print("❌ Seleção inválida. Tente novamente.")
             except ValueError:
                print("❌ Entrada inválida. Digite apenas o número da opção.")
        else:
            print(f"🚫 Nenhuma categoria encontrada contendo '{procura}'. Tente um termo mais genérico.")
print("✅ Carregamento inicial concluído. Árvore pronta para uso!")
print(f"Raiz da árvore: {srhp_tree.root}")
print(f"Altura da árvore: {srhp_tree._get_height(srhp_tree.root)}")

# Teste uma busca por ID primeiro
test_node = srhp_tree.search_item(1)  # ID da raiz
if test_node:
    print(f"✅ Busca por ID funciona. Nó 1: {test_node.data}")
else:
    print("❌ Busca por ID NÃO funciona - problema na árvore")
        

    
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
                # --- FUNCIONALIDADE INSERÇÃO ---
                selected_parent_data = get_parent_selection(srhp_tree)

                if not selected_parent_data:
                    continue

                pai_id = selected_parent_data['id']    

                #identificação
                print("\nPASSO 2: Insira os dados do novo item a ser conectado.")
                key = get_positive_int_input(" Digite o ID ÚNICO do novo item: ")
                nome = input(" Digite o Nome/Título do Item: ")

                #definição de hierarquia
                print("\nPara onde este item vai?")

                #definição de tipo
                tipo = input(" Digite o TIPO do Item (Ex: Produto, Subcategoria, Categoria): ")

                #Monta o dicionário COMPLETO (o que a AVL vai armazenar)
                data = {
                    "id": key,
                    "nome": nome,
                    "tipo": tipo,
                    "pai_id": pai_id,
                    "descricao": input(" Descrição opcional: ")
                }
                #Insere na AVL (ID + Dicionário de Dados)
                srhp_tree.insert_item(key, data)
                print(f"✅ Item '{nome}' (ID {key}) inserido e conectado ao PAI {pai_id}.")
                
            elif choice == '2':
                # --- FUNCIONALIDADE BUSCA  ---
                print("\n--- OPÇÕES DE BUSCA ---")
                search_type = input("Buscar por (1) ID Exato ou (2) Nome/Palavra-chave? ")

                if search_type == '1':
                 key = get_positive_int_input(" Digite o ID (Key) para busca: ")
                 result = srhp_tree.search_item(key)
                 if result:
                    data_info = result.data.get('nome', 'N/A') if isinstance(result.data, dict) else str(result.data)
                    print(f"🔎 Encontrado: ID {result.key}, Nome: {data_info} (O(log n) garantido!")
                 else:
                    print(f"🚫 ID {key} não encontrado no catálogo.")

                elif search_type == '2':
                    query = input(" Digite o Nome/Palavra-chave para busca: ")
                    results = srhp_tree.search_by_name(query) # Chama o novo método O(n)

                    if results:
                        print(f"\n✅ {len(results)} item(s) encontrado(s) por '{query}' (Busca O(n:")
                        for res in results:
                            print(f"   -> ID: {res['id']} | Nome: {res.get('nome', 'N/A')} | Tipo: {res.get('tipo', 'N/A')} | PAI: {res.get('pai_id', 'N/A')}")
                    else:
                        print(f"🚫 Nenhuma categoria/produto encontrado contendo '{query}'.")
                else:
                    print("Opção inválida.") 

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
                # --- MÓDULO DE RECOMENDAÇÃO (Integr. 2) ---
                key = get_positive_int_input(" Digite o ID do produto/categoria para obter sugestões: ")
                
                print(f"\n... Buscando sugestões para o ID {key}...")
                
                # 🚀 CONEXÃO CORRETA DA LÓGICA RECURSIVA JÁ FEITA NA AVLTree
                recommendations = srhp_tree.recommend_item(key) 
                
                if recommendations:
                    print("-" * 40)
                    print(f"✅ Recomendações Encontradas ({len(recommendations)} itens):")
                    for item in recommendations:
                        # Assumindo que 'nome' e 'id' estão presentes no dicionário
                        print(f"   -> ID {item.get('id')}: {item.get('nome', 'N/A')} (Pai: {item.get('pai_id')})")
                    print("-" * 40)
                else:
                    print(f"🚫 Não foram encontradas recomendações para o ID {key} ou ele não existe.")


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