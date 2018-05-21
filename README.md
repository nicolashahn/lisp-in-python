# lisp-in-python
Lisp interpreter written in Python (2.7)

With inspiration from [Peter Norvig](http://norvig.com/lispy.html)

Run REPL:

```
$ ./repl
lisp-in-python
> (define x 4)
nil
> (define sq (lambda (x) (* x x)))
nil
> (sq 3)
9
> x
4
```

To run tests:

```
$ ./test
....................
----------------------------------------------------------------------
Ran 20 tests in 0.002s

OK
```
