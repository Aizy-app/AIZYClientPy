from typing import Dict

class CandleData:
    """Represents candlestick data for a trading instrument.
    
    A candlestick represents price movement over a specific time period,
    including opening price, highest price, lowest price, closing price,
    and trading volume.
    
    Attributes:
        timestamp: Time period of the candlestick
        open: Opening price of the period
        high: Highest price reached during the period
        low: Lowest price reached during the period
        close: Closing price of the period
        volume: Trading volume during the period
    """
    
    def __init__(self, timestamp: str, open: float, high: float, low: float, close: float, volume: float) -> None:
        """Initialize a new candlestick data instance.
        
        Args:
            timestamp: Time period of the candlestick
            open: Opening price of the period
            high: Highest price reached during the period
            low: Lowest price reached during the period
            close: Closing price of the period
            volume: Trading volume during the period
        """
        self.timestamp: str = timestamp
        self.open: float = open
        self.high: float = high
        self.low: float = low
        self.close: float = close
        self.volume: float = volume

    @classmethod
    def from_json(cls, data: Dict[str, str]) -> 'CandleData':
        """Create a CandleData instance from JSON data.
        
        Args:
            data: Dictionary containing candlestick data with keys:
                 timestamp, open, high, low, close, volume
        
        Returns:
            A new CandleData instance initialized with the provided data
        """
        return cls(
            timestamp=data["timestamp"],
            open=float(data["open"]),
            high=float(data["high"]),
            low=float(data["low"]),
            close=float(data["close"]),
            volume=float(data["volume"])
        )

    def __repr__(self) -> str:
        """Return a string representation of the candlestick data.
        
        Returns:
            A formatted string containing all candlestick attributes
        """
        return (f"CandleData(timestamp={self.timestamp}, open={self.open}, high={self.high}, "
                f"low={self.low}, close={self.close}, volume={self.volume})")
