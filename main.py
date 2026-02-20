import lexer
import parser
import solver


if __name__ == '__main__':
    print('Enter a system of linear equations, such as `4x-8y=-2x+1`, separated by newlines.')
    print('There must be an equal number of equations and variables.')
    print('Enter an empty line to end.')
    eqs = []
    while True:
        eq = input('> ')
        if not eq:
            break
        eqs.append(eq + '\n')
    tokens = list(lexer.lexer(''.join(eqs)))
    parsed_eqs = parser.Parser(tokens).parse_Root()
    eq_sys = solver.canonicalize(parsed_eqs)
    solution = solver.solve(eq_sys)

    print('The unique solution is:')
    for var_name, var_value in solution.items():
        print(f'{var_name} = {var_value}')
