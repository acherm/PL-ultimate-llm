(define (eval expr)
  (cond ((number? expr) expr)
        ((symbol? expr) (lookup expr))
        ((list? expr)
         (let ((op (car expr))
               (args (cdr expr)))
           (case op
             ((+) (apply + (map eval args)))
             ((-) (apply - (map eval args)))
             ((*) (apply * (map eval args)))
             ((/) (apply / (map eval args)))
             (else (error "Unknown operator")))))))

(define (lookup sym)
  (if (assoc sym env)
      (cdr (assoc sym env))
      (error "Unbound variable")))

(define env '((x . 10) (y . 20)))

(eval '(+ x y))