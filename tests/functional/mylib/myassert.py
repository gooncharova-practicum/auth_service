from __future__ import annotations


class Assert:
    def __init__(self, response):
        self.response = response
        self.response_code = response.status
        self.response_body = response.body

    def status_code(self, expected_code: int) -> Assert:
        assert self.response_code == expected_code
        return self

    def status_code_not_equal(self, code: int) -> Assert:
        assert self.response_code != code
        return self

    def body_is(self, expected_body) -> Assert:
        assert self.response_body == expected_body
        return self

    def body_len_is(self, expected_len: int) -> Assert:
        assert len(self.response_body) == expected_len
        return self
