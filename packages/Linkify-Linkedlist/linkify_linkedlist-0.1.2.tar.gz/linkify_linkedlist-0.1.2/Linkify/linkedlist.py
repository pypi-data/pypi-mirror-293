class Node:
    def __init__(self, value=None):
        self.value = value
        self.next = None
class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, value):
        new_node = Node(value)
        if not self.head:
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node

    def display(self):
        elements = []
        current = self.head
        while current:
            elements.append(str(current.value))
            current = current.next
        return ' -> '.join(elements) if elements else 'Empty List'

    @staticmethod
    def from_array(array):
        linked_list = LinkedList()
        for item in array:
            linked_list.append(item)
        return linked_list
