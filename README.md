# AIZYClientPy - Algorithmic Trading Bot Framework

A flexible and extensible Python framework for creating and testing algorithmic trading bots. This framework provides the core infrastructure for developing, testing, and running trading strategies with real-time market data.

## Features

- Real-time market data processing via WebSocket connections
- Order management system with support for market and limit orders
- Candlestick data handling and analysis
- Trade position tracking and performance metrics
- Built-in testing engine for strategy validation
- Comprehensive logging system

## Project Structure

```
AIZYClientPy/
├── src/
│   ├── AizyBot.py         # Base trading bot implementation
│   ├── CandleData.py      # Candlestick data structure
│   ├── OrderManager.py    # Order management system
│   ├── TestEngine.py      # Testing framework
│   └── Trade.py           # Trade position tracking
```

## Components

### AizyBot

The base class for implementing trading bots. It provides:
- WebSocket connection management
- Order placement and management
- Trade tracking
- Logging functionality

To create a custom trading bot, inherit from `AizyBot` and implement the `bot_action` method:

```python
from aizypy import AizyBot
from aizypy import CandleData

class MyTradingBot(AizyBot):
    async def bot_action(self, candle_data: CandleData) -> None:
        # Implement your trading strategy here
        pass
```

### CandleData

Represents candlestick market data with properties:
- timestamp
- open, high, low, close prices
- volume

### OrderManager

Handles the lifecycle of trading orders:
- Order creation and validation
- Execution tracking
- Status management (CREATED, VALIDATED, ACTIVE, PENDING, CANCELLED, FAILED, CLOSED)

### Trade

Represents a trading position with:
- Entry and exit prices
- Position size and leverage
- Performance metrics (ROE, profit/loss)
- Take profit and stop loss levels

### TestEngine

Provides a simulation environment for testing trading strategies:
- Market data simulation
- Performance tracking
- Detailed trade analysis
- Summary statistics

## Usage Example

```python
from aizypy import AizyBot
from aizypy import CandleData
from aizypy import TestEngine

class SimpleMovingAverageBot(AizyBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prices = []
        
    async def bot_action(self, candle_data: CandleData) -> None:
        self.prices.append(candle_data.close)
        
        if len(self.prices) >= 20:
            sma = sum(self.prices[-20:]) / 20
            if candle_data.close > sma:
                await self.place_order("buy", 1.0, candle_data.close, "BTC/USD")
            elif candle_data.close < sma:
                await self.place_order("sell", 1.0, candle_data.close, "BTC/USD")

# Test the strategy
async def test_strategy():
    await TestEngine.test(SimpleMovingAverageBot, duration=120, interval=1)
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/AIZYClientPy.git
cd AIZYClientPy
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Testing

The framework includes a comprehensive testing engine. To test a trading strategy:

```python
from aizypy import TestEngine

# Run a 1-hour test with 1-minute intervals
await TestEngine.test(YourTradingBot, duration=60, interval=1)
```

The test engine will:
1. Simulate market data
2. Execute your strategy
3. Track all trades
4. Generate performance metrics
5. Provide detailed analysis

## Logging

The framework includes built-in logging functionality. Logs are written to the specified log file (default: `log.txt`):

```python
bot = YourTradingBot(log_file="custom_log.txt")
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
