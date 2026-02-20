"""Parser for a set of linear equations.

Grammar:

Root       -> Eq (NEWLINE Root)?
Eq         -> Side '=' Side
Side       -> FirstTerm OtherTerms?
FirstTerm  -> Sign? ActualTerm
OtherTerms -> Sign ActualTerm
ActualTerm -> INTEGER? VARNAME | INTEGER
Sign       -> '+' | '-'
"""

import dataclasses
import enum
from typing import Iterator

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


def lexer(input: str) -> Iterator[Token]:
    pos = 0
    while pos < len(input):
        if input[pos] == '\n':
            yield Token(type=TokenType.NEWLINE, value=input[pos])
        elif input[pos].isspace():
            pass
        elif input[pos] == '=':
            yield Token(type=TokenType.EQUALITY, value=input[pos])
        elif input[pos] in ('+', '-'):
            yield Token(type=TokenType.SIGN, value=input[pos])
        elif input[pos].isalpha():
            yield Token(type=TokenType.VARNAME, value=input[pos])
        elif input[pos].isdigit():
            number_start = pos
            while pos+1 < len(input) and input[pos+1].isdigit():
                pos += 1
            yield Token(type=TokenType.NUMBER, value=int(input[number_start:pos+1]))
        else:
            raise SyntaxError(f'Invalid character "{input[pos]}" at position {pos}')
        pos += 1
