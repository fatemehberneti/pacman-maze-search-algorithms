class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
        self._size = 0

    def is_empty(self):
        return self.front is None

    def __bool__(self):
        return not self.is_empty()

    def __len__(self):
        return self._size

    def enqueue(self, data):
        new_node = Node(data)
        if self.is_empty():
            self.front = new_node
            self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            return None
        deleted = self.front.data
        if self.front == self.rear:
            self.front = None
            self.rear = None
        else:
            self.front = self.front.next
        self._size -= 1
        return deleted

    def show(self):
        tmp = self.front
        while tmp is not None:
            print(tmp.data, end="->")
            tmp = tmp.next