class DeckFMTException(Exception):
    """Base exception for the package. It allows to capture all exceptions raised by
    this package.
    """

    pass


class EncodeException(DeckFMTException):
    """Exception raised when failing to encode a decklist."""

    pass


class DecodeException(DeckFMTException):
    """Exception raised when failing to decode a decklist."""

    pass
