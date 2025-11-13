from node import Node

class AVLTree:
    """
    Classe central para gerenciar a Árvore AVL. 
    Implementa as lógicas de balanceamento, inserção, busca e remoção recursivas.
    Complexidade das operações principais: O(log n).
    """

    def __init__(self):
        """Inicializa a árvore com a raiz como None."""
        self.root = None
        self.comparison_count = 0 # Contador para análise de complexidade

    # --- MÉTODOS AUXILIARES O(1) ---

    def _get_height(self, node):
        """Calcula a altura de um nó. Retorna 0 se o nó for None."""
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        """Calcula o Fator de Balanceamento (FB): Altura_Esq - Altura_Dir."""
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    # --- MÉTODOS DE BALANCEAMENTO (ROTAÇÕES) O(1) ---

    def _rotate_right(self, z):
        """Executa a Rotação Simples à Direita (LL)."""
        y = z.left
        T2 = y.right

        # Realiza a rotação
        y.right = z
        z.left = T2

        # Atualiza as alturas (do nó mais baixo para o mais alto)
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def _rotate_left(self, z):
        """Executa a Rotação Simples à Esquerda (RR)."""
        y = z.right
        T2 = y.left

        # Realiza a rotação
        y.left = z
        z.right = T2

        # Atualiza as alturas
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    # --- OPERAÇÕES PRINCIPAIS RECURSIVAS O(log n) ---

    def insert(self, root, key, data):
        """
        Método RECURSIVO de inserção. 
        Encontra a posição, insere e rebalanceia no retorno da recursão.
        """
        # 1. PASSO RECURSIVO BASE: Inserção do novo nó.
        if not root:
            return Node(key, data)

        # 2. NAVEGAÇÃO RECURSIVA: Encontra a posição.
        if key < root.key:
            root.left = self.insert(root.left, key, data)
        elif key > root.key:
            root.right = self.insert(root.right, key, data)
        else:
            # Chaves duplicadas não são permitidas
            return root

        # 3. RETORNO DA RECURSÃO: Atualiza altura e verifica balanceamento.
        root.height = 1 + max(self._get_height(root.left), self._get_height(root.right))
        balance = self._get_balance(root)

        # 4. REBALANCEAMENTO (Rotações)
        
        # Caso 1: Left Left (LL)
        if balance > 1 and key < root.left.key:
            return self._rotate_right(root)

        # Caso 2: Right Right (RR)
        if balance < -1 and key > root.right.key:
            return self._rotate_left(root)

        # Caso 3: Left Right (LR)
        if balance > 1 and key > root.left.key:
            root.left = self._rotate_left(root.left)
            return self._rotate_right(root)

        # Caso 4: Right Left (RL)
        if balance < -1 and key < root.right.key:
            root.right = self._rotate_right(root.right)
            return self._rotate_left(root)

        return root

    def search(self, root, key):
        """
        Método RECURSIVO de busca. 
        Retorna o Nó se a chave for encontrada, ou None.
        """
        self.comparison_count += 1
        # Caso base: A chave não está presente ou o nó é encontrado.
        if not root or root.key == key:
            return root

        # Navegação recursiva
        if key < root.key:
            return self.search(root.left, key)
        else:
            return self.search(root.right, key)

    def _get_min_value_node(self, node):
        """Função auxiliar para encontrar o nó com o menor valor na subárvore (sucessor in-order)."""
        current = node
        # Loop para encontrar a folha mais à esquerda
        while current.left is not None:
            current = current.left
        return current

    def delete(self, root, key):
        """
        Método RECURSIVO de remoção. 
        Remove o nó e rebalanceia a árvore no retorno da recursão.
        """
        # 1. PASSO RECURSIVO BASE: Se a raiz for None, retorna.
        if not root:
            return root

        # 2. NAVEGAÇÃO RECURSIVA: Encontra o nó a ser removido.
        if key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            # Nó com a chave encontrada.
            
            # Caso 1: Nó com 0 ou 1 filho.
            if root.left is None:
                temp = root.right
                root = None # Libera o nó (em Python, é removido pelo Garbage Collector)
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            
            # Caso 2: Nó com 2 filhos.
            # Encontra o sucessor in-order (menor valor na subárvore direita).
            temp = self._get_min_value_node(root.right)
            
            # Copia o conteúdo (chave e dados) do sucessor para o nó atual.
            root.key = temp.key
            root.data = temp.data
            
            # Deleta o sucessor (agora na subárvore direita) de forma recursiva.
            root.right = self.delete(root.right, temp.key)

        # Se a árvore tem apenas 1 nó, retorna a raiz.
        if root is None:
            return root

        # 3. RETORNO DA RECURSÃO: Atualiza altura e verifica balanceamento.
        root.height = 1 + max(self._get_height(root.left), self._get_height(root.right))
        balance = self._get_balance(root)

        # 4. REBALANCEAMENTO (Quatro casos de rotação como na inserção)
        
        # Caso 1: Left Left (LL)
        if balance > 1 and self._get_balance(root.left) >= 0:
            return self._rotate_right(root)

        # Caso 2: Left Right (LR)
        if balance > 1 and self._get_balance(root.left) < 0:
            root.left = self._rotate_left(root.left)
            return self._rotate_right(root)

        # Caso 3: Right Right (RR)
        if balance < -1 and self._get_balance(root.right) <= 0:
            return self._rotate_left(root)

        # Caso 4: Right Left (RL)
        if balance < -1 and self._get_balance(root.right) > 0:
            root.right = self._rotate_right(root.right)
            return self._rotate_left(root)

        return root

    # --- OUTROS REQUISITOS (Exemplo de Impressão Hierárquica) ---

    def print_hierarchy(self, root, level=0):
        """
        Implementa a impressão hierárquica (in-order modificada).
        Demonstra o uso de RECURSIVIDADE para navegação.
        """
        if root:
            # Navega para a subárvore direita
            self.print_hierarchy(root.right, level + 1)

            # Imprime o nó atual com a indentação do nível
            print("    " * level + f"-> [{root.key}] {root.data} (H: {root.height}, FB: {self._get_balance(root)})")

            # Navega para a subárvore esquerda
            self.print_hierarchy(root.left, level + 1)