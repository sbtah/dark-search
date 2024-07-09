class NoProxiesError(Exception):
    """Exception raised when queryset for proxies is empty."""
    def __init__(self, message="No proxies found in database."):
        self.message = message
        super().__init__(self.message)