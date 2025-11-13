from node import Node

class AVLTree:

    def __init__(self):
       
        self.root = None
        self.comparison_count = 0 

    def _get_height(self, node):

        if not node:
            return 0
        return node.height

    def _get_balance(self, node):    
        if not node:
         return 0
        return self._get_height(node.left) - self._get_height(node.right)


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

    def insert(self, root, key, data):
    
        if not root:
            return Node(key, data)

        if key < root.key:
            root.left = self.insert(root.left, key, data)
        elif key > root.key:
            root.right = self.insert(root.right, key, data)
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

    def search(self, root, key):
    
        self.comparison_count += 1
        if not root or root.key == key:
            return root
        if key < root.key:
            return self.search(root.left, key)
        else:
            return self.search(root.right, key)

    def _get_min_value_node(self, node):

        current = node
        while current.left is not None:
            current = current.left
        return current

    def delete(self, root, key):

        if not root:
            return root

        if key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
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
            
            root.right = self.delete(root.right, temp.key)

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

def insert_item(self, key, data):
    self.root = self.insert(self.root, key, data)

def search_item(self, key):
    return self.search(self.root, key)