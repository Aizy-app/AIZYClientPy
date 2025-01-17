"""
Grid Trading Bot Example

This bot implements a grid trading strategy:
- Creates a grid of buy and sell orders at regular price intervals
- Automatically places new orders when existing orders are filled
- Aims to profit from price oscillations within a range
"""

from aizypy import AizyBot
from aizypy import CandleData
from aizypy import TestEngine
from typing import List, Dict, Optional
import logging

class GridTradingBot(AizyBot):
    def __init__(self,
                 grid_size: int = 10,
                 grid_spacing: float = 50.0,
                 position_size: float = 0.1,
                 *args, **kwargs) -> None:
        """Initialize the grid trading bot.
        
        Args:
            grid_size: Number of grid levels above and below the initial price
            grid_spacing: Price difference between grid levels
            position_size: Size of each order
            *args: Additional positional arguments for AizyBot
            **kwargs: Additional keyword arguments for AizyBot
        """
        super().__init__(*args, **kwargs)
        self.grid_size: int = grid_size
        self.grid_spacing: float = grid_spacing
        self.position_size: float = position_size
        self.grid_levels: Dict[float, str] = {}  # price -> order_type mapping
        self.active_orders: Dict[str, float] = {}  # order_id -> price mapping
        self.initial_price: Optional[float] = None
        self.logger.info(
            f"Initialized Grid Trading Bot (Grid Size: {grid_size}, "
            f"Spacing: {grid_spacing}, Position Size: {position_size})"
        )

    def setup_grid(self, current_price: float) -> None:
        """Set up the initial grid levels around the current price.
        
        Args:
            current_price: Current market price to center the grid around
        """
        self.initial_price = current_price
        
        # Create grid levels above current price
        for i in range(1, self.grid_size + 1):
            price = current_price + (i * self.grid_spacing)
            self.grid_levels[price] = "sell"
            
        # Create grid levels below current price
        for i in range(1, self.grid_size + 1):
            price = current_price - (i * self.grid_spacing)
            self.grid_levels[price] = "buy"
            
        self.logger.info(f"Grid setup complete with {len(self.grid_levels)} levels")

    async def place_grid_orders(self) -> None:
        """Place orders at all grid levels that don't have active orders."""
        for price, order_type in self.grid_levels.items():
            if price not in self.active_orders.values():
                self.logger.info(f"Placing {order_type} order at price level {price:.2f}")
                await self.place_order(
                    side=order_type,
                    amount=self.position_size,
                    price=price,
                    pair="BTC/USD",
                    order_type="limit"
                )

    async def handle_order_filled(self, order_id: str, price: float) -> None:
        """Handle filled orders by placing new orders on the opposite side.
        
        Args:
            order_id: ID of the filled order
            price: Price level of the filled order
        """
        if order_id in self.active_orders:
            filled_price = self.active_orders[order_id]
            original_type = self.grid_levels[filled_price]
            
            # Place a new order on the opposite side
            new_type = "buy" if original_type == "sell" else "sell"
            self.logger.info(f"Order filled at {price:.2f}, placing {new_type} order")
            
            await self.place_order(
                side=new_type,
                amount=self.position_size,
                price=price,
                pair="BTC/USD",
                order_type="limit"
            )
            
            del self.active_orders[order_id]

    async def bot_action(self, candle_data: CandleData) -> None:
        """Process new candle data and manage the grid trading strategy.
        
        Strategy:
        - Set up initial grid on first run
        - Monitor price movements
        - Place new orders when grid levels become empty
        - Handle filled orders by placing opposite orders
        
        Args:
            candle_data: Latest market candle data
        """
        current_price = candle_data.close
        
        # Initialize grid on first run
        if self.initial_price is None:
            self.logger.info(f"Initializing grid around price {current_price:.2f}")
            self.setup_grid(current_price)
            await self.place_grid_orders()
            return

        # Check for filled orders (simplified simulation)
        active_trades = self.list_active_trades()
        for trade in active_trades:
            if (trade.side == "buy" and current_price <= trade.price) or \
               (trade.side == "sell" and current_price >= trade.price):
                await self.handle_order_filled(trade.trade_id, trade.price)
                await self.close_trade(trade)

        # Ensure all grid levels have active orders
        await self.place_grid_orders()

async def main() -> None:
    """Run the grid trading bot with the test engine."""
    # Test parameters
    test_duration = 240   # 4 hours
    test_interval = 1     # 1 minute candles
    grid_size = 5        # 5 levels above and below
    grid_spacing = 100.0  # $100 between levels
    position_size = 0.1   # 0.1 BTC per trade

    print(f"Starting Grid Trading Bot test (Duration: {test_duration} minutes, "
          f"Interval: {test_interval} minute(s))")
    await TestEngine.test(
        lambda *args, **kwargs: GridTradingBot(
            grid_size, grid_spacing, position_size, *args, **kwargs
        ),
        duration=test_duration,
        interval=test_interval
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 