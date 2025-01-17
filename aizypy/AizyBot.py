import logging
from typing import Optional, Any, Callable, Awaitable, List, Union
from .CandleData import CandleData
from .OrderManager import OrderManager, OrderStatus
from .Trade import Trade
from .WebSocketHandler import WebSocketHandler

class AizyBot:
    """Base trading bot class implementing core trading functionality."""
    
    def __init__(self, log_file: str = "log.txt", websocket: Optional[Any] = None) -> None:
        self.logger: logging.Logger = self._setup_logger(log_file)
        self.websocket_handler: WebSocketHandler = WebSocketHandler(self.logger)
        self.order_manager: OrderManager = OrderManager(self.logger)
        self.websocket_handler.set_websocket(websocket)
        self.websocket_handler.set_callback(self.bot_action)

    async def bot_setup(self) -> None:
        """Initialize bot settings and configurations."""
        self.logger.info("Bot Setup")

    async def bot_action(self, candle_data: CandleData) -> None:
        """Process incoming candle data and execute trading strategy.
        
        Args:
            candle_data: Candlestick data for analysis
            
        Raises:
            NotImplementedError: This method must be implemented by subclasses
        """
        raise NotImplementedError("bot_action method should be implemented by the subclass")

    def _setup_logger(self, log_file: str) -> logging.Logger:
        """Configure logging for the bot.
        
        Args:
            log_file: Path to the log file
            
        Returns:
            Configured logger instance
        """
        logger = logging.getLogger("AizyBot")
        logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
        return logger

    async def start(self) -> None:
        """Start the bot and establish WebSocket connection."""
        await self.websocket_handler.connect()
        self.logger.info("Bot started and listening for messages.")

    async def place_order(self, side: str, amount: float, price: float, pair: str, order_type: str = "market") -> None:
        """Place a new trading order.
        
        Args:
            side: Order side ('buy' or 'sell')
            amount: Order quantity
            price: Order price
            pair: Trading pair (e.g., 'BTC/USD')
            order_type: Type of order (default: 'market')
        """
        order = self.order_manager.create_order(side, amount, price, pair, order_type)
        
        if self.order_manager.validate_order(order):
            self.order_manager.execute_order(order)
            if self.websocket_handler.ws:
                await self.websocket_handler.ws.send_order(order)

    async def close_trade(self, order: Union[str, Trade]) -> None:
        """Close an active trade.
        
        Args:
            order: Either the order ID (str) or Trade object to close
        """
        if isinstance(order, str):
            order = next((o for o in self.order_manager.orders if o.order_id == order), None)
        
        if order and order.status == OrderStatus.ACTIVE:
            self.order_manager.close_order(order)
            if self.websocket_handler.ws:
                await self.websocket_handler.ws.send_close_order(order)

    def list_active_trades(self) -> List[Trade]:
        """Get all active trades.
        
        Returns:
            List of active Trade objects
        """
        return self.order_manager.list_active_trades()

    def list_pending_orders(self) -> List[Trade]:
        """Get all pending orders.
        
        Returns:
            List of pending Trade objects
        """
        return self.order_manager.list_pending_orders()
