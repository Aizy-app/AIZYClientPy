"""
AIZYClientPy - A Python framework for creating and testing trading bots
"""

from .AizyBot import AizyBot
from .CandleData import CandleData
from .OrderManager import OrderManager, OrderStatus, Order
from .TestEngine import TestEngine
from .Trade import Trade
from .WebSocketHandler import WebSocketHandler

__version__ = "0.2.2"
__all__ = [
    "AizyBot",
    "CandleData",
    "OrderManager",
    "OrderStatus",
    "Order",
    "TestEngine",
    "Trade",
    "WebSocketHandler",
] 