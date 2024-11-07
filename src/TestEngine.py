from typing import Type, List, Dict, Union
import random
import asyncio
from datetime import datetime, timedelta
from .AizyBot import AizyBot
from .CandleData import CandleData
from .OrderManager import Order

class MockWebSocket:
    def __init__(self):
        self.connected = False
        self.subscribers = []
        self.orders = []
        self.closed_orders = []
        self.on_order = None
        self.on_close_order = None

    async def connect(self):
        self.connected = True
        return True

    async def disconnect(self):
        self.connected = False
        return True

    def subscribe(self, callback):
        self.subscribers.append(callback)

    async def emit_data(self, data):
        for subscriber in self.subscribers:
            await subscriber(data)

    async def send_order(self, order):
        """Record new orders"""
        self.orders.append(order)
        print(f"WebSocket received new order: {order}")
        if self.on_order:
            self.on_order(order)

    async def send_close_order(self, order):
        """Record closed orders"""
        if order in self.orders:
            self.orders.remove(order)
            self.closed_orders.append(order)
            print(f"WebSocket received close order: {order}")
            if self.on_close_order:
                self.on_close_order(order)

class TestEngine:
    def __init__(self, bot_class: Type[AizyBot], duration: int = 60, interval: int = 1) -> None:
        
        self.duration: int = duration
        self.interval: int = interval
        self.trade_log: List[Dict[str, Union[str, float]]] = []
        self.forced_trade_log = []  # Separate log for forced closes
        self.profit_loss: float = 0.0
        self.mock_ws = MockWebSocket()

        self.bot_instance: AizyBot = bot_class(websocket=self.mock_ws)
        self.current_price = 0
        self.current_timestamp = datetime(2024, 1, 1)  # Start from a fixed date
        self.open_trade_times = {}

    async def run(self) -> None:
        # Setup WebSocket handlers for order tracking
        self.mock_ws.on_order = self.handle_new_order
        self.mock_ws.on_close_order = self.handle_close_order
        
        await self.bot_instance.bot_setup()
        await self.mock_ws.connect()
        await self.simulate_market_data()
        await self.close_all_trades()
        await self.mock_ws.disconnect()
        
        self.display_summary()
        self.check_for_active_trade_alerts()

    async def simulate_market_data(self) -> None:
        for i in range(self.duration):
            open_price = random.uniform(1000, 2000)
            close_price = open_price * random.uniform(0.95, 1.05)
            high_price = max(open_price, close_price) * random.uniform(1.0, 1.02)
            low_price = min(open_price, close_price) * random.uniform(0.98, 1.0)
            volume = random.uniform(10, 100)

            candle_data = CandleData(
                timestamp=self.current_timestamp,
                open=open_price,
                high=high_price,
                low=low_price,
                close=close_price,
                volume=volume
            )

            self.current_price = close_price
            await self.mock_ws.emit_data(candle_data)
            
            # Update timestamp by interval
            self.current_timestamp += timedelta(minutes=self.interval)
            await asyncio.sleep(0.1)  # Small delay for processing

    async def close_all_trades(self) -> None:
        """Close all remaining trades but log them separately"""
        active_trades = self.bot_instance.list_active_trades()
        for trade in active_trades:
            await self.bot_instance.close_trade(trade)
            # The handle_close_order will be called, but we'll mark these trades as forced
            self.forced_trade_log.append(self.trade_log.pop())  # Move the last trade to forced_trade_log

    def record_trade(self, trade: Order, exit_price: float) -> None:
        """Log trade performance for summary."""
        profit_loss: float = (exit_price - trade.price) if trade.side == "buy" else (trade.price - exit_price)
        trade_data: Dict[str, Union[str, float]] = {
            "trade_id": trade.order_id,
            "side": trade.side,
            "entry_price": trade.price,
            "exit_price": exit_price,
            "profit_loss": profit_loss
        }
        self.profit_loss += profit_loss
        self.trade_log.append(trade_data)
        print("Recorded trade:", trade_data)

    def display_summary(self) -> None:
        """Display a summary of trade performance."""
        natural_trades = self.trade_log
        natural_pl = sum(t['profit_loss'] for t in natural_trades)
        avg_duration = sum(t['duration_intervals'] for t in natural_trades) / len(natural_trades) if natural_trades else 0

        print("\n=== Natural Trading Performance (excluding forced closes) ===")
        print(f"Total Trades: {len(natural_trades)}")
        print(f"Total Profit/Loss: {natural_pl:.2f}")
        print(f"Average Trade Duration: {avg_duration:.1f} intervals")
        
        print("\nDetailed Natural Trades:")
        for trade in natural_trades:
            print(f"Trade {trade['trade_id'][:8]}... - "
                  f"{trade['side'].upper()} - "
                  f"Entry: {trade['entry_price']:.2f}, "
                  f"Exit: {trade['exit_price']:.2f}, "
                  f"P/L: {trade['profit_loss']:.2f}, "
                  f"Duration: {trade['duration_intervals']:.0f} intervals "
                  f"(from {trade['open_interval']} to {trade['close_interval']})")

        # If there were forced closes, show them separately
        if self.forced_trade_log:
            forced_pl = sum(t['profit_loss'] for t in self.forced_trade_log)
            print("\n=== Forced Closes at Test End ===")
            print(f"Forced Closes: {len(self.forced_trade_log)}")
            print(f"Forced Close P/L: {forced_pl:.2f}")
            
            print("\nDetailed Forced Closes:")
            for trade in self.forced_trade_log:
                print(f"Trade {trade['trade_id'][:8]}... - "
                      f"{trade['side'].upper()} - "
                      f"Entry: {trade['entry_price']:.2f}, "
                      f"Exit: {trade['exit_price']:.2f}, "
                      f"P/L: {trade['profit_loss']:.2f}, "
                      f"Duration: {trade['duration_intervals']:.0f} intervals")

        # Show overall statistics
        print("\n=== Overall Statistics (including forced closes) ===")
        total_trades = len(natural_trades) + len(self.forced_trade_log)
        total_pl = natural_pl + sum(t['profit_loss'] for t in self.forced_trade_log)
        print(f"Total Trades: {total_trades}")
        print(f"Total Profit/Loss: {total_pl:.2f}")
        print(f"Orders still open on WebSocket: {len(self.mock_ws.orders)}")
        print(f"Orders closed on WebSocket: {len(self.mock_ws.closed_orders)}")

    def check_for_active_trade_alerts(self) -> None:
        active_trades = self.bot_instance.list_active_trades()
        websocket_orders = len(self.mock_ws.orders)
        
        if active_trades:
            print("\n[ALERT] There are still active trades remaining at the end of the test.")
            print(f"Active Trades Count: {len(active_trades)}")
            print(f"WebSocket Open Orders Count: {websocket_orders}")
            
            if len(active_trades) != websocket_orders:
                print("[WARNING] Mismatch between active trades and WebSocket orders!")

    @classmethod
    async def test(cls, bot_class: Type[AizyBot], duration: int = 60, interval: int = 1) -> None:
        engine = cls(bot_class, duration, interval)
        await engine.run()

    def handle_new_order(self, order):
        """Handle new order events"""
        order.entry_price = self.current_price
        self.open_trade_times[order.order_id] = self.current_timestamp
        print(f"New trade opened at interval {self.get_interval_number()} - Price: {order.entry_price:.2f}")

    def handle_close_order(self, order):
        """Handle order closing events"""
        exit_price = self.current_price
        profit_loss = (exit_price - order.entry_price) if order.side == "buy" else (order.entry_price - exit_price)
        
        open_time = self.open_trade_times.get(order.order_id)
        duration_intervals = 0
        if open_time:
            duration = self.current_timestamp - open_time
            duration_intervals = duration.total_seconds() / (60 * self.interval)  # Convert to number of intervals
            del self.open_trade_times[order.order_id]
        
        trade_data = {
            "trade_id": order.order_id,
            "side": order.side,
            "entry_price": order.entry_price,
            "exit_price": exit_price,
            "profit_loss": profit_loss,
            "duration_intervals": duration_intervals,
            "open_interval": self.get_interval_number(open_time) if open_time else 0,
            "close_interval": self.get_interval_number()
        }
        
        self.profit_loss += profit_loss
        self.trade_log.append(trade_data)
        print(f"Trade closed at interval {self.get_interval_number()} - "
              f"Entry: {order.entry_price:.2f}, Exit: {exit_price:.2f}, "
              f"P/L: {profit_loss:.2f}, Duration: {duration_intervals:.0f} intervals")

    def get_interval_number(self, timestamp=None):
        """Convert timestamp to interval number (0-based)"""
        ts = timestamp or self.current_timestamp
        return int((ts - datetime(2024, 1, 1)).total_seconds() / (60 * self.interval))
