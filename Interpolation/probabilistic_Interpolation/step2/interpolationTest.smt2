;; activate interpolation
(set-option :produce-interpolants true)


(declare-sort U 0)
(declare-fun a0val0 () U)
(declare-fun a1val0 () U)
(declare-fun a2val0 () U)
(declare-fun a3val0 () U)
(declare-fun a0val1 () U)
(declare-fun a1val1 () U)
(declare-fun a2val1 () U)
(declare-fun a3val1 () U)
(declare-fun a0id0 () U)
(declare-fun a2id0 () U)
(declare-fun a1id0 () U)
(declare-fun a3id0 () U)
(declare-fun a0id1 () U)
(declare-fun a1id1 () U)
(declare-fun a2id1 () U)
(declare-fun a3id1 () U)

;;Inherit properties of the model
(define-fun P1 () Bool (not (= a0id0 a1id0)))
(define-fun P2 () Bool (not (= a0id0 a2id0)))
(define-fun P3 () Bool (not (= a0id0 a3id0)))
(define-fun P4 () Bool (not (= a0id1 a1id1)))
(define-fun P5 () Bool (not (= a0id1 a2id1)))
(define-fun P6 () Bool (not (= a0id1 a3id1)))

;;Clock cycle t=0
(define-fun C0_1 () Bool (= a0val0 a3id0))
(define-fun C0_2 () Bool (= a1val0 a3id0))
(define-fun C0_3 () Bool (= a2val0 a0id0))
(define-fun C0_4 () Bool (= a3val0 a0id0))

;;Clock cycle t=1
(define-fun C1_1 () Bool (= a0val1 a1val0))
(define-fun C1_2 () Bool (= a1val1 a3val0))
(define-fun C1_3 () Bool (= a2val1 a0id1))) ;;Change this line for each iteration
(define-fun C1_4 () Bool (= a3val1 a0id1))) ;;Change this line for each iteration

(define-fun C1_5 () Bool (= a0id1 a1id0))
(define-fun C1_6 () Bool (= a1id1 a3id0))
(define-fun C1_7 () Bool (= a2id1 a0id0))
(define-fun C1_8 () Bool (= a3id1 a2id0))

;; Assertation (B)
(define-fun B () Bool 
(or
	(or
		(and(= a1val1 a0id1) (and(= a2val1 a0id1) (= a3val1 a0id1))) 
		(and(= a0val1 a1id1) (and(= a2val1 a1id1) (= a3val1 a1id1)))
	)
	(or
		(and(= a0val1 a2id1) (and(= a1val1 a2id1) (= a3val1 a2id1)))
		(and(= a0val1 a3id1) (and(= a1val1 a3id1) (= a2val1 a2id1)))
	)
)
)


;; use annotation :interpolation-group to partition the input problem into
;; several groups
(assert (! P1 :interpolation-group g1))
(assert (! P2 :interpolation-group g2))
(assert (! P3 :interpolation-group g3))
(assert (! P4 :interpolation-group g4))
(assert (! P5 :interpolation-group g5))
(assert (! P6 :interpolation-group g6))


(assert (! C0_1 :interpolation-group g7))
(assert (! C0_2 :interpolation-group g8))
(assert (! C0_3 :interpolation-group g9))
(assert (! C0_4 :interpolation-group g10))


(assert (! C1_1 :interpolation-group g11))
(assert (! C1_2 :interpolation-group g12))
(assert (! C1_3 :interpolation-group g13))
(assert (! C1_4 :interpolation-group g14))

(assert (! C1_5 :interpolation-group g15))
(assert (! C1_6 :interpolation-group g16))
(assert (! C1_7 :interpolation-group g17))
(assert (! C1_8 :interpolation-group g18))


(assert (! B :interpolation-group gb))

(check-sat)

;; compute an interpolant for the given partition: the argument to
;; get-interpolant is a list of groups forming the A-part of the interpolation
;; problem

(get-interpolant (g1 g2 g3 g4 g5 g6 g7 g8 g9 g10 g11 g12 g13 g14 g15 g16 g17 g18))

(exit)
