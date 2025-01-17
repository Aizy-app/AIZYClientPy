"""
Simple Moving Average (SMA) Trading Bot Example

This bot implements a basic trading strategy based on the Simple Moving Average indicator:
- Buy when price crosses above SMA
- Sell when price crosses below SMA
"""

from aizypy import AizyBot
from aizypy import CandleData
from aizypy import TestEngine
from typing import List, Optional
import logging

class SimpleMovingAverageBot(AizyBot):
    def __init__(self, *args, **kwargs) -> None:
        """Initialize the SMA trading bot.
        
        Args:
            sma_period: Number of periods to use for SMA calculation
            *args: Additional positional arguments for AizyBot
            **kwargs: Additional keyword arguments for AizyBot
        """
        super().__init__(*args, **kwargs)
        self.sma_period: int = 20
        self.prices: List[float] = []
        self.last_position: Optional[str] = None
        self.logger.info(f"Initialized SMA bot with period {self.sma_period}")

    def calculate_sma(self) -> float:
        """Calculate the Simple Moving Average.
        
        Returns:
            The calculated SMA value
        """
        return sum(self.prices[-self.sma_period:]) / self.sma_period

    async def bot_action(self, candle_data: CandleData) -> None:
        """Process new candle data and execute trading strategy.
        
        Strategy:
        - Calculate SMA when enough price data is available
        - Buy when price crosses above SMA
        - Sell when price crosses below SMA
        - Avoid opening multiple positions in the same direction
        
        Args:
            candle_data: Latest market candle data
        """
        self.prices.append(candle_data.close)
        
        # Wait until we have enough data to calculate SMA
        if len(self.prices) < self.sma_period:
            self.logger.info(f"Collecting initial data: {len(self.prices)}/{self.sma_period}")
            return

        sma = self.calculate_sma()
        current_price = candle_data.close
        
        self.logger.info(f"Current Price: {current_price:.2f}, SMA: {sma:.2f}")

        # Check for buy signal
        if current_price > sma and self.last_position != "long":
            self.logger.info("Buy signal: Price crossed above SMA")
            await self.place_order("buy", 1.0, current_price, "BTC/USD")
            self.last_position = "long"

        # Check for sell signal
        elif current_price < sma and self.last_position != "short":
            self.logger.info("Sell signal: Price crossed below SMA")
            await self.place_order("sell", 1.0, current_price, "BTC/USD")
            self.last_position = "short"

async def main() -> None:
    """Run the SMA bot with the test engine."""
    # Test parameters
    test_duration = 120  # 2 hours
    test_interval = 1    # 1 minute candles
    sma_period = 20     # 20-period SMA

    print(f"Starting SMA bot test (Duration: {test_duration} minutes, Interval: {test_interval} minute(s))")
    await TestEngine.test(
        lambda *args, **kwargs: SimpleMovingAverageBot(sma_period, *args, **kwargs),
        duration=test_duration,
        interval=test_interval
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 