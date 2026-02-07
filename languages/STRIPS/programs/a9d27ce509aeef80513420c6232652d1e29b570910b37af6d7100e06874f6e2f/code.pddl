;;; Blocks World Planning Problem in STRIPS

(define (problem blocks-world-1)
  (:domain blocks)
  (:objects a b c table)
  (:init
    (on a table)
    (on b table)
    (on c a)
    (clear b)
    (clear c)
    (handempty))
  (:goal
    (and
      (on a b)
      (on b c))))

(define (domain blocks)
  (:requirements :strips)
  (:predicates
    (on ?x ?y)
    (clear ?x)
    (holding ?x)
    (handempty))

  (:action pickup
    :parameters (?ob)
    :precondition (and (clear ?ob) (on ?ob table) (handempty))
    :effect (and (holding ?ob) (not (on ?ob table)) (not (clear ?ob)) (not (handempty))))

  (:action putdown
    :parameters (?ob)
    :precondition (holding ?ob)
    :effect (and (on ?ob table) (clear ?ob) (handempty) (not (holding ?ob))))

  (:action stack
    :parameters (?ob ?underob)
    :precondition (and (holding ?ob) (clear ?underob))
    :effect (and (on ?ob ?underob) (clear ?ob) (handempty) (not (holding ?ob)) (not (clear ?underob))))

  (:action unstack
    :parameters (?ob ?underob)
    :precondition (and (on ?ob ?underob) (clear ?ob) (handempty))
    :effect (and (holding ?ob) (clear ?underob) (not (on ?ob ?underob)) (not (clear ?ob)) (not (handempty)))))
