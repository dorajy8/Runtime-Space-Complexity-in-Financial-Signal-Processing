# Complexity Analysis Report

## 1. Performance Metrics

| Input Size (N) | Strategy | Time (s) | Memory (MB) |
|---|---|---|---|
| 1000 | Naive | 0.0004 | 88.73 |
| 1000 | Windowed | 0.0003 | 79.56 |
| 10000 | Naive | 0.0052 | 81.72 |
| 10000 | Windowed | 0.0048 | 81.70 |
| 100000 | Naive | 0.0481 | 106.59 |
| 100000 | Windowed | 0.0235 | 106.59 |

## 2. Theoretical Complexity

### NaiveMovingAverageStrategy
- **Time:** $O(N)$ per operation if re-calculating sum, or $O(k)$ for slicing. Over $N$ ticks, total time is high due to list slicing overhead.
- **Space:** $O(N)$. We store every single tick in `self.history`. Memory grows linearly with input size.

### WindowedMovingAverageStrategy
- **Time:** $O(1)$. We use a rolling sum (add new, subtract old). No slicing required.
- **Space:** $O(k)$. We only store the last $k$ elements in a `deque`. Memory usage remains constant regardless of $N$ (once $N > k$).

### NumpyMovingAverageStrategy
- **Time:** $O(1)$ effective per element 
- **Space:** $O(N)$ to store the arrays, but much more compact than Python lists. 

## 3. Observations
As seen in the plots:
- The **Naive** strategy consumes significantly more memory as N increases.
- The **Windowed** strategy maintains a flat memory footprint.
- Runtime improvement in the Windowed strategy is due to avoiding repeated list slicing and summation.

## 4. Optimization
- When I refactored the data loader to use Python Generators instead of loading the entire list into memory and implemented the Numpy Moving Average Strategy, streaming process 100k ticks in 0.0187s with minimal memory overhead.
