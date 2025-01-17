# Trading Bot Examples

This directory contains example implementations of different trading strategies using the AIZYClientPy framework. Each example demonstrates different aspects of the framework and various trading approaches.

## Available Examples

### 1. Simple Moving Average Bot (`simple_moving_average_bot.py`)

A basic trend-following strategy that uses the Simple Moving Average (SMA) indicator:
- Calculates SMA over a specified period (default: 20 periods)
- Buys when price crosses above SMA (uptrend)
- Sells when price crosses below SMA (downtrend)
- Includes position tracking to avoid duplicate signals

Usage:
```bash
python examples/simple_moving_average_bot.py
```

### 2. RSI Bot (`rsi_bot.py`)

A mean reversion strategy using the Relative Strength Index (RSI) indicator:
- Calculates RSI over a specified period (default: 14 periods)
- Buys when RSI drops below oversold level (default: 30)
- Sells when RSI rises above overbought level (default: 70)
- Includes proper handling of edge cases in RSI calculation

Usage:
```bash
python examples/rsi_bot.py
```

### 3. Grid Trading Bot (`grid_trading_bot.py`)

A grid trading strategy that profits from price oscillations:
- Creates a grid of buy and sell orders at regular price intervals
- Automatically places new orders when existing ones are filled
- Manages multiple orders simultaneously
- Demonstrates limit order handling

Usage:
```bash
python examples/grid_trading_bot.py
```

## Running the Examples

Each example can be run independently and includes:
- Configurable parameters for the strategy
- Built-in test execution using the TestEngine
- Detailed logging of trading decisions
- Performance metrics output

To run any example:
1. Make sure you have installed all requirements
2. Navigate to the project root directory
3. Run the desired example using Python

Example:
```bash
# From the project root directory
python examples/simple_moving_average_bot.py
```

## Customizing the Examples

Each bot can be customized by modifying its parameters:

### Simple Moving Average Bot
- `sma_period`: Number of periods for SMA calculation
- `test_duration`: Duration of the test in minutes
- `test_interval`: Interval between candles in minutes

### RSI Bot
- `rsi_period`: Number of periods for RSI calculation
- `oversold_level`: RSI level for buy signals
- `overbought_level`: RSI level for sell signals
- `test_duration`: Duration of the test in minutes
- `test_interval`: Interval between candles in minutes

### Grid Trading Bot
- `grid_size`: Number of grid levels above and below the initial price
- `grid_spacing`: Price difference between grid levels
- `position_size`: Size of each order
- `test_duration`: Duration of the test in minutes
- `test_interval`: Interval between candles in minutes

## Creating Your Own Bot

To create your own trading bot:

1. Create a new Python file in the examples directory
2. Inherit from the `AizyBot` class
3. Implement the `bot_action` method with your strategy
4. Add any necessary helper methods and state management
5. Use the TestEngine to validate your strategy

Example template:
```python
from aizypy import AizyBot
from aizypy import CandleData
from aizypy import TestEngine

class MyCustomBot(AizyBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize your strategy parameters here
        
    async def bot_action(self, candle_data: CandleData) -> None:
        # Implement your trading logic here
        pass

async def main():
    await TestEngine.test(MyCustomBot, duration=120, interval=1)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 