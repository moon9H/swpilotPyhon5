# 과정 4 - (문제8) "식물의 계보를 추적하자"

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

# [보너스 과제] - 전체 내용 BinarySearchTree 라는 이름의 클래스로 구성
class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        new_node = Node(value)
        if self.root is None:
            self.root = new_node
            return

        current = self.root
        while True:
            if value < current.value:
                if current.left is None:
                    current.left = new_node
                    return
                current = current.left
            else:
                if current.right is None:
                    current.right = new_node
                    return
                current = current.right

    def find(self, value):
        current = self.root
        while current is not None:
            if value == current.value:
                return True
            elif value < current.value:
                current = current.left
            else:
                current = current.right
        return False

    def delete(self, value):
        self.root = self._delete_node(self.root, value)

    def _delete_node(self, node, value):
        if node is None:
            return node

        if value < node.value:
            node.left = self._delete_node(node.left, value)
        elif value > node.value:
            node.right = self._delete_node(node.right, value)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # 양쪽 자식이 있는 경우
            temp = self._min_value_node(node.right)
            node.value = temp.value
            node.right = self._delete_node(node.right, temp.value)

        return node

    def _min_value_node(self, node):
        while node.left is not None:
            node = node.left
        return node

    def inorder(self):
        result = []
        self._inorder_traversal(self.root, result)
        return result

    def _inorder_traversal(self, node, result):
        if node:
            self._inorder_traversal(node.left, result)
            result.append(node.value)
            self._inorder_traversal(node.right, result)

# 사용 예시
if __name__ == '__main__':
    tree = BinarySearchTree()
    values = [50, 30, 70, 20, 40, 60, 80]

    for v in values:
        tree.insert(v)

    print('Inorder 순회:', tree.inorder())  # [20, 30, 40, 50, 60, 70, 80]

    print('Find 60:', tree.find(60))        # True
    print('Find 100:', tree.find(100))      # False

    tree.delete(70)
    print('70 삭제 후:', tree.inorder())    # [20, 30, 40, 50, 60, 80]