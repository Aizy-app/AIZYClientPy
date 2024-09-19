import json
from .testing_engine.QuotesGen import QuotesGenerator
from .bot.AizyBotcls import AizyBot
import asyncio

class TradingBot(AizyBot):
    def __init__(self, pair="BTC/USDT"):
        super().__init__(pair=pair)
        self.last_100_prices = []

    async def bot_action(self, message):
        message = json.loads(message)
        last_price = message["Close"]
        # Add the last price to the list of last 100 prices and if the list has more than 100 prices, remove the first price
        self.last_100_prices.append(float(last_price))
        # mean of the last 100 prices in percentage
        mean_of_last_100_prices = (self.last_100_prices[-1] - self.last_100_prices[0]) / self.last_100_prices[0]
        # print the mean of the last 100 prices
        print(f"Mean of the last 100 prices: {sum(self.last_100_prices) / len(self.last_100_prices)}")
        print(f"Mean_of_last_100_prices %: {mean_of_last_100_prices}")

class TestEngine:
    def __init__(self, bot : TradingBot) -> None:
        self.quotes_gen = QuotesGenerator()
        self.bot = bot

    async def test_run(self):
        self.quotes_gen.generate_prices()
        for i in range(len(self.quotes_gen.prices)):
            message = self.quotes_gen.prices.iloc[i].to_json()
            await self.bot.bot_action(message)    

if __name__ == "__main__":
    mybot = TradingBot()
    
    test_engine = TestEngine(mybot)
    asyncio.run(test_engine.test_run())