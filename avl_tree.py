from node import Node
import unicodedata

class AVLTree:

    def __init__(self):
        
        self.root = None
        self.comparison_count = 0 

    # --- MÉTODOS PÚBLICOS (Interface para main.py) ---
    # Estes métodos são chamados externamente e gerenciam a recursão interna.

    def insert_item(self, key, data):
        """Método público que inicia e gerencia a recursão de inserção."""
        self.root = self._insert(self.root, key, data)

    def search_item(self, key):
        """Método público que inicia a busca."""
        # Limpa o contador de comparações e chama a função recursiva
        self.comparison_count = 0 
        return self._search(self.root, key)
    
    def search_by_name(self, query):
        """Busca um produto ou categoria pelo nome/palavra-chave.
    Esta é uma busca O(n) necessária para usabilidade.
    Retorna uma lista de dicionários encontrados."""
        if not self.root:
            return []
        normalized_query = self._normalize_string(query) 
        matches = []
        #Inicia a busca recursiva do nó raiz
        self._find_all_matches(self.root, normalized_query, matches)
        return matches

    def delete_item(self, key):
        """Método público que inicia e gerencia a remoção."""
        self.root = self._delete(self.root, key)
    
    def recommend_item(self, key, limit=5):
        """Método público para recomendação."""
        # Chama o método recommend
        return self.recommend(key, limit)

    # ----------------------------------------------------------------------
    # --- MÉTODOS AUXILIARES O(1) ---

    def _get_height(self, node):
        """Retorna a altura do nó (0 se for None)."""
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):    
        """Calcula o Fator de Balanceamento (FB) de um nó."""
        if not node:
           return 0
        return self._get_height(node.left) - self._get_height(node.right)
    
    def _normalize_string(self, text):
        """Remove acentos e caracteres diacríticos, e converte para minúsculas."""
        if not isinstance(text, str):
            return ""
        
        # Remove acentos e converte para minúsculas
        text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8")
        return text.lower()

    # ----------------------------------------------------------------------
    # --- MÉTODOS DE BALANCEAMENTO (ROTAÇÕES) O(1) ---

    def _rotate_right(self, z):
        y = z.left
        T2 = y.right

        y.right = z
        z.left = T2

        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def _rotate_left(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    # ----------------------------------------------------------------------
    # --- OPERAÇÕES PRINCIPAIS RECURSIVAS O(log n) ---

    def _insert(self, root, key, data):
        """Método recursivo para inserção e balanceamento."""
        key = int(key)
        
        if not root:
            return Node(key, data)
        root.key = int(root.key)

        if key < root.key:
            root.left = self._insert(root.left, key, data)
        elif key > root.key:
            root.right = self._insert(root.right, key, data)
        else:
            return root

        # Atualiza altura e calcula balanceamento
        root.height = 1 + max(self._get_height(root.left), self._get_height(root.right))
        balance = self._get_balance(root)

        # Rotações (casos de desbalanceamento)
        if balance > 1 and key < root.left.key:
            return self._rotate_right(root)

        if balance < -1 and key > root.right.key:
            return self._rotate_left(root)

        if balance > 1 and key > root.left.key:
            root.left = self._rotate_left(root.left)
            return self._rotate_right(root)

        if balance < -1 and key < root.right.key:
            root.right = self._rotate_right(root.right)
            return self._rotate_left(root)

        return root

    def _search(self, root, key):
        """Método recursivo para busca."""

        if root is None:
            return None
        try:
            key = int(key)
            node_key = int(root.key)
        except:
            node_key = root.key
    
        self.comparison_count += 1
        if node_key == key:
            return root
        if key < node_key:
            return self._search(root.left, key)
        else:
            return self._search(root.right, key)

    def _get_min_value_node(self, node):
        """Encontra o nó com o menor valor na subárvore (mais à esquerda)."""
        current = node
        while current.left is not None:
            current = current.left
        return current
    
    def _find_all_matches(self, root, normalized_query, matches):
        """Método recursivo para fazer um percorrimento completo (O(n)) na árvore."""
        if root is None:
            return
        #Percorre sub árvore esquerda
        self._find_all_matches(root.left, normalized_query, matches)

        # Verifica nó atual
        if hasattr(root, 'data') and isinstance(root.data, dict):
           item_name = root.data.get('nome')
           if item_name:
              try:
               item_name_normalized = self._normalize_string(item_name)
               if normalized_query in item_name_normalized:
                matches.append(root.data)
              except Exception as e:
               # Se houver erro em algum nó, continua com os próximos
               print(f"⚠️  Erro ao processar nó {root.key}: {e}")
        pass        
        
        self._find_all_matches(root.right, normalized_query, matches)

    def _delete(self, root, key):
        """Método recursivo para deleção e balanceamento."""
        if not root:
            return root

        if key < root.key:
            root.left = self._delete(root.left, key)
        elif key > root.key:
            root.right = self._delete(root.right, key)
        else:
            # Caso de 0 ou 1 filho
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            
            # Caso de 2 filhos: encontra o sucessor in-order
            temp = self._get_min_value_node(root.right)
            
            # Copia o conteúdo do sucessor para o nó atual
            root.key = temp.key
            root.data = temp.data
            
            # Remove o sucessor (que agora está na subárvore direita)
            root.right = self._delete(root.right, temp.key)

        if root is None:
            return root

        # Atualiza altura e calcula balanceamento após a deleção
        root.height = 1 + max(self._get_height(root.left), self._get_height(root.right))
        balance = self._get_balance(root)

        # Rotações (casos de desbalanceamento)
        if balance > 1 and self._get_balance(root.left) >= 0:
            return self._rotate_right(root)

        if balance > 1 and self._get_balance(root.left) < 0:
            root.left = self._rotate_left(root.left)
            return self._rotate_right(root)

        if balance < -1 and self._get_balance(root.right) <= 0:
            return self._rotate_left(root)

        if balance < -1 and self._get_balance(root.right) > 0:
            root.right = self._rotate_right(root.right)
            return self._rotate_left(root)

        return root

    # ----------------------------------------------------------------------
    # --- IMPRESSÃO HIERÁRQUICA ---

    def print_hierarchy(self, root, level=0):
        """Imprime a árvore de forma hierárquica (In-Order reverso)."""
        if root:
            self.print_hierarchy(root.right, level + 1)
            print("    " * level + f"-> [{root.key}] {root.data.get('nome', 'N/A')} (H: {root.height}, FB: {self._get_balance(root)})")
            self.print_hierarchy(root.left, level + 1) 

    # ----------------------------------------------------------------------
    # --- MÉTODOS AUXILIARES DE RECOMENDAÇÃO O(log n) ---

    def _get_inorder_successor(self, node):
        """Encontra o nó com a chave imediatamente MAIOR (sucessor in-order). O(log n)."""
        if node is None:
            return None
        
        current = node.right
        while current and current.left:
            current = current.left
        return current

    def _get_inorder_predecessor(self, node):
        """Encontra o nó com a chave imediatamente MENOR (predecessor in-order). O(log n)."""
        if node is None:
            return None

        current = node.left
        while current and current.right:
            current = current.right
        return current
    
    # ----------------------------------------------------------------------
    # --- NOVO MÉTODO: BUSCA HIERÁRQUICA RECURSIVA O(n) ---

    def _find_by_parent_id(self, root, target_parent_id, recommendations, original_key):
        """
        Função auxiliar recursiva (In-Order) para coletar itens que compartilham 
        o mesmo 'pai_id'. Complexidade O(n) (varredura completa).
        """
        if root is None:
            return
        
        stack = [root]
        while stack:
            current_node = stack.pop()

            if isinstance(current_node.data, dict) and 'pai_id' in current_node.data:
                try:
                    item_pai_id = int(current_node.data['pai_id']) 
                except (ValueError, TypeError):
                     item_pai_id = -1 
                if item_pai_id == target_parent_id:
                    # Evita recomendar o próprio item buscado
                    if current_node.key != original_key:
                        recommendations.append(current_node.data)

            if current_node.right:
                stack.append(current_node.right)
            if current_node.left:
                stack.append(current_node.left)

    # ----------------------------------------------------------------------
    # --- MÉTODO PRINCIPAL DE RECOMENDAÇÃO (VERSÃO FINAL) ---

    def recommend(self, key, limit=5):
        """
        Combina recomendação hierárquica (recursiva, O(n)) com recomendação 
        por vizinhança AVL (in-order, O(log n) por passo).
        """
        target_node = self.search_item(key)
        if not target_node or not isinstance(target_node.data, dict):
            print(f"Item com ID {key} não encontrado ou com dados inválidos para recomendação.")
            return []
        
        recommendations = []
        target_data = target_node.data

        # 1. Busca o nó alvo (O(log n))
        target_node = self._search(self.root, key)
        
        if not target_node:
            print(f"Item com ID {key} não encontrado para recomendação.")
            return []

        recommendations = []
        
        # 2. Recomendação por Hierarquia (Forte) - O(n)
        target_parent_id = target_node.data.get('pai_id')
        try:
               target_parent_id = int(target_parent_id)
        except (ValueError, TypeError):
            target_parent_id = 0
        
        if target_parent_id > 0:
            recommendation_target = target_parent_id
            print(f"... Buscando IRMÃOS (mesmo PAI ID: {recommendation_target}) ...")

        else:
            recommendation_target = key
            print(f"... Buscando FILHOS (PAI ID: {recommendation_target}) ...")

        self._find_by_parent_id(self.root, recommendation_target, recommendations, key)
            
        # Retorna se a busca hierárquica já preencheu ou excedeu o limite
        if len(recommendations) >= limit:
             return recommendations[:limit] 

        # 3. Recomendação por Vizinhança (Fraca/Completa) - O(log n) por item
        
        # 3.1. Sucessores (Itens com ID ligeiramente maior)
        current_suc = target_node
        while len(recommendations) < limit:
            successor = self._get_inorder_successor(current_suc)
            if successor is None: break

            # Garante que o item não foi incluído antes e é adicionado à lista
            if successor.data not in recommendations:
                recommendations.append(successor.data) 
            
            current_suc = successor
        
        # 3.2. Predecessores (Itens com ID ligeiramente menor)
        current_pred = target_node
        while len(recommendations) < limit:
            predecessor = self._get_inorder_predecessor(current_pred)

            if predecessor is None: break
            
            # Garante que o item não foi incluído antes
            if predecessor.data not in recommendations:
                recommendations.append(predecessor.data)
            
            current_pred = predecessor
            
        return recommendations[:limit]
    
    