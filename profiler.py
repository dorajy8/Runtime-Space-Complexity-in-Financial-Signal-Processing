import time
from memory_profiler import memory_usage
from strategies import NaiveMovingAverageStrategy, WindowedMovingAverageStrategy
from models import MarketDataPoint
from datetime import datetime

def generate_dummy_data(n):
    """Helper to generate N ticks for testing"""
    return [
        MarketDataPoint(datetime.now(), "AAPL", 100.0 + i) 
        for i in range(n)
    ]

def run_strategy(strategy, data):
    """Wrapper function to run the loop for profiling"""
    for tick in data:
        strategy.generate_signals(tick)

def profile_strategies():
    tick_counts = [1000, 10000, 100000] # As requested
    results = {}

    for n in tick_counts:
        print(f"--- Profiling N={n} ---")
        data = generate_dummy_data(n)
        
        for StratClass in [NaiveMovingAverageStrategy, WindowedMovingAverageStrategy]:
            name = StratClass.__name__
            
            start_time = time.time()
            strat = StratClass(window_size=50) # Window size of 50
            run_strategy(strat, data)
            end_time = time.time()
            total_time = end_time - start_time
    
            strat_mem = StratClass(window_size=50)
            mem_usage = memory_usage((run_strategy, (strat_mem, data)), max_usage=True)
            
            if name not in results: results[name] = {'time': [], 'mem': [], 'n': []}
            results[name]['time'].append(total_time)
            results[name]['mem'].append(mem_usage)
            results[name]['n'].append(n)
            
            print(f"{name}: Time={total_time:.4f}s, Peak Mem={mem_usage} MB")
            
    return results