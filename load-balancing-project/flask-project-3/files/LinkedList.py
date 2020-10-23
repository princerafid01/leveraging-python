class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self,head = None  , tail = None , len = 0 ):
        self.head = head
        self.tail = tail
        self.len = len

    def insert(self , data):
        node = Node(data)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = self.tail.next
        self.len += 1

    def search(self ,data):
        hop = self.head
        while hop is not None:
            if hop.data == data:
                return True
            hop  = hop.next
        return False

    def __str__(self):
        vals= []
        node = self.head
        while node is not None:
            vals.append(node.data)
            node = node.next
        return f"[{', '.join(str(val) for val in vals)}]"
