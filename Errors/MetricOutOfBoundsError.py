from Errors.BacktradeInputErrors import BacktradeInputErrors


class MetricOutOfBoundsError(BacktradeInputErrors):
    """
    MetricOutOfBoundsError is raised when input metrics like sma and ema are out of bounds
    Child of BacktradeInputErrors
    """
    pass

