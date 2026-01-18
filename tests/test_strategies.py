import unittest
from datetime import datetime
from strategies import NaiveMovingAverageStrategy, WindowedMovingAverageStrategy
from models import MarketDataPoint

class TestStrategies(unittest.TestCase):
    
    def setUp(self):
        self.ticks = [
            MarketDataPoint(datetime.now(), "TEST", float(p)) 
            for p in [10, 20, 30, 40, 50]
        ]
        self.window_size = 3

    def test_naive_strategy_correctness(self):
        strategy = NaiveMovingAverageStrategy(self.window_size)
        
        # Tick 1 (Price 10): Not enough data -> []
        self.assertEqual(strategy.generate_signals(self.ticks[0]), [])
        
        # Tick 2 (Price 20): Not enough data -> []
        self.assertEqual(strategy.generate_signals(self.ticks[1]), [])
        
        # Tick 3 (Price 30): History [10, 20, 30]. Avg = 20. 
        # Price 30 > Avg 20 -> BUY
        self.assertEqual(strategy.generate_signals(self.ticks[2]), ["BUY"])
        
        # Tick 4 (Price 40): History [..., 20, 30, 40]. Avg = 30.
        # Price 40 > Avg 30 -> BUY
        self.assertEqual(strategy.generate_signals(self.ticks[3]), ["BUY"])

    def test_windowed_strategy_correctness(self):
        strategy = WindowedMovingAverageStrategy(self.window_size)
        
        self.assertEqual(strategy.generate_signals(self.ticks[0]), [])
        self.assertEqual(strategy.generate_signals(self.ticks[1]), [])
        # Window [10, 20, 30]. Avg 20. Price 30 -> BUY
        self.assertEqual(strategy.generate_signals(self.ticks[2]), ["BUY"])
        
        # Window [20, 30, 40]. Avg 30. Price 40 -> BUY
        self.assertEqual(strategy.generate_signals(self.ticks[3]), ["BUY"])

    def test_sell_signal(self):

        strategy = WindowedMovingAverageStrategy(3)
        # Prices: 100, 100, 100 (Avg 100) -> 50 (Avg 83.3) -> SELL
        
        ticks = [MarketDataPoint(datetime.now(), "T", p) for p in [100, 100, 100, 50]]
        
        for t in ticks[:3]:
            strategy.generate_signals(t)
            
        # Feed 4th (Price 50)
        # Window before 4th: [100, 100, 100]. Sum 300.
        # Update: remove 100, add 50. New Sum 250. Avg = 83.33.
        # Price 50 < Avg 83.33 -> SELL
        signal = strategy.generate_signals(ticks[3])
        self.assertEqual(signal, ["SELL"])

    def test_performance_constraints(self):
        """
        Rough validation that Windowed strategy is fast.
        The prompt asks to 'confirm optimized strategy runs under 1 second'.
        """
        import time
        strategy = WindowedMovingAverageStrategy(50)
        # Generate 100,000 dummy ticks
        large_data = [MarketDataPoint(datetime.now(), "T", 1.0) for _ in range(100_000)]
        
        start = time.time()
        for tick in large_data:
            strategy.generate_signals(tick)
        duration = time.time() - start
        
        print(f"\nPerformance Test: Processed 100k ticks in {duration:.4f}s")
        self.assertLess(duration, 1.0, "Windowed strategy is too slow!")

if __name__ == '__main__':
    unittest.main()