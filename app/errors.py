class RetryingError(Exception):
    pass


class NoScriptError(RetryingError):
    def __init__(self) -> None:
        super().__init__("no script")


class NoDataError(RetryingError):
    def __init__(self) -> None:
        super().__init__("no data")


class ContentFetchError(RetryingError):
    def __init__(self) -> None:
        super().__init__("error fetching content")


class DifferentPageError(RetryingError):
    def __init__(self) -> None:
        super().__init__("tiktok_id is different from page_id")


class SignTokError(RetryingError):
    def __init__(self) -> None:
        super().__init__("SignTok error")
