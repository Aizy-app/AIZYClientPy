"""
RSI (Relative Strength Index) Trading Bot Example

This bot implements a trading strategy based on the RSI indicator:
- Buy when RSI is below oversold level (indicating potential reversal up)
- Sell when RSI is above overbought level (indicating potential reversal down)
"""

from aizypy import AizyBot
from aizypy import CandleData
from aizypy import TestEngine
from typing import List, Optional
import logging

class RSIBot(AizyBot):
    def __init__(self, 
                 rsi_period: int = 14,
                 oversold_level: float = 30.0,
                 overbought_level: float = 70.0,
                 *args, **kwargs) -> None:
        """Initialize the RSI trading bot.
        
        Args:
            rsi_period: Number of periods for RSI calculation
            oversold_level: RSI level below which to consider buying
            overbought_level: RSI level above which to consider selling
            *args: Additional positional arguments for AizyBot
            **kwargs: Additional keyword arguments for AizyBot
        """
        super().__init__(*args, **kwargs)
        self.rsi_period: int = rsi_period
        self.oversold_level: float = oversold_level
        self.overbought_level: float = overbought_level
        self.prices: List[float] = []
        self.gains: List[float] = []
        self.losses: List[float] = []
        self.last_position: Optional[str] = None
        self.logger.info(
            f"Initialized RSI bot (Period: {rsi_period}, "
            f"Oversold: {oversold_level}, Overbought: {overbought_level})"
        )

    def calculate_rsi(self) -> float:
        """Calculate the Relative Strength Index.
        
        Returns:
            The calculated RSI value
        """
        if len(self.prices) < 2:
            return 50.0  # Default to neutral when insufficient data
            
        # Calculate price changes
        changes = [self.prices[i] - self.prices[i-1] 
                  for i in range(1, len(self.prices))]
        
        # Separate gains and losses
        gains = [change if change > 0 else 0.0 for change in changes]
        losses = [-change if change < 0 else 0.0 for change in changes]
        
        # Calculate average gain and loss
        avg_gain = sum(gains[-self.rsi_period:]) / self.rsi_period
        avg_loss = sum(losses[-self.rsi_period:]) / self.rsi_period
        
        if avg_loss == 0:
            return 100.0
            
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi

    async def bot_action(self, candle_data: CandleData) -> None:
        """Process new candle data and execute trading strategy.
        
        Strategy:
        - Calculate RSI when enough price data is available
        - Buy when RSI drops below oversold level
        - Sell when RSI rises above overbought level
        - Avoid opening multiple positions in the same direction
        
        Args:
            candle_data: Latest market candle data
        """
        self.prices.append(candle_data.close)
        
        # Wait until we have enough data to calculate RSI
        if len(self.prices) < self.rsi_period + 1:
            self.logger.info(f"Collecting initial data: {len(self.prices)}/{self.rsi_period + 1}")
            return

        rsi = self.calculate_rsi()
        current_price = candle_data.close
        
        self.logger.info(f"Current Price: {current_price:.2f}, RSI: {rsi:.2f}")

        # Check for buy signal (oversold condition)
        if rsi < self.oversold_level and self.last_position != "long":
            self.logger.info(f"Buy signal: RSI ({rsi:.2f}) below oversold level ({self.oversold_level})")
            await self.place_order("buy", 1.0, current_price, "BTC/USD")
            self.last_position = "long"

        # Check for sell signal (overbought condition)
        elif rsi > self.overbought_level and self.last_position != "short":
            self.logger.info(f"Sell signal: RSI ({rsi:.2f}) above overbought level ({self.overbought_level})")
            await self.place_order("sell", 1.0, current_price, "BTC/USD")
            self.last_position = "short"

async def main() -> None:
    """Run the RSI bot with the test engine."""
    # Test parameters
    test_duration = 240  # 4 hours
    test_interval = 1    # 1 minute candles
    rsi_period = 14     # 14-period RSI
    oversold = 30.0     # Oversold level
    overbought = 70.0   # Overbought level

    print(f"Starting RSI bot test (Duration: {test_duration} minutes, Interval: {test_interval} minute(s))")
    await TestEngine.test(
        lambda *args, **kwargs: RSIBot(rsi_period, oversold, overbought, *args, **kwargs),
        duration=test_duration,
        interval=test_interval
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 