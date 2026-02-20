import unittest

import lexer


class LexerTest(unittest.TestCase):
    def test_lexer(self):
        token_strs = [str(tok) for tok in lexer.lexer("3a = 60b + 25\n b = b")]
        self.assertEqual(token_strs, ['3', 'a', '=', '60', 'b', '+', '25', '\n', 'b', '=', 'b'])

    def test_lexer_syntax_error(self):
        with self.assertRaisesRegex(SyntaxError, 'Invalid character "/"'):
            list(lexer.lexer("3/2"))


if __name__ == '__main__':
  unittest.main()
