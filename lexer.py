from typing import Iterator

import common_types as ct


def lexer(input: str) -> Iterator[ct.Token]:
    pos = 0
    while pos < len(input):
        if input[pos] == '\n':
            yield ct.Token(type=ct.TokenType.NEWLINE, value=input[pos])
        elif input[pos].isspace():
            pass
        elif input[pos] == '=':
            yield ct.EQUALITY
        elif input[pos] == '+':
            yield ct.PLUS_SIGN
        elif input[pos] == '-':
            yield ct.MINUS_SIGN
        elif input[pos].isalpha():
            yield ct.Token(type=ct.TokenType.VARNAME, value=input[pos])
        elif input[pos].isdigit():
            number_start = pos
            while pos+1 < len(input) and input[pos+1].isdigit():
                pos += 1
            yield ct.Token(type=ct.TokenType.NUMBER, value=int(input[number_start:pos + 1]))
        else:
            raise SyntaxError(f'Invalid character "{input[pos]}" at position {pos}')
        pos += 1
