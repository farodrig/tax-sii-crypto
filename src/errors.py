from enums import Currency


class CurrencyError(ValueError):
    """Exception raised for errors in the currency conversion process."""

    def __init__(self, currency: Currency, message: str = "Unsupported currency"):
        self.currency = currency
        self.message = message
        super().__init__(self.message, self.currency)
