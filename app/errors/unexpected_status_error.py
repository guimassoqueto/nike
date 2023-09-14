class UnexpectedStatusError(Exception):
    def __init__(self, status_code: int, *args: object) -> None:
        super().__init__(*args)
        self.status_code = status_code

    def __str__(self) -> str:
        return f"UnexpectedStatusError: Unexpected status code ({self.status_code})"