import json
import os 
from avl_tree import AVLTree
# ----------------------------------------------------------------------
# 1. FUNÇÃO DE LEITURA (Encapsulamento de I/O)
# ----------------------------------------------------------------------

def load_data_from_file(file_path: str) -> list:
    """
    Lê o conteúdo do arquivo JSON especificado.
    
    Args:
        file_path: O caminho para o arquivo de dados (e.g., 'banco_data.json').
        
    Returns:
        Uma lista contendo os itens lidos do arquivo.
    """
    if not os.path.exists(file_path):
        print(f"ERRO: Arquivo {file_path} não encontrado.")
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"✅ Dados carregados com sucesso do arquivo: {file_path}. Total de {len(data)} itens.")
            return data
    except json.JSONDecodeError:
        print(f"ERRO: O arquivo {file_path} não é um JSON válido.")
        return []
    except Exception as e:
        print(f"ERRO inesperado ao ler o arquivo: {e}")
        return []

# ----------------------------------------------------------------------
# 2. FUNÇÃO DE INSERÇÃO (Encapsulamento de Lógica AVL)
# ----------------------------------------------------------------------

def insert_data_into_tree(tree: AVLTree, data: list):
    """
    Insere uma lista de itens na árvore AVL usando o método insert_item.
    
    Args:
        tree: A instância da AVLTree a ser preenchida.
        data: A lista de dicionários contendo os itens.
    """
    if not data:
        print("Nenhum dado para inserir na árvore.")
        return

    print("Iniciando a inserção dos dados na AVL Tree...")
    
    # Assumindo que cada item tem um 'id' (chave) e 'data' (payload)
    for item in data:
        try:
            key = item['id']   
            payload = item['nome'] 
            tree.insert_item(key, payload)
        except KeyError as e:
            # Captura erro se o formato dos dados estiver errado
            print(f"AVISO: Item ignorado devido à chave ausente: {e} no item {item}")
        except Exception as e:
            # Captura qualquer outro erro de inserção na AVL
            print(f"ERRO ao inserir item com chave {key}: {e}")

    print("✅ Inserção concluída.")