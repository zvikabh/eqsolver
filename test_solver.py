import unittest

import numpy as np

import lexer
import parser
import solver


class TestSolver(unittest.TestCase):

    def test_canonicalize(self):
        eqs_str = '''\
             a + 7b = -a + 2
            -b +  5 = a
        '''
        eqs = parser.Parser(list(lexer.lexer(eqs_str))).parse_Root()
        canonical = solver.canonicalize(eqs)
        self.assertEqual(canonical.var_names, ['a', 'b'])
        np.testing.assert_array_equal(canonical.var_coefficients, [[2, 7], [-1, -1]])
        np.testing.assert_array_equal(canonical.free_coefficients, [[2], [-5]])


if __name__ == '__main__':
  unittest.main()
