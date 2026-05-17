(define (caar x) (car (car x)))
(define (cadr x) (car (cdr x)))
(define (cadar x) (car (cdr (car x))))
(define (cdar x) (cdr (car x)))
(define (cddr x) (cdr (cdr x)))

;; Problem 14
;; Returns a list of two-element lists
(define (enumerate s)
  ; BEGIN PROBLEM 14
  ;; go through list once and get index value pairs.
  (define (enum-iter lst i)
    (if (null? lst)
        '()
        (cons (list i (car lst)) (enum-iter (cdr lst) (+ i 1)))))
  (enum-iter s 0)
  ; END PROBLEM 14
)


;; Problem 15

;; Return the value for a key in a dictionary list
(define (get dict key)
  ; BEGIN PROBLEM 15
  (cond
    ((null? dict) #f)
    ((equal? key (car (car dict))) (cadr (car dict)))
    (else (get (cdr dict) key)))
  ; END PROBLEM 15
)

;; Return a dictionary list with a (key value) pair
(define (set dict key val)
  ; BEGIN PROBLEM 15
  (cond
    ((null? dict) (list (list key val)))
    ((equal? key (car (car dict))) (cons (list key val) (cdr dict)))
    (else (cons (car dict) (set (cdr dict) key val))))
  ; END PROBLEM 15
)

;; Problem 16

;; implement solution-code
(define (solution-code problem solution)
  ; BEGIN PROBLEM 16
  (define (replace expr)
    (cond
      ((pair? expr) (cons (replace (car expr)) (replace (cdr expr))))
      ((equal? expr '_____ ) (car solution))
      (else expr)))
  (replace problem)
  ; END PROBLEM 16
)

;; Merge two sorted lists according to a comparator
(define (merge ordered? list1 list2)
  ; BEGIN PROBLEM 15
  ;; Pick smaller head element and recurse on remaining lists.
  (cond
    ((null? list1) list2)
    ((null? list2) list1)
    ((ordered? (car list1) (car list2))
     (cons (car list1) (merge ordered? (cdr list1) list2)))
    (else
     (cons (car list2) (merge ordered? list1 (cdr list2)))))
  ; END PROBLEM 15
)
