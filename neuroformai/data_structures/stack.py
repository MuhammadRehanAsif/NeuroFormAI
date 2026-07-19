class Stack:
    """
    Array-based stack implementation.
    Used for rep state machine (tracking exercise phases) and undo actions.
    """

    def __init__(self):
        self._data = []
        self._size = 0

    def push(self, item):
        """Push an item onto the top of the stack."""
        if self._size == len(self._data):
            self._data.append(item)
        else:
            self._data[self._size] = item
        self._size += 1

    def pop(self):
        """Remove and return the top item."""
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        self._size -= 1
        item = self._data[self._size]
        self._data[self._size] = None
        return item

    def peek(self):
        """Return the top item without removing it."""
        if self.is_empty():
            raise IndexError("Peek from empty stack")
        return self._data[self._size - 1]

    def is_empty(self):
        return self._size == 0

    def size(self):
        return self._size

    def clear(self):
        """Remove all items from the stack."""
        self._data = []
        self._size = 0

    def to_list(self):
        """Return all items from bottom to top."""
        return [self._data[i] for i in range(self._size)]

    def contains(self, item):
        """Check if an item exists in the stack."""
        for i in range(self._size):
            if self._data[i] == item:
                return True
        return False

    def __len__(self):
        return self._size

    def __repr__(self):
        return f"Stack({self.to_list()})"
