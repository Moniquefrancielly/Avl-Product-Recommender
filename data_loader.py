import json
import os 
from avl_tree import AVLTree

def load_data_into_tree(tree_instance, filename="banco_data.json"):

    if not os.path.exists(filename):
        print(f"ERRO: Arquivo de dados '{filename}' não encontrado.")
        return 0 
    print(f"🤖 Carregando dados de {filename}...")
    
    item_count = 0
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

            if isinstance(data, list):
                for item in data:
                    tree_instance.insert_item(item['id'], item['nome'])
                    item_count += 1
            

            elif isinstance(data, dict):
                pass
                
        print(f"✅ {item_count} itens inseridos na AVLTree com sucesso!")
        return item_count

    except json.JSONDecodeError:
        print("ERRO: O arquivo JSON está mal formatado ou vazio.")
        return 0
    except Exception as e:
        print(f"ERRO ao carregar dados: {e}")
        return 0

# Você pode incluir a chamada no final do arquivo (opcional)
# if __name__ == "__main__":
#     # Teste rápido de carregamento
#     from avl_tree import AVLTree # É necessário para este teste
#     temp_tree = AVLTree()
#     load_data_into_tree(temp_tree)
#     temp_tree.print_hierarchy(temp_tree.root, 0)