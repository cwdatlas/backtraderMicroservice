from Errors.BacktradeInputErrors import BacktradeInputErrors


class TickerNotFoundError(BacktradeInputErrors):
    """
    TickerNotFoundError is raised when an algorithm of the same name is not found when prepping for trading
    Child of BacktradeInputErrors
    """
    pass