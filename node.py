class Node:
    def __init__(self, key, data):
        self.key = int(key)
        self.data = dict(data)
        self.left = None
        self.right = None
        self.height = 1