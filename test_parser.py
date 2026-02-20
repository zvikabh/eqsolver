import unittest

import lexer
import parser


class ParserTest(unittest.TestCase):

    def test_parser_single_equation(self):
        eq_str = 'a + 7b - c = -a - 1\n'
        tokens = list(lexer.lexer(eq_str))
        p = parser.Parser(tokens)
        eqs = p.parse_Root()
        self.assertEqual(1, len(eqs))
        eq = eqs[0]
        left_side = eq.left_side.terms
        right_side = eq.right_side.terms
        self.assertEqual(3, len(left_side))
        self.assertEqual(2, len(right_side))
        self.assertEqual('a', str(left_side[0]))
        self.assertEqual('7b', str(left_side[1]))
        self.assertEqual('-c', str(left_side[2]))
        self.assertEqual('-a', str(right_side[0]))
        self.assertEqual('-1', str(right_side[1]))

    def test_missing_newline(self):
        eq_str = 'a=b'
        tokens = list(lexer.lexer(eq_str))
        with self.assertRaisesRegex(SyntaxError, "Unexpected token 'EOF'.*expected NEWLINE"):
            parser.Parser(tokens).parse_Root()

    def test_invalid_term(self):
        eq_str = 'a=b7'
        tokens = list(lexer.lexer(eq_str))
        with self.assertRaisesRegex(SyntaxError, "Unexpected token '7'"):
            parser.Parser(tokens).parse_Root()


if __name__ == '__main__':
  unittest.main()
