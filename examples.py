from src.AizyBot import AizyBot
from src.TestEngine import TestEngine
import asyncio

class MyBot(AizyBot):
    async def bot_setup(self, exchange: str, stream_name: str):
        print(f"Setting up bot for {exchange} on stream {stream_name}")
        await super().bot_setup(exchange, stream_name)  # Ensure parent setup is also called

    async def bot_action(self, candle_data):
        # Implement custom trading logic with improved signal checks
        active_trades = self.list_active_trades()
        input()
        # Check for a buy signal if no active trades
        if candle_data.close > candle_data.open and not active_trades:
            print("Buy signal detected!")
            await self.place_order("buy", 1.0, candle_data.close, "BTC/USD", "market")
        # Check for a sell signal only if there is an active trade to close it
        elif candle_data.close < candle_data.open and active_trades:
            print("Sell signal detected!")
            print("We have an active order, closing it...")
            print(active_trades)
            print(candle_data.close)
            await self.close_trade(active_trades[-1])

# Run the test engine with MyBot
asyncio.run(TestEngine.test(MyBot, duration=20, interval=1))
