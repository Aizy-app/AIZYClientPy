import logging
import asyncio
import uuid
from .CandleData import CandleData
from .OrderManager import OrderManager, OrderStatus

class Trade:
    def __init__(self, side: str, amount: str, leverage: str, pair: str, stop_loss: str = None, take_profit: str = None, trade_id: str = None):
        self.trade_id = trade_id or str(uuid.uuid4())
        self.side = side
        self.amount = amount
        self.leverage = leverage
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.pair = pair

    def __repr__(self):
        return (f"Trade(id={self.trade_id}, pair={self.pair}, side={self.side}, amount={self.amount}, "
                f"leverage={self.leverage}, stop_loss={self.stop_loss}, take_profit={self.take_profit})")

class WebSocketHandler:
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.connected = False

    async def connect(self):
        self.connected = True

    async def listen(self, on_message):
        while self.connected:
            await asyncio.sleep(1)  # Simulate listening for messages

    async def send(self, message: str):
        self.logger.info(f"Simulated send: {message}")

class AizyBot:
    def __init__(self, log_file: str = "log.txt"):
        self.logger = self._setup_logger(log_file)
        self.websocket_handler = WebSocketHandler(self.logger)
        self.order_manager = OrderManager(self.logger)

    def _setup_logger(self, log_file: str):
        logger = logging.getLogger("AizyBot")
        logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
        return logger

    async def bot_setup(self, exchange: str, stream_name: str):
        await self.websocket_handler.connect()
        self.logger.info(f"Bot connected to {exchange} with stream {stream_name}.")

    async def bot_action(self, candle_data: CandleData):
        raise NotImplementedError("bot_action method should be implemented by the subclass")

    async def start(self):
        await self.websocket_handler.connect()
        self.logger.info("Bot started and listening for messages.")

    async def place_order(self, side: str, amount: float, price: float, pair: str, order_type: str = "market"):
        order = self.order_manager.create_order(side, amount, price, pair, order_type)
        
        if self.order_manager.validate_order(order):
            self.order_manager.execute_order(order)

    async def close_trade(self, trade: Trade):
        self.order_manager.close_order(trade)

    def list_active_trades(self):
        """List all active trades through the OrderManager."""
        return self.order_manager.list_active_trades()

    def list_pending_orders(self):
        """List all pending orders through the OrderManager."""
        return self.order_manager.list_pending_orders()
