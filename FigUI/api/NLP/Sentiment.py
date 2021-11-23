import enum

class FigSentiment(enum.Enum):
    TUP = 0
    JSON = 1


class FigSentimentEngine(enum.Enum):
    VADER = 1


class VADerAnalyzer:
    def __init__(self):
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
        self._backend = SentimentIntensityAnalyzer()

    def __call__(self, text: str):
        return self._backend.polarity_scores(text)


class FigSentimentDetector:
    def __init__(self, backend=FigSentimentEngine.VADER):
        if backend == FigSentimentEngine.VADER:
            self._backend = VADerAnalyzer()

    def __call__(self, text: str, dtype=""):
        return self._backend(text)