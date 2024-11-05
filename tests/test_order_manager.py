import unittest
from unittest.mock import MagicMock
from src.OrderManager import Order, OrderManager, OrderStatus

class TestOrderManager(unittest.TestCase):

    def setUp(self):
        self.logger = MagicMock()
        self.order_manager = OrderManager(self.logger)

    def test_create_order(self):
        order = self.order_manager.create_order("buy", 1.0, 50000, "BTC/USD")
        self.assertEqual(order.status, OrderStatus.CREATED)
        self.assertEqual(order.side, "buy")
        self.assertEqual(order.amount, 1.0)
        self.assertEqual(order.pair, "BTC/USD")

    def test_validate_order_success(self):
        order = self.order_manager.create_order("buy", 1.0, 50000, "BTC/USD")
        self.order_manager.validate_order(order)
        self.assertEqual(order.status, OrderStatus.VALIDATED)

    def test_validate_order_failure(self):
        order = self.order_manager.create_order("buy", -1.0, 50000, "BTC/USD")
        self.order_manager.validate_order(order)
        self.assertEqual(order.status, OrderStatus.FAILED)

    def test_execute_market_order(self):
        order = self.order_manager.create_order("buy", 1.0, 50000, "BTC/USD")
        self.order_manager.validate_order(order)
        executed = self.order_manager.execute_order(order)
        self.assertTrue(executed)
        self.assertEqual(order.status, OrderStatus.ACTIVE)

    def test_cancel_order(self):
        order = self.order_manager.create_order("buy", 1.0, 50000, "BTC/USD")
        self.order_manager.validate_order(order)
        canceled = self.order_manager.cancel_order(order)
        self.assertTrue(canceled)
        self.assertEqual(order.status, OrderStatus.CANCELLED)

if __name__ == "__main__":
    unittest.main()
