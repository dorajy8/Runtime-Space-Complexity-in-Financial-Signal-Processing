from collections import deque
from models import Strategy, MarketDataPoint

class NaiveMovingAverageStrategy(Strategy):
    """
    Time Complexity: O(N) per tick (summing the whole history)
    Space Complexity: O(N) (storing full history)
    """
    def __init__(self, window_size: int):
        self.window_size = window_size
        self.history = []  # Stores every price ever seen

    def generate_signals(self, tick: MarketDataPoint) -> list:
        self.history.append(tick.price)
        
        # If we don't have enough data for a window, do nothing
        if len(self.history) < self.window_size:
            return []
        recent_prices = self.history[-self.window_size:]
        avg_price = sum(recent_prices) / self.window_size

        if tick.price > avg_price:
            return ["BUY"]
        elif tick.price < avg_price:
            return ["SELL"]
        return []
    

class WindowedMovingAverageStrategy(Strategy):
    """
    Time Complexity: O(1) per tick (math operations are constant time)
    Space Complexity: O(K) where K is window size (only store the window)
    """
    def __init__(self, window_size: int):
        self.window_size = window_size
        self.window = deque(maxlen=window_size) 
        self.current_sum = 0.0

    def generate_signals(self, tick: MarketDataPoint) -> list:
        if len(self.window) == self.window_size:
            removed_price = self.window[0] # The left-most (oldest) item
            self.current_sum -= removed_price

        self.window.append(tick.price)
        self.current_sum += tick.price
        
        if len(self.window) < self.window_size:
            return []

        avg_price = self.current_sum / self.window_size
        
        if tick.price > avg_price:
            return ["BUY"]
        elif tick.price < avg_price:
            return ["SELL"]
        return []
    
import numpy as np # Make sure to pip install numpy
from models import Strategy, MarketDataPoint

class NumpyMovingAverageStrategy(Strategy):
    """
    Optimization: Vectorized Operations.
    Instead of processing tick-by-tick (streaming), we process a bulk array.
    
    Time Complexity: O(1) effective per element due to C-level optimizations in Numpy.
    Space Complexity: O(N) to store the arrays, but much more compact than Python lists.
    """
    def __init__(self, window_size: int):
        self.window_size = window_size
        self.prices = [] 

    def generate_signals(self, tick: MarketDataPoint) -> list:
        # load the whole CSV into a numpy array 
        self.prices.append(tick.price)
        
        if len(self.prices) < self.window_size:
            return []
            
        # CONVERT TO NUMPY (Expensive if done every tick, efficient if done once at end)
        price_array = np.array(self.prices[-self.window_size:])
        
        # Numpy mean is highly optimized
        avg_price = np.mean(price_array)
        
        if tick.price > avg_price:
            return ["BUY"]
        elif tick.price < avg_price:
            return ["SELL"]
        return []

# Optimization Memory
from functools import lru_cache
class MemoizedStrategy(Strategy):
    """
    Demonstrates lru_cache. 
    Useful when heavy calculation logic that repeated for specific price levels.
    """
    def generate_signals(self, tick: MarketDataPoint) -> list:
        return self._heavy_calculation(tick.price)

    @lru_cache(maxsize=128)
    def _heavy_calculation(self, price: float) -> list:
        # Pretend this is a very expensive math operation
        # If we see the same price twice, the result is returned instantly from cache.
        if price % 2 == 0:
            return ["BUY"]
        return []   