import unittest

from main import *
from builtins import *

class TestAll(unittest.TestCase):

    # constants shared between tests
    math_code = '(+ (* 4 10) 2)'
    math_eval = 42
    # @property because parsing fns have side effects
    # and this generates a deep copy every call
    @property
    def math_tokens(self): 
        return ['(', '+', '(', '*', '4', '10', ')', '2', ')']

    @property
    def math_token_tree(self):
        return ['+', ['*', '4', '10'], '2']

    @property
    def math_ast(self): 
        return [add, [mult, 4, 10], 2]

    # parse/eval/interpret tests

    def test_code_to_tokens(self):
        self.assertEqual(
            code_to_tokens(self.math_code),
            self.math_tokens
        )

    def test_tokens_to_token_tree(self):
        self.assertEqual(
            tokens_to_token_tree(self.math_tokens),
            self.math_token_tree
        )

    def test_token_tree_to_ast(self):
        self.assertEqual(
            token_tree_to_ast(self.math_token_tree),
            self.math_ast
        )

    def test_parse(self):
        self.assertEqual(
            parse(self.math_code),
            self.math_ast
        )

    def test_evaluate(self):
        self.assertEqual(
            evaluate(self.math_ast),
            self.math_eval
        )

    def test_interpret(self):
        self.assertEqual(
            interpret(self.math_code),
            self.math_eval
        )

    # test builtins

    def test_eq(self):
        self.assertTrue(interpret('(eq? red red)'))
        self.assertFalse(interpret('(eq? red blue)'))
        self.assertTrue(interpret('(eq? 3 3 3)'))
        self.assertFalse(interpret('(eq? 3 3 4)'))

    def test_if(self):
        self.assertEqual(
            interpret('(if (eq? 1 1) yes no)'),
            'yes'
        )
        self.assertEqual(
            interpret('(if (eq? 1 2) yes no)'),
            'no'
        )

    def test_cons(self):
        self.assertEqual(
            interpret('(cons 1 2 3)'),
            (1, 2, 3)
        )

    def test_car(self):
        self.assertEqual(
            interpret('(car (1 2 3))'),
            1
        )

    def test_cdr(self):
        self.assertEqual(
            interpret('(cdr (1 2 3))'),
            (2, 3)
        )

    def test_quote(self):
        # TODO
        pass

    def test_is_atom(self):
        # TODO
        pass

    def test_define(self):
        # TODO
        pass

    def test_lambda(self):
        # TODO
        pass

    def test_cond(self):
        # TODO
        pass

    # misc tests

    def test_nested_first_element(self):
        self.assertEqual(
            interpret('((if (true) + -) 3 5)'),
            8
        )
        # TODO make this throw error instead of hit max recursion depth
        # self.assertEqual(
            # interpret('((1 2 3))'),
            # (1, 2, 3)
        # )


if __name__ == '__main__':
    unittest.main()
