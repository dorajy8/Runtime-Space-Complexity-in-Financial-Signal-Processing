import matplotlib.pyplot as plt
import os

def generate_plots(stats: dict):
    """
    Generates and saves plots for Runtime and Memory usage.
    """
    # Prepare data for plotting
    n_values = stats['NaiveMovingAverageStrategy']['n']
    
    # --- Plot 1: Execution Time ---
    plt.figure(figsize=(10, 6))
    
    naive_times = stats['NaiveMovingAverageStrategy']['time']
    windowed_times = stats['WindowedMovingAverageStrategy']['time']
    
    plt.plot(n_values, naive_times, marker='o', label='Naive (Full History)')
    plt.plot(n_values, windowed_times, marker='o', label='Windowed (Deque)')
    
    plt.title('Execution Time vs Input Size')
    plt.xlabel('Number of Ticks (N)')
    plt.ylabel('Time (seconds)')
    plt.legend()
    plt.grid(True)
    plt.savefig('runtime_plot.png')
    plt.close()

    plt.figure(figsize=(10, 6))
    
    naive_mem = stats['NaiveMovingAverageStrategy']['mem']
    windowed_mem = stats['WindowedMovingAverageStrategy']['mem']
    
    plt.plot(n_values, naive_mem, marker='o', label='Naive (Full History)')
    plt.plot(n_values, windowed_mem, marker='o', label='Windowed (Deque)')
    
    plt.title('Peak Memory Usage vs Input Size')
    plt.xlabel('Number of Ticks (N)')
    plt.ylabel('Memory (MB)')
    plt.legend()
    plt.grid(True)
    plt.savefig('memory_plot.png')
    plt.close()

def create_markdown_report(stats: dict):
    """
    Generates the complexity_report.md file with tables and analysis.
    """
    filename = "complexity_report.md"
    
    with open(filename, 'w') as f:
        f.write("# Complexity Analysis Report\n\n")
        
        # 1. Performance Table
        f.write("## 1. Performance Metrics\n\n")
        f.write("| Input Size (N) | Strategy | Time (s) | Memory (MB) |\n")
        f.write("|---|---|---|---|\n")
        
        n_values = stats['NaiveMovingAverageStrategy']['n']
        for i, n in enumerate(n_values):
            # Naive Row
            n_time = stats['NaiveMovingAverageStrategy']['time'][i]
            n_mem = stats['NaiveMovingAverageStrategy']['mem'][i]
            f.write(f"| {n} | Naive | {n_time:.4f} | {n_mem:.2f} |\n")
            
            # Windowed Row
            w_time = stats['WindowedMovingAverageStrategy']['time'][i]
            w_mem = stats['WindowedMovingAverageStrategy']['mem'][i]
            f.write(f"| {n} | Windowed | {w_time:.4f} | {w_mem:.2f} |\n")
            
        f.write("\n## 2. Theoretical Complexity\n\n")
        f.write("### NaiveMovingAverageStrategy\n")
        f.write("- **Time:** $O(N)$ per operation if re-calculating sum, or $O(k)$ for slicing. Over $N$ ticks, total time is high due to list slicing overhead.\n")
        f.write("- **Space:** $O(N)$. We store every single tick in `self.history`. Memory grows linearly with input size.\n\n")
        
        f.write("### WindowedMovingAverageStrategy\n")
        f.write("- **Time:** $O(1)$. We use a rolling sum (add new, subtract old). No slicing required.\n")
        f.write("- **Space:** $O(k)$. We only store the last $k$ elements in a `deque`. Memory usage remains constant regardless of $N$ (once $N > k$).\n\n")
        
        # 3. Observations
        f.write("## 3. Observations\n")
        f.write("As seen in the plots:\n")
        f.write("- The **Naive** strategy consumes significantly more memory as N increases.\n")
        f.write("- The **Windowed** strategy maintains a flat memory footprint.\n")
        f.write("- Runtime improvement in the Windowed strategy is due to avoiding repeated list slicing and summation.\n")

    print(f"Report generated: {filename}")