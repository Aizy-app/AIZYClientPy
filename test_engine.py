from .testing_engine.QuotesGen import QuotesGenerator
from .bot import AizyBot

class TestEngine:
    def __init__(self, bot) -> None:
        self.quotes_gen = QuotesGenerator()
        self.bot = bot

    def test_run(self):
        self.quotes_gen.generate_prices()
        for i in range(len(self.quotes_gen.prices)):
            message = self.quotes_gen.prices.iloc[i].to_json()
            self.bot.bot_action(message)