def merge_sort(array, key=None, reverse=False):
    """
    Stable merge sort implementation. O(n log n) time, O(n) space.
    Used for sorting workout session history by date (stability matters
    when secondary ordering should be preserved).

    Args:
        array: List of items to sort.
        key: Optional function to extract comparison value from each item.
        reverse: If True, sort in descending order.

    Returns:
        A new sorted list (does not modify the original).
    """
    if key is None:
        key = lambda x: x

    arr = list(array)

    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key=key, reverse=reverse)
    right = merge_sort(arr[mid:], key=key, reverse=reverse)

    return _merge(left, right, key, reverse)


def _merge(left, right, key, reverse):
    """Merge two sorted lists into one sorted list."""
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        left_val = key(left[i])
        right_val = key(right[j])

        if reverse:
            should_take_left = left_val >= right_val
        else:
            should_take_left = left_val <= right_val

        if should_take_left:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    while i < len(left):
        result.append(left[i])
        i += 1

    while j < len(right):
        result.append(right[j])
        j += 1

    return result


def quick_sort(array, key=None, reverse=False):
    """
    Quick sort implementation using Lomuto partition scheme. O(n log n) average.
    Used for sorting leaderboard data by score/reps where stability isn't needed
    and average-case performance matters.

    Args:
        array: List of items to sort.
        key: Optional function to extract comparison value from each item.
        reverse: If True, sort in descending order.

    Returns:
        A new sorted list (does not modify the original).
    """
    if key is None:
        key = lambda x: x

    arr = list(array)
    _quick_sort_recursive(arr, 0, len(arr) - 1, key, reverse)
    return arr


def _quick_sort_recursive(arr, low, high, key, reverse):
    """Recursive quick sort with median-of-three pivot selection."""
    if low < high:
        pivot_index = _partition(arr, low, high, key, reverse)
        _quick_sort_recursive(arr, low, pivot_index - 1, key, reverse)
        _quick_sort_recursive(arr, pivot_index + 1, high, key, reverse)


def _median_of_three(arr, low, high, key):
    """Select median of first, middle, and last elements as pivot."""
    mid = (low + high) // 2
    a, b, c = key(arr[low]), key(arr[mid]), key(arr[high])

    if a <= b <= c or c <= b <= a:
        return mid
    elif b <= a <= c or c <= a <= b:
        return low
    else:
        return high


def _partition(arr, low, high, key, reverse):
    """Lomuto partition with median-of-three pivot."""
    pivot_index = _median_of_three(arr, low, high, key)
    arr[pivot_index], arr[high] = arr[high], arr[pivot_index]

    pivot_val = key(arr[high])
    i = low - 1

    for j in range(low, high):
        current_val = key(arr[j])
        if reverse:
            should_swap = current_val >= pivot_val
        else:
            should_swap = current_val <= pivot_val

        if should_swap:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
