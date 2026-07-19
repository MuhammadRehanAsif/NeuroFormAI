class Node:
    """A single node in the doubly linked list."""

    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

    def __repr__(self):
        return f"Node({self.data})"


class DoublyLinkedList:
    """
    Doubly linked list implementation.
    Used for workout session history navigation (prev/next)
    and exercise playlist (insert/remove at any position).
    """

    def __init__(self):
        self._head = None
        self._tail = None
        self._current = None
        self._size = 0

    def append(self, data):
        """Add a node at the end of the list."""
        new_node = Node(data)
        if self._head is None:
            self._head = new_node
            self._tail = new_node
            self._current = new_node
        else:
            new_node.prev = self._tail
            self._tail.next = new_node
            self._tail = new_node
        self._size += 1
        return new_node

    def prepend(self, data):
        """Add a node at the beginning of the list."""
        new_node = Node(data)
        if self._head is None:
            self._head = new_node
            self._tail = new_node
            self._current = new_node
        else:
            new_node.next = self._head
            self._head.prev = new_node
            self._head = new_node
        self._size += 1
        return new_node

    def insert_at(self, index, data):
        """Insert a node at a specific index (0-based)."""
        if index < 0 or index > self._size:
            raise IndexError(f"Index {index} out of range for list of size {self._size}")
        if index == 0:
            return self.prepend(data)
        if index == self._size:
            return self.append(data)

        current = self._head
        for _ in range(index):
            current = current.next

        new_node = Node(data)
        new_node.prev = current.prev
        new_node.next = current
        current.prev.next = new_node
        current.prev = new_node
        self._size += 1
        return new_node

    def remove_at(self, index):
        """Remove and return the data at a specific index."""
        if index < 0 or index >= self._size:
            raise IndexError(f"Index {index} out of range for list of size {self._size}")

        if self._size == 1:
            data = self._head.data
            self._head = None
            self._tail = None
            self._current = None
            self._size = 0
            return data

        if index == 0:
            data = self._head.data
            self._head = self._head.next
            self._head.prev = None
            if self._current and self._current.prev is None and self._current.next is None:
                self._current = self._head
        elif index == self._size - 1:
            data = self._tail.data
            self._tail = self._tail.prev
            self._tail.next = None
        else:
            current = self._head
            for _ in range(index):
                current = current.next
            data = current.data
            current.prev.next = current.next
            current.next.prev = current.prev
            if self._current == current:
                self._current = current.next

        self._size -= 1
        return data

    def get(self, index):
        """Get data at a specific index without removing it."""
        if index < 0 or index >= self._size:
            raise IndexError(f"Index {index} out of range for list of size {self._size}")
        current = self._head
        for _ in range(index):
            current = current.next
        return current.data

    def current(self):
        """Return the data at the current pointer position."""
        if self._current is None:
            return None
        return self._current.data

    def move_next(self):
        """Move the current pointer forward. Returns True if successful."""
        if self._current and self._current.next:
            self._current = self._current.next
            return True
        return False

    def move_prev(self):
        """Move the current pointer backward. Returns True if successful."""
        if self._current and self._current.prev:
            self._current = self._current.prev
            return True
        return False

    def move_to_head(self):
        """Reset current pointer to the head."""
        self._current = self._head

    def move_to_tail(self):
        """Move current pointer to the tail."""
        self._current = self._tail

    def current_index(self):
        """Return the index of the current pointer."""
        if self._current is None:
            return -1
        node = self._head
        idx = 0
        while node is not None:
            if node == self._current:
                return idx
            node = node.next
            idx += 1
        return -1

    def traverse_forward(self):
        """Yield all data from head to tail."""
        current = self._head
        while current is not None:
            yield current.data
            current = current.next

    def traverse_backward(self):
        """Yield all data from tail to head."""
        current = self._tail
        while current is not None:
            yield current.data
            current = current.prev

    def to_list(self):
        """Convert to a Python list (head to tail)."""
        return list(self.traverse_forward())

    def find(self, predicate):
        """Find first item matching a predicate function."""
        for data in self.traverse_forward():
            if predicate(data):
                return data
        return None

    def is_empty(self):
        return self._size == 0

    def length(self):
        return self._size

    def clear(self):
        """Remove all nodes."""
        self._head = None
        self._tail = None
        self._current = None
        self._size = 0

    def __len__(self):
        return self._size

    def __repr__(self):
        items = self.to_list()
        return f"DoublyLinkedList({items})"
