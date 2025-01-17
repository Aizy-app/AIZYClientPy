from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Trade:
    """Represents a trading position with its associated parameters and metrics.
    
    Attributes:
        trade_id: Unique identifier for the trade
        pair: Trading pair symbol (e.g., 'BTC/USD')
        position: Direction of the trade ('long' or 'short')
        entry_price: Price at which the trade was opened
        exit_price: Price at which the trade was closed (None if still open)
        size: Size/quantity of the trade
        leverage: Leverage multiplier used for the trade
        entry_time: UTC timestamp when the trade was opened
        exit_time: UTC timestamp when the trade was closed (None if still open)
        take_profit: Target price for taking profit (None if not set)
        stop_loss: Price at which to cut losses (None if not set)
        roe: Return on equity percentage after trade closure (None if still open)
        pf_gain: Actual profit/loss value (None if still open)
    """
    
    trade_id: str
    pair: str
    position: str  # "long" or "short"
    entry_price: float

    size: float
    leverage: float
    entry_time: datetime = field(default_factory=datetime.utcnow)
    exit_time: Optional[datetime] = None
    take_profit: Optional[float] = None
    stop_loss: Optional[float] = None
    roe: Optional[float] = None  # Return on Equity
    pf_gain: Optional[float] = None  # Profit/Loss in terms of gain percentage or value
    exit_price: Optional[float] = None

    def calculate_roe(self) -> None:
        """Calculate return on equity (ROE) and profit/loss after trade closure.
        
        Updates the roe and pf_gain attributes based on entry and exit prices.
        ROE is calculated as the percentage return multiplied by leverage.
        Profit/loss is calculated as the price difference multiplied by trade size.
        """
        if self.exit_price is not None:
            self.roe = ((self.exit_price - self.entry_price) / self.entry_price) * self.leverage
            self.pf_gain = (self.exit_price - self.entry_price) * self.size
