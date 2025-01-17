# AIZYClientPy

A Python framework for creating and testing trading bots on the Aizy platform.

## Features

- Real-time market data processing via WebSocket
- Order management system with market and limit orders
- Candlestick data handling and analysis
- Trade position tracking and performance metrics
- Built-in testing engine for strategy validation
- Comprehensive logging system

## Installation

```bash
pip install aizypy
```

## Quick Start

```python
from aizypy import AizyBot, CandleData, TestEngine

class MyTradingBot(AizyBot):
    async def bot_action(self, candle: CandleData) -> None:
        # Implement your trading strategy here
        if your_condition:
            await self.place_order("buy", 1.0, candle.close, "BTC/USD")

# Test your bot
await TestEngine.test(MyTradingBot, duration=120, interval=1)
```

## Documentation

Full documentation is available at [ReadTheDocs](https://aizyclientpy.readthedocs.io/en/latest/usage.html)

## Example Strategies

The package includes several example strategies:

1. Simple Moving Average Bot
2. RSI (Relative Strength Index) Bot
3. Grid Trading Bot

## Support

For support:
- Visit [aizy.dev](https://aizy.pages.dev/)
- Open an issue on [GitHub](https://github.com/Aizy-app/AIZYClientPy/issues)

## License

This project is licensed under the MIT License. 