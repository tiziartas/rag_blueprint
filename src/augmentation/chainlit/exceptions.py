class TraceNotFoundException(Exception):
    """Exception raised when a trace for a given message ID cannot be found.

    This exception is typically thrown when attempting to access or manipulate
    a trace using a message ID that doesn't exist in the system. It helps in
    handling missing trace scenarios gracefully.
    """

    def __init__(self, message_id: str) -> None:
        """Initialize the TraceNotFoundException with the specified message ID.

        This constructor creates a formatted error message that includes the
        missing message ID for better error reporting and debugging.

        Args:
            message_id: ID of the message whose trace was not found.
                        This ID is stored and used in the error message.
        """
        self.message_id = message_id
        self.message = f"Trace for message with id {message_id} not found"
        super().__init__(self.message)
