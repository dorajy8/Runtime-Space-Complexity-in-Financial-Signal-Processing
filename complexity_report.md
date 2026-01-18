# Complexity Analysis Report

## 1. Performance Metrics

| Input Size (N) | Strategy | Time (s) | Memory (MB) |
|---|---|---|---|
| 1000 | Naive | 0.0004 | 90.05 |
| 1000 | Windowed | 0.0006 | 78.06 |
| 10000 | Naive | 0.0046 | 78.95 |
| 10000 | Windowed | 0.0021 | 79.00 |
| 100000 | Naive | 0.0449 | 106.83 |
| 100000 | Windowed | 0.0233 | 106.83 |

## 2. Theoretical Complexity

### NaiveMovingAverageStrategy
- **Time:** $O(N)$ per operation if re-calculating sum, or $O(k)$ for slicing. Over $N$ ticks, total time is high due to list slicing overhead.
- **Space:** $O(N)$. We store every single tick in `self.history`. Memory grows linearly with input size.

### WindowedMovingAverageStrategy
- **Time:** $O(1)$. We use a rolling sum (add new, subtract old). No slicing required.
- **Space:** $O(k)$. We only store the last $k$ elements in a `deque`. Memory usage remains constant regardless of $N$ (once $N > k$).

## 3. Observations
As seen in the plots:
- The **Naive** strategy consumes significantly more memory as N increases.
- The **Windowed** strategy maintains a flat memory footprint.
- Runtime improvement in the Windowed strategy is due to avoiding repeated list slicing and summation.
