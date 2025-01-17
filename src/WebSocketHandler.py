import logging
from typing import Optional, Any, Callable, Awaitable, List, Union

class WebSocketHandler:
    """Handles WebSocket connections and message routing for the trading bot.
    
    Attributes:
        logger: Logger instance for recording events
        connected: Boolean indicating connection status
        ws: WebSocket connection instance
        callback: Callback function for handling incoming messages
    """
    
    def __init__(self, logger: logging.Logger) -> None:
        self.logger: logging.Logger = logger
        self.connected: bool = False
        self.ws: Optional[Any] = None
        self.callback: Optional[Callable[[Any], Awaitable[None]]] = None

    async def connect(self) -> None:
        """Establish WebSocket connection."""
        self.connected = True
        self.logger.info("Connected to WebSocket.")

    def set_websocket(self, ws: Any) -> None:
        """Set the WebSocket instance and initialize subscription if available.
        
        Args:
            ws: WebSocket instance to be used for communication
        """
        self.ws = ws
        if hasattr(ws, 'subscribe'):
            ws.subscribe(self.on_message)
        self.logger.info("WebSocket handler initialized")

    async def on_message(self, data: Any) -> None:
        """Handle incoming WebSocket messages.
        
        Args:
            data: Message data received from WebSocket
        """
        if self.callback:
            await self.callback(data)
        else:
            self.logger.warning("Received message but no callback is set")

    def set_callback(self, callback: Callable[[Any], Awaitable[None]]) -> None:
        """Set the callback function for handling incoming messages.
        
        Args:
            callback: Async function to handle incoming messages
        """
        self.callback = callback
        self.logger.info("Callback set for WebSocket messages")
