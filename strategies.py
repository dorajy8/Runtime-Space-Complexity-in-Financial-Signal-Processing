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