import uuid
from datetime import datetime
from enum import Enum
import logging
import pytz
from typing import List, Optional

class OrderStatus(Enum):
    CREATED = "Created"
    VALIDATED = "Validated"
    ACTIVE = "Active"      # For market orders that are actively traded
    PENDING = "Pending"    # For limit orders waiting for price confirmation
    CANCELLED = "Cancelled"
    FAILED = "Failed"
    CLOSED = "Closed"

class Order:
    def __init__(self, side: str, amount: float, price: float, pair: str, order_type: str = "market"):
        self.order_id = str(uuid.uuid4())
        self.side = side  # "buy" or "sell"
        self.amount = amount
        self.price = price
        self.pair = pair
        self.order_type = order_type  # "market" or "limit"
        self.status = OrderStatus.CREATED
        self.timestamp = datetime.now(pytz.timezone('America/New_York'))  # Set to New York time, timezone-aware

    def __repr__(self):
        return (f"Order(id={self.order_id}, pair={self.pair}, side={self.side}, amount={self.amount}, "
                f"price={self.price}, type={self.order_type}, status={self.status})")

class OrderManager:
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.orders: List[Order] = []
        self.active_trades: List[Order] = []  # List to hold active market orders

    def create_order(self, side: str, amount: float, price: float, pair: str, order_type: str = "market") -> Order:
        """Creates and logs a new order."""
        order = Order(side=side, amount=amount, price=price, pair=pair, order_type=order_type)
        self.orders.append(order)
        self.logger.info(f"Order created: {order}")
        return order

    def validate_order(self, order: Order) -> bool:
        """Validates the order based on criteria (e.g., amount > 0)."""
        if order.amount <= 0:
            order.status = OrderStatus.FAILED
            self.logger.error(f"Order validation failed for {order.order_id}: amount must be positive.")
            return False
        order.status = OrderStatus.VALIDATED
        self.logger.info(f"Order validated: {order.order_id}")
        return True

    def execute_order(self, order: Order) -> bool:
        """Executes the order based on type (market or limit)."""
        if order.status == OrderStatus.VALIDATED:
            if order.order_type == "market":
                order.status = OrderStatus.ACTIVE
                self.active_trades.append(order)
                self.logger.info(f"Market order activated: {order}")
            elif order.order_type == "limit":
                order.status = OrderStatus.PENDING
                self.logger.info(f"Limit order pending execution: {order}")
            return True
        else:
            self.logger.error(f"Order not validated and cannot be executed: {order}")
            return False

    def close_order(self, order: Order) -> bool:
        """Closes an active order."""
        if order.status == OrderStatus.ACTIVE:
            order.status = OrderStatus.CLOSED
            self.active_trades = [o for o in self.active_trades if o.order_id != order.order_id]  # Remove from active trades
            self.logger.info(f"Order closed: {order}")
            return True
        else:
            self.logger.warning(f"Cannot close order not in active status: {order}")
            return False

    def cancel_order(self, order: Order) -> bool:
        """Cancels an order if it is in a modifiable state (not active or closed)."""
        if order.status in [OrderStatus.CREATED, OrderStatus.VALIDATED, OrderStatus.PENDING]:
            order.status = OrderStatus.CANCELLED
            self.logger.info(f"Order cancelled: {order}")
            return True
        self.logger.warning(f"Order cannot be cancelled (already active, executed, or failed): {order}")
        return False

    def list_active_trades(self) -> List[Order]:
        """Returns a list of currently active trades."""
        active_trades = [order for order in self.orders if order.status == OrderStatus.ACTIVE]
        self.logger.info(f"Listing active trades: {active_trades}")
        return active_trades

    def list_pending_orders(self) -> List[Order]:
        """Returns a list of currently pending orders."""
        pending_orders = [order for order in self.orders if order.status == OrderStatus.PENDING]
        self.logger.info(f"Listing pending orders: {pending_orders}")
        return pending_orders

    def get_order_by_id(self, order_id: str) -> Optional[Order]:
        """Finds an order by its ID."""
        for order in self.orders:
            if order.order_id == order_id:
                return order
        self.logger.warning(f"Order ID {order_id} not found.")
        return None
    
    def __repr__(self):
        return f"OrderManager(orders={self.orders}, active_trades={self.active_trades})"
