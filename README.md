# lisp-in-python
Lisp interpreter written in Python (2.7)

Follows [these requirements](http://pythonpracticeprojects.com/lisp.html)

With inspiration from [Peter Norvig](http://norvig.com/lispy.html)

Run REPL:

```
$ ./repl.sh
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
$ ./test.sh
....................
----------------------------------------------------------------------
Ran 20 tests in 0.002s

OK
```
