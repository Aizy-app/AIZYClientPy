import asyncio
from src.AizyBot import AizyBot
from src.CandleData import CandleData

class ExampleTradingBot(AizyBot):
    def __init__(self, log_file: str = "example_log.log", uri: str = "ws://localhost:8080"):
        super().__init__(log_file, uri)

    async def bot_action(self, candle_data: CandleData):
        """A simple trading strategy based on candle data."""
        # Example strategy: If the closing price is higher than the opening price, go long; otherwise, go short.
        if candle_data.close > candle_data.open:
            await self.place_market_order("long", "1", "10", "BTC/USDT")
            self.logger.info("Placed a long order based on candle data.")
        else:
            await self.place_market_order("short", "1", "10", "BTC/USDT")
            self.logger.info("Placed a short order based on candle data.")

# Usage example (for testing locally)
async def main():
    bot = ExampleTradingBot()
    await bot.bot_setup("MockExchange", "MockStream")
    await bot.start()

    # Simulate receiving candle data and performing a trading action
    candle_data = CandleData(timestamp="2024-10-23T12:00:00Z", open=100, high=105, low=99, close=104, volume=1000)
    await bot.bot_action(candle_data)

    # List active trades
    active_trades = bot.list_active_trades()
    print("Active Trades:", active_trades)

# Run the example
if __name__ == "__main__":
    asyncio.run(main())
