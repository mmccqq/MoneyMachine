import statistics
def MA(data, period):
    if len(data) < period:
        return None
    ma = 0
    for i in data:
        ma += i
    ma /= period
    return ma


def BOLL(MA20, data, period=20, k=2):
    if len(data) != period:
        return None
    std = statistics.stdev(data)
    upper = MA20 + k * std
    lower = MA20 - k * std
    return (upper, lower)

def EMA(number, prev, period):
    k = 2 / (period + 1)
    ema = number * k + prev * (1 - k)
    return ema

def MACD(price, prev_short, prev_long, dif, prev_dif, short_period=12, long_period=26, signal_period=9):
    ema_short = EMA(price, prev_short, short_period)
    ema_long = EMA(price, prev_long, long_period)
    if ema_short is None or ema_long is None:
        return None
    dif = ema_short - ema_long
    dea = EMA(dif, prev_dif, signal_period)
    macd = (dif - dea) * 2
    return macd