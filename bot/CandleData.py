class CandleData:
    def __init__(self, timestamp: str, open: float, high: float, low: float, close: float, volume: float):
        self.timestamp = timestamp
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            timestamp=data["timestamp"],
            open=float(data["open"]),
            high=float(data["high"]),
            low=float(data["low"]),
            close=float(data["close"]),
            volume=float(data["volume"])
        )

    def __repr__(self):
        return (f"CandleData(timestamp={self.timestamp}, open={self.open}, high={self.high}, "
                f"low={self.low}, close={self.close}, volume={self.volume})")
