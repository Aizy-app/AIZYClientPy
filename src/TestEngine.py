from typing import Type, List, Dict, Union
import random
from datetime import datetime, timedelta
from .AizyBot import AizyBot
from .CandleData import CandleData
from .OrderManager import Order

class TestEngine:
    def __init__(self, bot_class: Type[AizyBot], duration: int = 60, interval: int = 1) -> None:
        self.bot_instance: AizyBot = bot_class()
        self.duration: int = duration
        self.interval: int = interval
        self.trade_log: List[Dict[str, Union[str, float]]] = []  # To store trade data for performance summary
        self.profit_loss: float = 0.0  # Track total profit/loss

    async def run(self) -> None:
        await self.bot_instance.bot_setup("MockExchange", "MockStream")  # Initial setup
        await self.simulate_market_data()
        
        # Ensure all active trades are closed at the end of the simulation
        await self.close_all_trades()
        
        # Display performance summary
        self.display_summary()

        # Alerts based on active trades
        self.check_for_active_trade_alerts()

    async def simulate_market_data(self) -> None:
        timestamp: datetime = datetime.now()
        for _ in range(self.duration):
            open_price: float = random.uniform(1000, 2000)
            close_price: float = open_price * random.uniform(0.95, 1.05)
            high_price: float = max(open_price, close_price) * random.uniform(1.0, 1.02)
            low_price: float = min(open_price, close_price) * random.uniform(0.98, 1.0)
            volume: float = random.uniform(10, 100)

            candle_data = CandleData(
                timestamp=timestamp.isoformat(),
                open=open_price,
                high=high_price,
                low=low_price,
                close=close_price,
                volume=volume
            )

            await self.bot_instance.bot_action(candle_data)
            timestamp += timedelta(minutes=self.interval)

    async def close_all_trades(self) -> None:
        active_trades: List[Order] = self.bot_instance.list_active_trades()
        final_price: float = active_trades[-1].price if active_trades else 0  # Use last known price as exit price
        for trade in active_trades:
            await self.bot_instance.close_trade(trade)
            self.record_trade(trade, final_price)  # Log each closed trade with its exit price

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
        print("Recorded trade:", trade_data)  # This should now print each recorded trade

    def display_summary(self) -> None:
        """Display a summary of trade performance."""
        print("=== Trade Performance Summary ===")
        print(f"Total Trades: {len(self.trade_log)}")
        print(f"Total Profit/Loss: {self.profit_loss:.2f}")
        print("Trades:")
        for trade in self.trade_log:
            print(trade)

    def check_for_active_trade_alerts(self) -> None:
        active_trades: List[Order] = self.bot_instance.list_active_trades()
        total_trades_opened: int = len(self.trade_log) + len(active_trades)  # Sum of closed and active trades

        if active_trades:
            print("\n[ALERT] There are still active trades remaining at the end of the test.")
            print(f"Active Trades Count: {len(active_trades)}")

        if len(active_trades) == total_trades_opened:
            print("\n[ALERT] The bot did not close any trades during the test.")
            print("This may indicate an issue with trade-closing logic.")
            print(f"Active Trades Count: {len(active_trades)}")

    @classmethod
    async def test(cls, bot_class: Type[AizyBot], duration: int = 60, interval: int = 1) -> None:
        engine = cls(bot_class, duration, interval)
        await engine.run()
