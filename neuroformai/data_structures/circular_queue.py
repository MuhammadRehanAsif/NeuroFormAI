class CircularQueue:
    """
    Fixed-size circular queue for angle smoothing.
    Maintains a sliding window of recent angle readings and returns
    their average to reduce frame-to-frame noise from MediaPipe.
    """

    def __init__(self, capacity=7):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self._capacity = capacity
        self._data = [None] * capacity
        self._front = 0
        self._rear = -1
        self._size = 0

    def enqueue(self, value):
        """Add a value. If full, overwrites the oldest value (auto-dequeue)."""
        if self.is_full():
            self._front = (self._front + 1) % self._capacity
            self._size -= 1
        self._rear = (self._rear + 1) % self._capacity
        self._data[self._rear] = value
        self._size += 1

    def dequeue(self):
        """Remove and return the oldest value."""
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        value = self._data[self._front]
        self._data[self._front] = None
        self._front = (self._front + 1) % self._capacity
        self._size -= 1
        return value

    def peek(self):
        """Return the oldest value without removing it."""
        if self.is_empty():
            raise IndexError("Peek from empty queue")
        return self._data[self._front]

    def average(self):
        """Return the average of all values in the queue (smoothed angle)."""
        if self.is_empty():
            return 0.0
        total = 0.0
        idx = self._front
        for _ in range(self._size):
            total += self._data[idx]
            idx = (idx + 1) % self._capacity
        return total / self._size

    def is_full(self):
        return self._size == self._capacity

    def is_empty(self):
        return self._size == 0

    def size(self):
        return self._size

    def capacity(self):
        return self._capacity

    def clear(self):
        """Reset the queue to empty state."""
        self._data = [None] * self._capacity
        self._front = 0
        self._rear = -1
        self._size = 0

    def to_list(self):
        """Return all values in order (oldest to newest)."""
        result = []
        idx = self._front
        for _ in range(self._size):
            result.append(self._data[idx])
            idx = (idx + 1) % self._capacity
        return result

    def __len__(self):
        return self._size

    def __repr__(self):
        return f"CircularQueue({self.to_list()}, capacity={self._capacity})"
