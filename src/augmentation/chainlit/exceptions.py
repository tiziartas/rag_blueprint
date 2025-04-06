class TraceNotFoundException(Exception):
    """Exception raised when a trace for a given message ID cannot be found.

    Attributes:
        message_id: ID of the message whose trace was not found.
        message: Explanation of the error.
    """

    def __init__(self, message_id: str) -> None:
        """Initialize the exception.

        Args:
            message_id: ID of the message whose trace was not found.
        """
        self.message_id = message_id
        self.message = f"Trace for message with id {message_id} not found"
        super().__init__(self.message)
