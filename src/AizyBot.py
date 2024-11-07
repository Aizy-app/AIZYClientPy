import logging
from .CandleData import CandleData
from .OrderManager import OrderManager, OrderStatus

class WebSocketHandler:
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.connected = False
        self.ws = None
        self.callback = None

    async def connect(self):
        self.connected = True
        self.logger.info("Connected to WebSocket.")

    def set_websocket(self, ws):
        self.ws = ws
        if hasattr(ws, 'subscribe'):
            ws.subscribe(self.on_message)
        self.logger.info("WebSocket handler initialized")

    async def on_message(self, data):
        if self.callback:
            await self.callback(data)
        else:
            self.logger.warning("Received message but no callback is set")

    def set_callback(self, callback):
        self.callback = callback
        self.logger.info("Callback set for WebSocket messages")

class AizyBot:
    def __init__(self, log_file: str = "log.txt", websocket: WebSocketHandler = None):
        self.logger = self._setup_logger(log_file)
        self.websocket_handler = WebSocketHandler(self.logger)
        self.order_manager = OrderManager(self.logger)
        # Initialize websocket handler with the provided websocket
        self.websocket_handler.set_websocket(websocket)
        # Set the callback for incoming messages
        self.websocket_handler.set_callback(self.bot_action)

    async def bot_setup(self):
        self.logger.info("Bot Setup")

    async def bot_action(self, candle_data: CandleData):
        raise NotImplementedError("bot_action method should be implemented by the subclass")

    def _setup_logger(self, log_file: str):
        logger = logging.getLogger("AizyBot")
        logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
        return logger

    async def start(self):
        await self.websocket_handler.connect()
        self.logger.info("Bot started and listening for messages.")

    async def place_order(self, side: str, amount: float, price: float, pair: str, order_type: str = "market"):
        """Place an order through the OrderManager."""
        order = self.order_manager.create_order(side, amount, price, pair, order_type)
        
        if self.order_manager.validate_order(order):
            self.order_manager.execute_order(order)
            # Notify WebSocket of new order
            if self.websocket_handler.ws:
                await self.websocket_handler.ws.send_order(order)

    async def close_trade(self, order):
        """Close an active trade through the OrderManager."""
        if isinstance(order, str):
            # If order_id was passed
            order = next((o for o in self.order_manager.orders if o.order_id == order), None)
        
        if order and order.status == OrderStatus.ACTIVE:
            self.order_manager.close_order(order)
            # Notify WebSocket of closed order
            if self.websocket_handler.ws:
                await self.websocket_handler.ws.send_close_order(order)

                
    def list_active_trades(self):
        """List all active trades through the OrderManager."""
        return self.order_manager.list_active_trades()

    def list_pending_orders(self):
        """List all pending orders through the OrderManager."""
        return self.order_manager.list_pending_orders()
