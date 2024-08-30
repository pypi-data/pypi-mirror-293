import logging


class GMFYClientError(Exception):
    """Base class for exceptions with automatic logging."""

    def __init__(self, message: str):
        super().__init__(message)
        logging.error(message)
