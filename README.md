# Runtime-Space-Complexity-in-Financial-Signal-Processing
Homework 2 for Real time Intelligence Systems

This project implements a high-performance market data processing pipeline in Python. It demonstrates the differences in algorithmic complexity between a Naive approach (O(N)) and an Optimized Windowed approach (O(1)). It also explores system-level optimizations like Generator Streaming to minimize memory footprint.

## File Structure
File Description:  

data_loader.py handles CSV parsing, Dataclass creation, and Generator streaming.  

models.py defines the immutable MarketDataPoint (frozen dataclass) and Strategy interface.  

strategies.py implements NaiveMovingAverageStrategy and WindowedMovingAverageStrategy.profiler.py and measures Runtime and Peak Memory using timeit and memory_profiler.  

reporting.py generates plots (matplotlib) and the markdown complexity report.  

main.py runs ingestion, strategies, and profiling.  

tests/Unit tests validating strategy correctness and performance constraints.  


## Setup & Usage
Prerequisites:
Ensure have Python 3.10+ installed. 
1. Install the required dependencies: Bashpip install matplotlib memory_profiler numpy
2. Downloaded data from "sudalairajkumar/cryptocurrencypricehistory" Kaggle "coin_Bitcoin.csv" and in this project refered as "market_data.csv"
3. Run the Main Pipeline (python main.py)
Output: Generates complexity_report.md, runtime_plot.png, and memory_plot.png.
4. Run Unit Tests (python -m unittest discover tests)
