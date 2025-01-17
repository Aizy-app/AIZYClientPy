import uuid
from datetime import datetime
from enum import Enum
import logging
from dataclasses import dataclass, field
import pytz
from typing import List, Optional

class OrderStatus(Enum):
    """Enumeration of possible order statuses in the trading system.
    
    Attributes:
        CREATED: Initial status when order is first created
        VALIDATED: Order has passed validation checks
        ACTIVE: Market order that is currently being traded
        PENDING: Limit order waiting for price target
        CANCELLED: Order was cancelled before execution
        FAILED: Order failed validation or execution
        CLOSED: Order has been completed and closed
    """
    CREATED = "Created"
    VALIDATED = "Validated"
    ACTIVE = "Active"
    PENDING = "Pending"
    CANCELLED = "Cancelled"
    FAILED = "Failed"
    CLOSED = "Closed"

@dataclass
class Order:
    """Represents a trading order with its parameters and current status.
    
    Attributes:
        side: Trading direction ('buy' or 'sell')
        amount: Quantity to trade
        price: Target price for the trade
        pair: Trading pair symbol (e.g., 'BTC/USD')
        order_type: Type of order ('market' or 'limit')
        order_id: Unique identifier for the order
        status: Current status of the order
        timestamp: Time when the order was created
    """
    side: str
    amount: float
    price: float
    pair: str
    order_type: str = "market"
    order_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: OrderStatus = OrderStatus.CREATED
    timestamp: datetime = field(default_factory=lambda: datetime.now(pytz.timezone('America/New_York')))

    def __repr__(self) -> str:
        """Return a string representation of the order."""
        return (f"Order(id={self.order_id}, pair={self.pair}, side={self.side}, amount={self.amount}, "
                f"price={self.price}, type={self.order_type}, status={self.status})")

class OrderManager:
    """Manages the lifecycle of trading orders including creation, execution, and tracking.
    
    This class handles all aspects of order management including validation,
    execution, cancellation, and status tracking. It maintains lists of both
    active trades and pending orders.
    
    Attributes:
        logger: Logger instance for recording order events
        orders: List of all orders ever created
        active_trades: List of currently active market orders
    """
    
    def __init__(self, logger: logging.Logger) -> None:
        """Initialize the OrderManager.
        
        Args:
            logger: Logger instance for recording order events
        """
        self.logger: logging.Logger = logger
        self.orders: List[Order] = []
        self.active_trades: List[Order] = []  # List to hold active market orders

    def create_order(self, side: str, amount: float, price: float, pair: str, order_type: str = "market") -> Order:
        """Create a new order and add it to the order list.
        
        Args:
            side: Trading direction ('buy' or 'sell')
            amount: Quantity to trade
            price: Target price for the trade
            pair: Trading pair symbol
            order_type: Type of order ('market' or 'limit')
            
        Returns:
            The newly created Order instance
        """
        order = Order(side=side, amount=amount, price=price, pair=pair, order_type=order_type)
        self.orders.append(order)
        self.logger.info(f"Order created: {order}")
        return order

    def validate_order(self, order: Order) -> bool:
        """Validate an order based on predefined criteria.
        
        Args:
            order: The Order instance to validate
            
        Returns:
            True if validation passes, False otherwise
        """
        if order.amount <= 0:
            order.status = OrderStatus.FAILED
            self.logger.error(f"Order validation failed for {order.order_id}: amount must be positive.")
            return False
        order.status = OrderStatus.VALIDATED
        self.logger.info(f"Order validated: {order.order_id}")
        return True

    def execute_order(self, order: Order) -> bool:
        """Execute a validated order based on its type.
        
        Args:
            order: The Order instance to execute
            
        Returns:
            True if execution starts successfully, False otherwise
        """
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
        """Close an active order.
        
        Args:
            order: The Order instance to close
            
        Returns:
            True if order was closed successfully, False otherwise
        """
        if order.status == OrderStatus.ACTIVE:
            order.status = OrderStatus.CLOSED
            self.active_trades = [o for o in self.active_trades if o.order_id != order.order_id]
            self.logger.info(f"Order closed: {order}")
            return True
        else:
            self.logger.warning(f"Cannot close order not in active status: {order}")
            return False

    def cancel_order(self, order: Order) -> bool:
        """Cancel an order if it's in a cancellable state.
        
        Args:
            order: The Order instance to cancel
            
        Returns:
            True if order was cancelled successfully, False otherwise
        """
        if order.status in [OrderStatus.CREATED, OrderStatus.VALIDATED, OrderStatus.PENDING]:
            order.status = OrderStatus.CANCELLED
            self.logger.info(f"Order cancelled: {order}")
            return True
        self.logger.warning(f"Order cannot be cancelled (already active, executed, or failed): {order}")
        return False

    def list_active_trades(self) -> List[Order]:
        """Get all currently active trades.
        
        Returns:
            List of Order instances with ACTIVE status
        """
        active_trades = [order for order in self.orders if order.status == OrderStatus.ACTIVE]
        self.logger.info(f"Listing active trades: {active_trades}")
        return active_trades

    def list_pending_orders(self) -> List[Order]:
        """Get all currently pending orders.
        
        Returns:
            List of Order instances with PENDING status
        """
        pending_orders = [order for order in self.orders if order.status == OrderStatus.PENDING]
        self.logger.info(f"Listing pending orders: {pending_orders}")
        return pending_orders

    def get_order_by_id(self, order_id: str) -> Optional[Order]:
        """Find an order by its unique identifier.
        
        Args:
            order_id: The unique identifier of the order to find
            
        Returns:
            The Order instance if found, None otherwise
        """
        for order in self.orders:
            if order.order_id == order_id:
                return order
        self.logger.warning(f"Order ID {order_id} not found.")
        return None
    
    def __repr__(self) -> str:
        """Return a string representation of the OrderManager."""
        return f"OrderManager(orders={self.orders}, active_trades={self.active_trades})"
