;; Implementation of Game of Life in Lisp

;; Notes
;; Extended language features used
;; (println datum)              -> Print datum with line break
;; (string-append str ...)      -> Concat strings
;; (list-ref list pos)          -> Returns the element of list at position pos
;; (count proc list)            -> Returns the number of elements in the list where procedure proc return true
;; (str-split str separator) -> Split str by separator into a list of sub-strings
;; (str->num str)         -> Convert string to number

;; Print board
(define print-board
  (lambda (board)
    (cond ((equal? board '()) (println ".........."))
          (else (do (println (car board)) (print-board (cdr board)))))))

;; Print board list
(define print-board-list
  (lambda (name boards)
    (cond ((equal? boards '()) (println (string-append "End of " name)))
          (else (do (print-board (car boards)) (print-board-list name (cdr boards)))))))

;; Get value from board by row and column
(define pos
  (lambda (board i j nrow ncol default)
    (cond ((< i 0) default)
          ((> i (- nrow 1)) default)
          ((< j 0) default)
          ((> j (- ncol 1)) default)
          (else (list-ref (list-ref board i) j)))))

;; Check if alive
(define alive? (lambda (cell) (equal? cell 1)))

;; Check if dead
(define dead? (lambda (cell) (equal? cell 0)))

;; Get 8-cells neighbor
(define neighbor
  (lambda (board i j nrow ncol)
    (list (pos board (- i 1) (- j 1) nrow ncol '())
          (pos board (- i 1) j nrow ncol '())
          (pos board (- i 1) (+ j 1) nrow ncol '())
          (pos board i (- j 1) nrow ncol '())
          (pos board i (+ j 1) nrow ncol '())
          (pos board (+ i 1) (- j 1) nrow ncol '())
          (pos board (+ i 1) j nrow ncol '())
          (pos board (+ i 1) (+ j 1) nrow ncol '()))))

;; Check if stay alive by position
(define stay-alive?
  (lambda (board i j nrow ncol)
    (or (equal? (count alive? (neighbor board i j nrow ncol)) 2)
        (equal? (count alive? (neighbor board i j nrow ncol)) 3))))

;; Get next cell state
(define next-cell-state
  (lambda (board i j nrow ncol)
    (cond
      ((alive? (pos board i j nrow ncol '()))
       (cond ((stay-alive? board i j nrow ncol) 1)
             (else 0)))
      (else
       (cond ((equal? (count alive? (neighbor board i j nrow ncol)) 3) 1)
             (else 0))))))

;; Get next column recursively given fixed row
(define next-cell
  (lambda (board i j nrow ncol)
    (cond ((> j (- ncol 1)) '())
          (else (cons (next-cell-state board i j nrow ncol)
                      (next-cell board i (+ j 1) nrow ncol))))))

;; Get next row recursively
(define next-row
  (lambda (board i j nrow ncol)
    (cond ((> i (- nrow 1)) '())
          (else (cons (next-cell board i j nrow ncol)
                      (next-row board (+ i 1) j nrow ncol))))))
;; Get next board
(define next-board
  (lambda (board nrow ncol)
    (next-row board 0 0 nrow ncol)))

;; Run a generation of life
(define game-of-life
  (lambda (board n nrow ncol)
    (cond ((equal? n 0) '())
          (else (cons (next-board board nrow ncol)
                      (game-of-life (next-board board nrow ncol) (- n 1) nrow ncol))))))

; testing
(define boards
  '(("block" ((0 0 0 0)
              (0 1 1 0)
              (0 1 1 0)
              (0 0 0 0)))
    ("blinker" ((0 0 0 0 0)
                (0 0 1 0 0)
                (0 0 1 0 0)
                (0 0 1 0 0)
                (0 0 0 0 0)))
    ("boat" ((0 0 0 0 0)
             (0 1 1 0 0)
             (0 1 0 1 0)
             (0 0 1 0 0)
             (0 0 0 0 0)))
    ("beacon" ((0 0 0 0 0 0)
               (0 1 1 0 0 0)
               (0 1 0 0 0 0)
               (0 0 0 0 1 0)
               (0 0 0 1 1 0)
               (0 0 0 0 0 0)))
    ("beehive" ((0 0 0 0 0 0)
                (0 0 1 1 0 0)
                (0 1 0 0 1 0)
                (0 0 1 1 0 0)
                (0 0 0 0 0 0)))))

(define find-board
  (lambda (boards name)
    (cond ((equal? boards '()) '())
          ((equal? name (list-ref (car boards) 0)) (list-ref (car boards) 1))
          (else (find-board (cdr boards) name)))))

(define run-on-board
  (lambda (board n)
    (do (print-board board)
        (cond ((equal? board '()) (println "Invalid board!"))
          (else (game-of-life board n (length board) (length (car board))))))))

(define run
  (lambda (expression)
    (print-board-list
         expression
         (run-on-board (find-board boards (car (str-split expression "(")))
                   (str->num (car (str-split (car (cdr (str-split expression "("))) ")")))))))

(run "beacon(10)")
