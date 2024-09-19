import logging

class AizyBot:
    """
    AizyBot is a base class for building trading bots that interact with a 
    WebSocket server. It handles logging, trade management, and provides 
    methods for opening and closing long/short trades. The class is designed 
    to be subclassed, allowing the user to implement custom trading strategies.

    Attributes:
        log_file (str): The file where logs will be written.
        logger (logging.Logger): The logger instance used for logging bot actions.
        uri (str): The WebSocket URI that the bot connects to.
        on_message_callbacks (list): A list of callback functions triggered by messages from the WebSocket.
        opened_trade (bool): A flag indicating whether a trade is currently open.
        currents_trades (list): A list containing details of current trades.
        pair (str): The trading pair for which the bot opens trades.
    """

    def __init__(self, log_file="log.txt", uri="ws://localhost:8080", pair="BTC/USDT"):
        """
        Initializes the AizyBot instance with logging, WebSocket URI, and the trading pair.

        Args:
            log_file (str): The log file to store log messages. Defaults to "log.txt".
            uri (str): The WebSocket URI to connect to. Defaults to "ws://localhost:8080".
            pair (str): The trading pair for the bot. Defaults to "BTC/USDT".
        """
        self.log_file = log_file
        self.logger = logging.getLogger("AizyBot")
        self.logger.setLevel(logging.DEBUG)
        self.file_handler = logging.FileHandler(log_file)
        self.file_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(self.file_handler)
        self.uri = uri
        self.on_message_callbacks = []
        self.opened_trade = False
        self.currents_trades = []
        self.pair = pair

    def _set_pair(self, pair):
        """
        Sets the trading pair for the bot.

        Args:
            pair (str): The trading pair to set (e.g., "ETH/USDT").
        """
        self.pair = pair

    def bot_action(callback):
        """
        A method that must be implemented by the subclass to define the bot's
        specific trading action.

        Args:
            callback: A function to define custom bot behavior.

        Raises:
            NotImplementedError: If not implemented in a subclass.
        """
        raise NotImplementedError("bot_action method should be implemented by the subclass")

    async def bot_setup(self, exchange, stream_name):
        """
        A method to set up the bot with an exchange and WebSocket stream.
        Should be implemented by the subclass.

        Args:
            exchange (str): The exchange to connect to.
            stream_name (str): The stream name to subscribe to.

        Raises:
            NotImplementedError: If not implemented in a subclass.
        """
        raise NotImplementedError("bot_setup method should be implemented by the subclass")

    async def test(self):
        """
        A simple test method for asynchronous operations.
        """
        print("Test")

    async def start(self):
        """
        Starts the bot by running initial setup operations, including calling the
        test method.
        """
        await self.test()

    def _log(self, msg):
        """
        Internal method to log a message.

        Args:
            msg (str): The message to log.
        """
        self.logger.debug(msg)

    def open_long(self, amount, leverage, stop_loss, take_profit):
        """
        Opens a long trade.

        Args:
            amount (float): The amount of the asset to trade.
            leverage (int): The leverage to apply to the trade.
            stop_loss (float): The stop loss price.
            take_profit (float): The take profit price.

        Logs the trade details and adds it to the list of current trades.
        """
        self._log(f"Opened Long on {self.pair} with {amount} at {leverage}x leverage with stop loss at {stop_loss} and take profit at {take_profit}")
        print("Open Long")
        self.currents_trades.append({"side": "long", "pair": self.pair, "amount": amount, "leverage": leverage, "stop_loss": stop_loss, "take_profit": take_profit})
        self.opened_trade = True

    def close_trade(self):
        """
        Closes the current trade.

        Logs the action and sets the `opened_trade` flag to False.
        """
        self._log("Close Trade")
        print("Close Trade")
        self.opened_trade = False

    def open_short(self, amount, leverage, stop_loss, take_profit):
        """
        Opens a short trade.

        Args:
            amount (float): The amount of the asset to trade.
            leverage (int): The leverage to apply to the trade.
            stop_loss (float): The stop loss price.
            take_profit (float): The take profit price.

        Logs the trade details and adds it to the list of current trades.
        """
        self._log(f"Opened Short on {self.pair} with {amount} at {leverage}x leverage with stop loss at {stop_loss} and take profit at {take_profit}")
        print("Open Short")
        self.currents_trades.append({"side": "short", "pair": self.pair, "amount": amount, "leverage": leverage, "stop_loss": stop_loss, "take_profit": take_profit})
        self.opened_trade = True

    def close_short(self):
        """
        Closes the current short trade.

        Logs the action and sets the `opened_trade` flag to False.
        """
        self._log("Close Short")
        print("Close Short")
        self.opened_trade = False
