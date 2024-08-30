import unittest
from Linkify import LinkedList

class TestLinkedList(unittest.TestCase):
    def test_from_array(self):
        arr = [1, 2, 3]
        linked_list = LinkedList.from_array(arr)
        self.assertEqual(linked_list.display(), arr)

    def test_append(self):
        linked_list = LinkedList()
        linked_list.append(1)
        linked_list.append(2)
        self.assertEqual(linked_list.display(), [1, 2])

if __name__ == '__main__':
    unittest.main()
