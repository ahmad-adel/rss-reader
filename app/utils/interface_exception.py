class InterfaceException(Exception):
    def __init__(self, message):
        """Exception class initializer

        Args:
            message (str): Custom error message. Defaults to None.
        """
        super().__init__("")
        self.message = message
