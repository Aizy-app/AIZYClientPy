=============
SDK Reference
=============

AizyBot
-------

.. py:class:: AizyBot

    Base trading bot class implementing core trading functionality.

    .. py:attribute:: logger
        :type: logging.Logger

        Logger instance for recording events

    .. py:attribute:: websocket_handler
        :type: WebSocketHandler

        Handler for WebSocket communications

    .. py:attribute:: order_manager
        :type: OrderManager

        Manager for handling trading orders

    .. py:method:: __init__(log_file: str = "log.txt", websocket: Optional[Any] = None) -> None

        Initialize the bot with logging and WebSocket setup.

        :param log_file: Path to the log file
        :param websocket: Optional WebSocket instance

    .. py:method:: async bot_setup() -> None

        Initialize bot settings and configurations.

    .. py:method:: async bot_action(candle_data: CandleData) -> None

        Process incoming candle data and execute trading strategy.

        :param candle_data: Candlestick data for analysis
        :raises NotImplementedError: This method must be implemented by subclasses

    .. py:method:: async start() -> None

        Start the bot and establish WebSocket connection.

    .. py:method:: async place_order(side: str, amount: float, price: float, pair: str, order_type: str = "market") -> None

        Place a new trading order.

        :param side: Order side ('buy' or 'sell')
        :param amount: Order quantity
        :param price: Order price
        :param pair: Trading pair (e.g., 'BTC/USD')
        :param order_type: Type of order (default: 'market')

    .. py:method:: async close_trade(order: Union[str, Trade]) -> None

        Close an active trade.

        :param order: Either the order ID (str) or Trade object to close

    .. py:method:: list_active_trades() -> List[Trade]

        Get all active trades.

        :return: List of active Trade objects

    .. py:method:: list_pending_orders() -> List[Trade]

        Get all pending orders.

        :return: List of pending Trade objects

WebSocketHandler
--------------

.. py:class:: WebSocketHandler

    Handles WebSocket communications for real-time data and order execution.

    .. py:attribute:: logger
        :type: logging.Logger

        Logger instance for recording WebSocket events

    .. py:attribute:: ws
        :type: Optional[Any]

        WebSocket connection instance

    .. py:method:: __init__(logger: logging.Logger) -> None

        Initialize the WebSocket handler.

        :param logger: Logger instance for recording events

    .. py:method:: set_websocket(websocket: Optional[Any]) -> None

        Set the WebSocket connection instance.

        :param websocket: WebSocket instance to use

    .. py:method:: set_callback(callback: Callable[[CandleData], Awaitable[None]]) -> None

        Set the callback function for handling incoming data.

        :param callback: Async function to handle candle data

    .. py:method:: async connect() -> None

        Establish WebSocket connection.

    .. py:method:: async disconnect() -> None

        Close WebSocket connection.

    .. py:method:: async send_order(order: Trade) -> None

        Send order through WebSocket.

        :param order: Trade object to send

    .. py:method:: async send_close_order(order: Trade) -> None

        Send order closure request through WebSocket.

        :param order: Trade object to close

Example Usage
-----------

Here's a basic example of using these classes together:

.. code-block:: python

    class MyBot(AizyBot):
        async def bot_action(self, candle: CandleData) -> None:
            # Implement trading strategy
            if candle.close > some_condition:
                await self.place_order("buy", 1.0, candle.close, "BTC/USD")

    # Create and start the bot
    bot = MyBot()
    await bot.start()
