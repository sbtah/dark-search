class NoProxiesError(Exception):
    """Exception raised when queryset for proxies is empty."""
    def __init__(self, message: str = "No proxies found in database.") -> None:
        self.message = message
        super().__init__(self.message)
