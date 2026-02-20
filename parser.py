"""Parser for a set of linear equations.

Grammar:

Root       -> Eq NEWLINE Root?
Eq         -> Side '=' Side
Side       -> FirstTerm OtherTerms?
FirstTerm  -> Sign? ActualTerm
OtherTerms -> Sign ActualTerm OtherTerms?
ActualTerm -> INTEGER? VARNAME | INTEGER
Sign       -> '+' | '-'
"""
import dataclasses

import common_types as ct


def _apply_sign_to_term(term: ct.Term, sign: ct.Token) -> ct.Term:
    if sign == ct.PLUS_SIGN:
        return term
    else:
        return dataclasses.replace(term, coefficient=-term.coefficient)


class Parser:

    def __init__(self, tokens: list[ct.Token]):
        self.tokens = tokens
        self.cur_pos = 0

    @property
    def cur_token(self) -> ct.Token:
        if self.cur_pos == len(self.tokens):
            return ct.END_OF_FILE
        return self.tokens[self.cur_pos]

    @property
    def next_token(self) -> ct.Token:
        if self.cur_pos + 1 < len(self.tokens):
            return self.tokens[self.cur_pos + 1]
        else:
            return ct.END_OF_FILE

    @property
    def at_eof(self) -> bool:
        return self.cur_pos == len(self.tokens)

    def consume(self, token_type: ct.TokenType) -> ct.Token:
        if self.cur_token.type != token_type:
            raise SyntaxError(
                f"Unexpected token '{self.cur_token}' of type {self.cur_token.type.name} at position {self.cur_pos} (expected {token_type.name})")
        token = self.cur_token
        self.cur_pos += 1
        return token

    def parse_Root(self) -> list[ct.Equation]:
        eqs = [self.parse_Eq()]
        self.consume(ct.TokenType.NEWLINE)
        if self.at_eof:
            return eqs
        eqs.extend(self.parse_Root())
        return eqs

    def parse_Eq(self) -> ct.Equation:
        left_side = self.parse_Side()
        self.consume(ct.TokenType.EQUALITY)
        right_side = self.parse_Side()
        return ct.Equation(left_side=left_side, right_side=right_side)

    def parse_Side(self) -> ct.EqSide:
        terms = [self.parse_FirstTerm()]
        if self.cur_token.type == ct.TokenType.SIGN:
            terms.extend(self.parse_OtherTerms())
        return ct.EqSide(terms=terms)

    def parse_FirstTerm(self) -> ct.Term:
        if self.cur_token.type == ct.TokenType.SIGN:
            sign = self.consume(ct.TokenType.SIGN)
        else:
            sign = ct.PLUS_SIGN
        term = self.parse_ActualTerm()
        return _apply_sign_to_term(term, sign)

    def parse_OtherTerms(self) -> list[ct.Term]:
        sign = self.consume(ct.TokenType.SIGN)
        term = self.parse_ActualTerm()
        terms = [_apply_sign_to_term(term, sign)]
        if self.cur_token.type == ct.TokenType.SIGN:
            terms.extend(self.parse_OtherTerms())
        return terms

    def parse_ActualTerm(self) -> ct.Term:
        if self.cur_token.type == ct.TokenType.NUMBER:
            number = self.consume(ct.TokenType.NUMBER).value
        else:
            number = 1
        if self.cur_token.type == ct.TokenType.VARNAME:
            var_name = self.consume(ct.TokenType.VARNAME).value
        else:
            var_name = None
        return ct.Term(coefficient=number, variable_name=var_name)
