import data_loader
import profiler
import reporting
import strategies
import time

def main():
    try:
        data = data_loader.load_market_data('market_data.csv')
        print(f"Successfully loaded {len(data)} rows.")
    except FileNotFoundError:
        print("market_data.csv not found. Skipping CSV load test.")

    stats = profiler.profile_strategies()
    
    reporting.generate_plots(stats)
    reporting.create_markdown_report(stats)

    print("\n--- Optimization Implemented")
    # This loop runs without ever storing the full file in RAM
    strategy = strategies.WindowedMovingAverageStrategy(window_size=50)
    
    # Notice we use 'stream_market_data' here
    data_stream = data_loader.stream_market_data('market_data.csv')
    
    start_t = time.time()
    for tick in data_stream:
        strategy.generate_signals(tick)
    print(f"Streamed processing finished in {time.time() - start_t:.4f}s")

if __name__ == "__main__":
    main()