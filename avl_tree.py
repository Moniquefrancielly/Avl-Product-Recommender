from node import Node

class AVLTree:

   def __init__(self):
        
        self.root = None
        self.comparison_count = 0 
# --- MÉTODOS PÚBLICOS (Interface para main.py) ---

   def insert_item(self, key, data):
     """Método público que inicia e gerencia a recursão de inserção."""
    # Chama o método privado e atualiza o root da classe
     self.root = self._insert(self.root, key, data)

   def search_item(self, key):
     """Método público que inicia a busca."""
    # Chama o método privado
     return self._search(self.root, key)

   def delete_item(self, key):
     """Método público que inicia e gerencia a remoção."""
    # Chama o método privado e atualiza o root da classe
     self.root = self._delete(self.root, key)
    
   def recommend_item(self, key, limit=5):
      """Método público para recomendação."""
      # Chama o método recommend
      return self.recommend(key, limit)

    # --- MÉTODOS AUXILIARES O(1) ---

   def _get_height(self, node):
        if not node:
            return 0
        return node.height

   def _get_balance(self, node):    
        if not node:
           return 0
        return self._get_height(node.left) - self._get_height(node.right)

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

    # --- OPERAÇÕES PRINCIPAIS RECURSIVAS O(log n) ---

   def _insert(self, root, key, data):
        
        if not root:
            return Node(key, data)

        if key < root.key:
            root.left = self._insert(root.left, key, data)
        elif key > root.key:
            root.right = self._insert(root.right, key, data)
        else:
            return root

        root.height = 1 + max(self._get_height(root.left), self._get_height(root.right))
        balance = self._get_balance(root)

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
    
        self.comparison_count += 1
        if not root or root.key == key:
            return root
        if key < root.key:
            return self._search(root.left, key)
        else:
            return self._search(root.right, key)

   def _get_min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

   def _delete(self, root, key):
        if not root:
            return root

        if key < root.key:
            root.left = self._delete(root.left, key)
        elif key > root.key:
            root.right = self._delete(root.right, key)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            
            temp = self._get_min_value_node(root.right)
            
            root.key = temp.key
            root.data = temp.data
            
            root.right = self._delete(root.right, temp.key)

        if root is None:
            return root

        root.height = 1 + max(self._get_height(root.left), self._get_height(root.right))
        balance = self._get_balance(root)

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

   def print_hierarchy(self, root, level=0):
        if root:
            self.print_hierarchy(root.right, level + 1)
            print("    " * level + f"-> [{root.key}] {root.data} (H: {root.height}, FB: {self._get_balance(root)})")
            self.print_hierarchy(root.left, level + 1) 

   def _get_inorder_successor(self, node):

        if node is None:
            return None
        
        current = node.right
        while current and current.left:
            current = current.left
        return current

   def _get_inorder_predecessor(self, node):

        if node is None:
            return None

        current = node.left
        while current and current.right:
            current = current.right
        return current
    
   def recommend(self, key, limit=5):
   
      self.comparison_count = 0 

      target_node = self._search(self.root, key)
        
      if not target_node:
            print(f"Item com ID {key} não encontrado para recomendação.")
            return []

      recommendations_set = set()

      current_suc = target_node
      while len(recommendations_set) < limit:
        successor = self._get_inorder_successor(current_suc)

        if successor is None:
           break
         
        recommendations_set.add(successor.data) 
        current_suc = successor
   
      current_pred = target_node
      while len(recommendations_set) < limit:
         predecessor = self._get_inorder_predecessor(current_pred)

         if predecessor is None:
             break
         
         recommendations_set.add(predecessor.data)
         current_pred = predecessor
        
      return list(recommendations_set)