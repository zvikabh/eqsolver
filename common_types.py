import dataclasses
import enum

import numpy as np


##### Lexer types

class TokenType(enum.IntEnum):
    SIGN = enum.auto()      # '+' OR '-'
    EQUALITY = enum.auto()  # '='
    NEWLINE = enum.auto()   # '\n'
    NUMBER = enum.auto()    # integer constant literal
    VARNAME = enum.auto()   # single-letter variable name, e.g. 'x'
    EOF = enum.auto()       # end of input


@dataclasses.dataclass(frozen=True)
class Token:
    type: TokenType
    value: str | int

    def __str__(self):
        return str(self.value)


END_OF_FILE = Token(type=TokenType.EOF, value='EOF')
PLUS_SIGN = Token(type=TokenType.SIGN, value='+')
MINUS_SIGN = Token(type=TokenType.SIGN, value='-')
EQUALITY = Token(type=TokenType.EQUALITY, value='=')


##### Parser types

@dataclasses.dataclass(frozen=True)
class Term:
    coefficient: int
    variable_name: str | None  # None indicates a free coefficient

    def __str__(self) -> str:
        if self.variable_name is None:
            return str(self.coefficient)
        if self.coefficient == 1:
            return self.variable_name
        if self.coefficient == -1:
            return '-' + self.variable_name
        return f'{self.coefficient}{self.variable_name}'


@dataclasses.dataclass(frozen=True)
class EqSide:
    terms: list[Term]


@dataclasses.dataclass(frozen=True)
class Equation:
    left_side: EqSide
    right_side: EqSide
