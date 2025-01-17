from aizypy import AizyBot
from aizypy import TestEngine
import asyncio

class MyBot(AizyBot):
    async def bot_setup(self):
        print("Setting up bot...")
        await super().bot_setup()

    async def bot_action(self, candle_data):
        active_trades = self.list_active_trades()
        
        if candle_data.close > candle_data.open and not active_trades:
            print(f"Buy signal detected! Close: {candle_data.close}")
            await self.place_order("buy", 1.0, candle_data.close, "BTC/USD", "market")
        elif candle_data.close < candle_data.open and active_trades:
            print(f"Sell signal detected! Close: {candle_data.close}")
            print(f"Active trades: {active_trades}")
            await self.close_trade(active_trades[-1])


if __name__ == "__main__":
    asyncio.run(TestEngine.test(MyBot, duration=120, interval=1))