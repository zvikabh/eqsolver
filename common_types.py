import dataclasses
import enum


class TokenType(enum.IntEnum):
    SIGN = enum.auto()      # '+' OR '-'
    EQUALITY = enum.auto()  # '='
    NEWLINE = enum.auto()   # '\n'
    NUMBER = enum.auto()    # integer constant literal
    VARNAME = enum.auto()   # single-letter variable name, e.g. 'x'


@dataclasses.dataclass(frozen=True)
class Token:
    type: TokenType
    value: str | int

    def __str__(self):
        return str(self.value)

