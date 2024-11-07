from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Trade:
    trade_id: str
    pair: str
    position: str  # "long" or "short"
    entry_price: float
    exit_price: Optional[float] = None
    size: float
    leverage: float
    entry_time: datetime = field(default_factory=datetime.utcnow)
    exit_time: Optional[datetime] = None
    take_profit: Optional[float] = None
    stop_loss: Optional[float] = None
    roe: Optional[float] = None  # Return on Equity
    pf_gain: Optional[float] = None  # Profit/Loss in terms of gain percentage or value

    def calculate_roe(self) -> None:
        """Calculate return on equity (ROE) after trade closure."""
        if self.exit_price is not None:
            self.roe = ((self.exit_price - self.entry_price) / self.entry_price) * self.leverage
            self.pf_gain = (self.exit_price - self.entry_price) * self.size
