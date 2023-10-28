class TestReturn:
    def __init__(self, sma, ema, ending_value):
        self.sma = sma
        self.ema = ema
        self.ending_value = ending_value

    def set_sma(self, sma):
        self.sma = sma

    def set_ema(self, ema):
        self.ema = ema

    def set_ending_value(self, ending_value):
        self.ending_value = ending_value

    def to_dict(self):
        return {
            'sma': self.sma,
            'ema': self.ema,
            'ending_value': self.endingValue
        }
