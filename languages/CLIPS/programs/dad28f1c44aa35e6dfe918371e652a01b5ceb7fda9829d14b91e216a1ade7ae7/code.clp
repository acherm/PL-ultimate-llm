(defrule start
   =>
   (printout t "Is the animal a mammal? (yes/no)" crlf)
   (assert (mammal (read))))

(defrule mammal-yes
   (mammal yes)
   =>
   (printout t "Does it have stripes? (yes/no)" crlf)
   (assert (stripes (read))))

(defrule mammal-stripes-yes
   (mammal yes)
   (stripes yes)
   =>
   (printout t "The animal is a Tiger" crlf))

(defrule mammal-stripes-no
   (mammal yes)
   (stripes no)
   =>
   (printout t "Does it have a mane? (yes/no)" crlf)
   (assert (mane (read))))

(defrule mammal-mane-yes
   (mammal yes)
   (stripes no)
   (mane yes)
   =>
   (printout t "The animal is a Lion" crlf))