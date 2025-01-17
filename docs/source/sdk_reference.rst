=============
SDK Reference
=============

This section provides detailed documentation for all components of the AIZYClientPy framework.

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

OrderManager
-----------

.. py:class:: OrderStatus

    Enumeration of possible order statuses in the trading system.

    .. py:attribute:: CREATED
        Status when order is first created

    .. py:attribute:: VALIDATED
        Order has passed validation checks

    .. py:attribute:: ACTIVE
        Market order that is currently being traded

    .. py:attribute:: PENDING
        Limit order waiting for price target

    .. py:attribute:: CANCELLED
        Order was cancelled before execution

    .. py:attribute:: FAILED
        Order failed validation or execution

    .. py:attribute:: CLOSED
        Order has been completed and closed

.. py:class:: Order

    Represents a trading order with its parameters and current status.

    .. py:attribute:: side
        :type: str
        Trading direction ('buy' or 'sell')

    .. py:attribute:: amount
        :type: float
        Quantity to trade

    .. py:attribute:: price
        :type: float
        Target price for the trade

    .. py:attribute:: pair
        :type: str
        Trading pair symbol (e.g., 'BTC/USD')

    .. py:attribute:: order_type
        :type: str
        Type of order ('market' or 'limit')

    .. py:attribute:: order_id
        :type: str
        Unique identifier for the order

    .. py:attribute:: status
        :type: OrderStatus
        Current status of the order

    .. py:attribute:: timestamp
        :type: datetime
        Time when the order was created

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

CandleData
---------

.. py:class:: CandleData

    Represents market candlestick data.

    .. py:attribute:: timestamp
        :type: datetime
        Time when the candle was created

    .. py:attribute:: open
        :type: float
        Opening price of the period

    .. py:attribute:: high
        :type: float
        Highest price during the period

    .. py:attribute:: low
        :type: float
        Lowest price during the period

    .. py:attribute:: close
        :type: float
        Closing price of the period

    .. py:attribute:: volume
        :type: float
        Trading volume during the period

Trade
-----

.. py:class:: Trade

    Represents a trade with its execution details.

    .. py:attribute:: order_id
        :type: str
        Unique identifier for the trade

    .. py:attribute:: symbol
        :type: str
        Trading pair symbol

    .. py:attribute:: side
        :type: str
        Trading direction ('buy' or 'sell')

    .. py:attribute:: quantity
        :type: float
        Trade quantity

    .. py:attribute:: price
        :type: float
        Execution price

    .. py:attribute:: timestamp
        :type: datetime
        Time of trade execution

TestEngine
---------

.. py:class:: TestEngine

    Engine for testing trading bots with simulated market conditions.

    .. py:method:: async test(bot_class: Type[AizyBot], duration: int = 60, interval: int = 1) -> None

        Run a trading bot test with simulated market data.

        :param bot_class: Trading bot class to test
        :param duration: Test duration in minutes
        :param interval: Candle interval in minutes
        
    .. py:method:: generate_test_data(duration: int, interval: int) -> List[CandleData]

        Generate simulated market data for testing.

        :param duration: Duration to generate data for (minutes)
        :param interval: Time between candles (minutes)
        :return: List of CandleData objects

Example Usage
-----------

Here's a basic example of creating and testing a trading bot:

.. code-block:: python

    from AizyClientPy import AizyBot, CandleData, TestEngine

    class MyBot(AizyBot):
        async def bot_action(self, candle: CandleData) -> None:
            if some_condition:
                await self.place_order("buy", 1.0, candle.close, "BTC/USD")

    # Test the bot
    await TestEngine.test(MyBot, duration=120, interval=1)
