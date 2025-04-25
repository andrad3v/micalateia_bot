class ProgressBar:
    def __init__(self, length: int = 20, fill: str = "█", empty: str = "░") -> None:
        self.length = length
        self.fill = fill
        self.empty = empty

    def progress(self, value: int, total: int) -> str:
        progress = int(self.length * value / total)
        return f"{self.fill * progress}{self.empty * (self.length - progress)}"

    def __str__(self) -> str:
        return f"{self.fill * self.length}"

    def __repr__(self) -> str:
        return f"{self.fill * self.length}"