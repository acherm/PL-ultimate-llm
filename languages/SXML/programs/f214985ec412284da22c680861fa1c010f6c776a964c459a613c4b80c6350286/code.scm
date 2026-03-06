;; SXML representation of an HTML document
;; Source: http://okmij.org/ftp/Scheme/SXML.html

(define doc
  '(*TOP*
    (html
      (head
        (title "My Document"))
      (body
        (p "Hello, World!")
        (p (@ (class "note")) "This is SXML")))))

;; SXML is just a Scheme data structure
;; XML: <html><head><title>My Document</title></head>
;;      <body><p>Hello, World!</p>
;;            <p class="note">This is SXML</p></body></html>

;; Accessing parts of the document using standard Scheme
(display (car doc))               ; *TOP*
(newline)
(display (cadr doc))              ; (html ...)
(newline)
(display (car (cadr doc)))        ; html
(newline)
