class LenOfValueError(Exception):
    """Exceptions for small or big values

    Attributes:
        value: name of value
        len: len for value
    """

    def __init__(self, param: str, len_of_value: str | int, big: bool = False) -> None:
        self.param = param
        self.len_of_value = len_of_value
        self.big = big
        text_for_len = "has at least"
        if big:
            text_for_len = "has less than"
        self.message = f"Ensure value of param '{param}' {text_for_len} {len_of_value} characters"
        super().__init__(self.message)
