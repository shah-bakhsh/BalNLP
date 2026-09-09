class BalNLPError(Exception):
    """An error whose message is safe to show to an API client."""

    def __init__(self, code: str, message: str, status: int = 422):
        super().__init__(message)
        self.code, self.message, self.status = code, message, status
