import unittest

from repl import (
    g_env,
    code_to_tokens,
    tokens_to_ast,
    parse,
    evaluate,
    serialize,
    interpret
)

from env import builtin_map

class TestAll(unittest.TestCase):

    # constants shared between tests
    math_code = '(+ (* 4 10) 2)'
    math_eval = 42
    math_eval_str = str(math_eval)
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
        return ['+', ['*', 4, 10], 2]

    # parse/eval/interpret tests

    def test_code_to_tokens(self):
        self.assertEqual(
            code_to_tokens(self.math_code),
            self.math_tokens
        )

    def test_tokens_to_ast(self):
        self.assertEqual(
            tokens_to_ast(self.math_tokens),
            # self.math_token_tree
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

    def test_serialize(self):
        self.assertEqual(
            serialize(['+', 1, 'a']),
            '(+ 1 a)'
        )

    def test_interpret(self):
        self.assertEqual(
            interpret(self.math_code),
            self.math_eval
        )
        self.assertEqual(
            interpret(self.math_code, lisp_output=True),
            self.math_eval_str
        )

    # test builtins

    def test_eq(self):
        self.assertTrue(interpret('(equal? red red)'))
        self.assertFalse(interpret('(equal? red blue)'))
        self.assertTrue(interpret('(equal? 3 3 3)'))
        self.assertFalse(interpret('(equal? 3 3 4)'))

    def test_if(self):
        self.assertEqual(
            interpret('(if (equal? 1 1) yes no)'),
            'yes'
        )
        self.assertEqual(
            interpret('(if (equal? 1 2) yes no)'),
            'no'
        )
        self.assertTrue('(if true true false)')
        self.assertTrue('(if false false true)')
        self.assertTrue('(if true true)')

    def test_list(self):
        self.assertEqual(
            interpret("(list 1 2 3)"),
            [1, 2, 3]
        )

    def test_cons(self):
        self.assertEqual(
            interpret("(cons 1 '(2 3))"),
            [1, 2, 3]
        )

    def test_car(self):
        self.assertEqual(
            interpret('(car (1 2 3))'),
            1
        )

    def test_cdr(self):
        self.assertEqual(
            interpret('(cdr (1 2 3))'),
            [2, 3]
        )

    def test_quote(self):
        self.assertEqual(
            interpret('(quote (+ 1 2))'),
            ['+', 1, 2]
        )
        self.assertEqual(
            interpret("(cdr '(+ 1 2))"),
            [1, 2]
        )

    def test_is_atom(self):
        self.assertTrue(interpret('(atom? nil)'))
        self.assertTrue(interpret('(atom? 1)'))
        self.assertTrue(interpret('(atom? a)'))
        self.assertFalse(interpret('(atom? (1 1 1))'))
        self.assertFalse(interpret('(atom? (quote (+ 1 1)))'))

    def test_do(self):
        self.assertEqual(
            interpret('(do (+ 1 1) (+ 1 2) (+ 1 3))'),
            4
        )

    def test_define(self):
        self.assertEqual(
            interpret('(do (define a (* 2 2)) (+ a a))'),
            8
        )

    def test_lambda(self):
        self.assertEqual(
            interpret('((lambda x (+ x x)) 1)'),
            2
        )
        self.assertEqual(
            interpret('((lambda (y) (+ y y)) 1)'),
            2
        )
        self.assertEqual(
            interpret('((lambda (fn x) (fn x x x)) + 2)'),
            6
        )

    def test_do_define_lambda(self):
        self.assertEqual(
            interpret(
            ''' (do (define x 3) 
                    (define twice
                        (lambda x (* x 2)))
                    (twice x))
            '''),
            6
        )

    def test_cond(self):
        self.assertEqual(
            interpret(
            ''' (cond ((equal? 1 2) no) 
                      (true      yes)))
            '''),
            'yes'
        )
        self.assertEqual(
            interpret(
            ''' (cond ((equal? 1 2)         no)
                      ((equal? 1 1)         yes)
                      ((equal? false true)  nono))
            '''),
            'yes'
        )

    def test_println(self):
        #TODO capture stdout?
        pass

    # misc tests

    def test_nested_first_element(self):
        self.assertEqual(
            interpret('((if true + -) 3 5)'),
            8
        )
    def test_nested(self):
        # TODO make this throw error instead of hit max recursion depth
        self.assertEqual(
            interpret("'((1 2 3))"),
            [[1, 2, 3]]
        )

    def test_fib(self):
        self.assertEqual(
            interpret('''
            (do 
                (define fib
                    (lambda n 
                        (cond ((equal? 0 n) 1)
                              ((equal? 1 n) 1)
                              (else (+ (fib (- n 1)) (fib (- n 2)))))))
                (fib 4))
                '''),
            5
        )

    def test_scope(self):
        self.assertEqual(
            interpret('''
            (do (define x 5)
                (define incx
                    (lambda y (+ x y)))
                (define x 6)
                (incx 1)
            )
            '''),
            7
        )

    def test_string(self):
        self.assertEqual(
            interpret('(do (define x "hello world") x)'),
            'hello world'
        )

    def test_string_append(self):
        self.assertEqual(
            interpret('(string-append "hello" " " "world")'),
            'hello world'
        )

    def test_list_ref(self):
        self.assertEqual(
            interpret('(list-ref (1 2 3 4) 3)'),
            4
        )

    def test_count(self):
        self.assertEqual(
            interpret('''
            (count (lambda x (equal? x 4)) (3 4 4 5)))
            '''),
            2
        )

    def test_str_split(self):
        self.assertEqual(
            interpret('(string-split "a,b,c" ",")'),
            ['a','b','c']
        )
        self.assertEqual(
            interpret('(string-split "a,,c" ",")'),
            ['a','','c']
        )
        self.assertEqual(
            interpret('(string-split "ac" ",")'),
            ['ac']
        )
        self.assertEqual(
            interpret('''
            (string->number 
                (car (string-split 
                    (car (cdr (string-split "beehive(10)" "("))) ")")))
            '''),
            10
        )

    def test_str_to_num(self):
        self.assertEqual(
            interpret('(string->number "4")'),
            4
        )
        self.assertEqual(
            interpret('(string->number "4.1")'),
            4.1
        )

    def test_comments(self):
        self.assertEqual(
            interpret('''
            (1 2
                ;asdf asdf sd fafd
                3 4)
            '''),
            [1,2,3,4]
        )
        self.assertEqual(
            interpret('''
            (1 2 ;asdf asdf sd fafd
                3 4)
            '''),
            [1,2,3,4]
        )

    def test_length(self):
        self.assertEqual(
            interpret('''
                (length '(1 2 3))
            '''),
            3
        )
if __name__ == '__main__':
    unittest.main()
