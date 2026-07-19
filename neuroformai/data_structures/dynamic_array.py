import ctypes


class DynamicArray:
    """
    Resizable array implementation.
    Used for storing MediaPipe landmark coordinates per frame (33 landmarks x 3 values)
    and collecting rep angle data during a session for analysis.

    Doubles capacity when full, halves when quarter full (amortized O(1) append).
    """

    def __init__(self, initial_capacity=16):
        if initial_capacity <= 0:
            raise ValueError("Initial capacity must be positive")
        self._size = 0
        self._capacity = initial_capacity
        self._data = self._make_array(initial_capacity)

    def _make_array(self, capacity):
        """Create a new raw array of the given capacity using ctypes."""
        return (capacity * ctypes.py_object)()

    def _resize(self, new_capacity):
        """Resize the internal array to new_capacity."""
        new_array = self._make_array(new_capacity)
        for i in range(self._size):
            new_array[i] = self._data[i]
        self._data = new_array
        self._capacity = new_capacity

    def append(self, item):
        """Add an item to the end. O(1) amortized."""
        if self._size == self._capacity:
            self._resize(2 * self._capacity)
        self._data[self._size] = item
        self._size += 1

    def get(self, index):
        """Get item at index. O(1)."""
        if index < 0 or index >= self._size:
            raise IndexError(f"Index {index} out of range for array of size {self._size}")
        return self._data[index]

    def set(self, index, value):
        """Set item at index. O(1)."""
        if index < 0 or index >= self._size:
            raise IndexError(f"Index {index} out of range for array of size {self._size}")
        self._data[index] = value

    def remove(self, index):
        """Remove item at index and shift remaining elements. O(n)."""
        if index < 0 or index >= self._size:
            raise IndexError(f"Index {index} out of range for array of size {self._size}")
        item = self._data[index]
        for i in range(index, self._size - 1):
            self._data[i] = self._data[i + 1]
        self._size -= 1

        if self._size > 0 and self._size <= self._capacity // 4:
            self._resize(max(self._capacity // 2, 1))

        return item

    def insert(self, index, item):
        """Insert item at index and shift remaining elements. O(n)."""
        if index < 0 or index > self._size:
            raise IndexError(f"Index {index} out of range for array of size {self._size}")
        if self._size == self._capacity:
            self._resize(2 * self._capacity)
        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]
        self._data[index] = item
        self._size += 1

    def pop(self):
        """Remove and return the last item."""
        if self._size == 0:
            raise IndexError("Pop from empty array")
        self._size -= 1
        item = self._data[self._size]
        if self._size > 0 and self._size <= self._capacity // 4:
            self._resize(max(self._capacity // 2, 1))
        return item

    def clear(self):
        """Remove all items and reset capacity."""
        self._size = 0
        self._capacity = 16
        self._data = self._make_array(self._capacity)

    def size(self):
        return self._size

    def capacity(self):
        return self._capacity

    def is_empty(self):
        return self._size == 0

    def to_list(self):
        """Convert to a Python list."""
        return [self._data[i] for i in range(self._size)]

    def __len__(self):
        return self._size

    def __getitem__(self, index):
        return self.get(index)

    def __setitem__(self, index, value):
        self.set(index, value)

    def __repr__(self):
        return f"DynamicArray({self.to_list()})"
