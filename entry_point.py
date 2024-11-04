import asyncio
from example_bot import ExampleTradingBot  # Ensure proper import
from src.CandleData import CandleData
async def main():
    bot = ExampleTradingBot()
    await bot.bot_setup("MockExchange", "MockStream")
    await bot.start()

    # You could also simulate a loop that sends candle data periodically
    while True:
        # Simulate receiving candle data
        candle_data = CandleData(timestamp="2024-10-23T12:00:00Z", open=100, high=105, low=99, close=104, volume=1000)
        await bot.bot_action(candle_data)

        # Check for active trades
        active_trades = bot.list_active_trades()
        print("Active Trades:", active_trades)

        await asyncio.sleep(1)  # Sleep for a while before sending the next candle data

if __name__ == "__main__":
    asyncio.run(main())
