(do 
    (define fib
        (lambda n 
            (cond (eq? 0 n) 1
                  (eq? 1 n) 1
                  else (+ (fib (- n 1)) (fib (- n 2))))))
    (fib 4))
