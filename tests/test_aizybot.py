import unittest
from unittest.mock import MagicMock
from src.AizyBot import AizyBot, Trade
from src.OrderManager import OrderStatus

class TestAizyBot(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.bot = AizyBot(log_file="test_log.txt")
        self.bot.order_manager.logger = MagicMock()

    async def test_place_order(self):
        await self.bot.place_order("buy", 1.0, 50000, "BTC/USD", "market")
        active_orders = self.bot.list_active_orders()
        self.assertEqual(len(active_orders), 1)
        print(active_orders)
        self.assertEqual(active_orders[0].status, OrderStatus.ACTIVE)

    async def test_close_trade(self):
        trade = Trade("buy", "1", "10", "BTC/USD")
        self.bot.active_trades.append(trade)
        
        # Await the close_trade method
        await self.bot.close_trade(trade)
        
        # Assert that the trade list is empty after closing the trade
        self.assertEqual(len(self.bot.active_trades), 0)

if __name__ == "__main__":
    unittest.main()
