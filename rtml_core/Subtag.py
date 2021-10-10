#!/usr/bin/env python3


class subtag:
    def __init__(self, subtag_name, subtag_value, subtag_start, subtag_end):
        self.subtag_name = subtag_name
        self.subtag_value = subtag_value
        self.subtag_start = subtag_start
        self.subtag_end = subtag_end

    def __eq__(self, other):
        if isinstance(other, subtag):
            if (
                other.subtag_name == self.subtag_name
                and other.subtag_value == self.subtag_value
            ):
                return True

        return False

    @property
    def asdict(self):
        return {
            "subtag_name": self.subtag_name,
            "subtag_value": self.subtag_value,
            "subtag_start": self.subtag_start,
            "subtag_end": self.subtag_end,
        }
