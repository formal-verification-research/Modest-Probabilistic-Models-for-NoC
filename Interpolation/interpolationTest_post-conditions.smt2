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
(declare-fun a0val2 () U)
(declare-fun a1val2 () U)
(declare-fun a2val2 () U)
(declare-fun a3val2 () U)
(declare-fun a0id0 () U)
(declare-fun a2id0 () U)
(declare-fun a1id0 () U)
(declare-fun a3id0 () U)
(declare-fun a0id1 () U)
(declare-fun a1id1 () U)
(declare-fun a2id1 () U)
(declare-fun a3id1 () U)
(declare-fun a0id2 () U)
(declare-fun a1id2 () U)
(declare-fun a2id2 () U)
(declare-fun a3id2 () U)

(declare-fun TU1 () Int)
(declare-fun TU2 () Int)

;;Inherit properties of the model --------------------------------------
(define-fun P1 () Bool (not (= a0id0 a1id0)))
(define-fun P2 () Bool (not (= a0id0 a2id0)))
(define-fun P3 () Bool (not (= a0id0 a3id0)))
(define-fun P4 () Bool (not (= a0id1 a1id1)))
(define-fun P5 () Bool (not (= a0id1 a2id1)))
(define-fun P6 () Bool (not (= a0id1 a3id1)))

;;Clock cycle t=0 -------------------------------------------------------
(define-fun C0_1 () Bool (= a0val0 a1val0))
(define-fun C0_2 () Bool (not(= a0val0 a2val0)))
(define-fun C0_3 () Bool (= a2val0 a3val0))
(define-fun C0_4 () Bool (= a0val0 a2id0))
(define-fun C0_5 () Bool (= a2val0 a0id0))

;;Clock cycle t=1 -------------------------------------------------------
(define-fun C1_1 () Bool (= a0val1 a1val0))
(define-fun C1_2 () Bool (= a1val1 a3val0))
(define-fun C1_3 () Bool (not(= a2val1 a2id1)))
(define-fun C1_4 () Bool (not(= a3val1 a3id1)))

(define-fun C1_5 () Bool (= a0id1 a1id0))
(define-fun C1_6 () Bool (= a1id1 a3id0))
(define-fun C1_7 () Bool (= a2id1 a0id0))
(define-fun C1_8 () Bool (= a3id1 a2id0))

(define-fun C1_TU () Bool (= TU1 2))

;;Clock cycle t=2 --------------------------------------------------------
(define-fun C2_TU0 () Bool (=> (or (and (= a2val1 a0id1) (= a3val1 a1id1)) (and (= a2val1 a1id1) (= a3val1 a0id1))) (= TU2 0)))

(define-fun C2_TU1 () Bool 
	(=> 
		(or 
			(or
				(or (and (= a2val1 a3id1) (= a3val1 a0id1)) (and (= a2val1 a3id1) (= a3val1 a1id1))) 
				(or (and (= a2val1 a0id1) (= a3val1 a2id1)) (and (= a2val1 a1id1) (= a3val1 a2id1)))
			)
			(or (and (= a2val1 a0id1) (= a3val1 a0id1)) (and (= a2val1 a1id1) (= a3val1 a1id1)))
		) 
		(= TU2 1)
	)
)

(define-fun C2_TU2 () Bool 
	(and	
		(=> (and (= a2val1 a3id1) (= a3val1 a2id1)) (= TU2 2))
		(=> (= TU2 2) (and (= a2val1 a3id1) (= a3val1 a2id1)))
	)
)

(define-fun C2_a02 () Bool 
	(and
		(=> (= a2val1 a3id1) (and (= a0val2 a2val1) (= a0id2 a2id1))) 
		(=> (and (= a0val2 a2val1) (= a0id2 a2id1)) (= a2val1 a3id1)) 
	)
)

(define-fun C2_a03 () Bool 
	(=> 	 
		(or
			(or (and (= a2val1 a0id1) (= a3val1 a2id1)) (and (= a2val1 a1id1) (= a3val1 a2id1))) 
			(or (and (= a2val1 a0id1) (= a3val1 a0id1)) (and (= a2val1 a1id1) (= a3val1 a1id1)))
		)
		(and (= a0val2 a3val1) (= a0id2 a3id1))
	)
)

(define-fun C2_a0N () Bool 
	(=> 	 
		(or (and (= a2val1 a0id1) (= a3val1 a1id1)) (and (= a2val1 a1id1) (= a3val1 a0id1))) 	
		(not (= a0val2 a0id2))
	)
)

(define-fun C2_a1N () Bool
	(=>
		(or 
			(or
				(or (and (= a2val1 a0id1) (= a3val1 a1id1)) (and (= a2val1 a1id1) (= a3val1 a0id1))) 
				(or (and (= a2val1 a3id1) (= a3val1 a0id1)) (and (= a2val1 a3id1) (= a3val1 a1id1)))
			)
			(or
				(or (and (= a2val1 a0id1) (= a3val1 a2id1)) (and (= a2val1 a1id1) (= a3val1 a2id1))) 
				(or (and (= a2val1 a0id1) (= a3val1 a0id1)) (and (= a2val1 a1id1) (= a3val1 a1id1)))
			)
		)
		(not (= a1val2 a1id2))
	)
)

(define-fun C2_a13 () Bool
	(=>
		(and (= a2val1 a3id1) (= a3val1 a2id1))
		(and (= a1val2 a3val1) (= a1id2 a3id1))
	)
)

(define-fun C2_a1id_0 () Bool
	(=>	
		(or 
			(or
				(or (and (= a2val1 a3id1) (= a3val1 a0id1)) (and (= a2val1 a3id1) (= a3val1 a1id1))) 
				(or (and (= a2val1 a0id1) (= a3val1 a2id1)) (and (= a2val1 a1id1) (= a3val1 a2id1)))
			)
			(or (and (= a2val1 a0id1) (= a3val1 a0id1)) (and (= a2val1 a1id1) (= a3val1 a1id1)))
		)
		(= a1id2 a0id1) 
	)
)

(define-fun C2_a1id_1 () Bool
	(=>
		(or (and (= a2val1 a0id1) (= a3val1 a1id1)) (and (= a2val1 a1id1) (= a3val1 a0id1)))
		(= a1id2 a1id1)
	)
)

(define-fun C2_a2N () Bool (not (= a2val2 a2id2)))

(define-fun C2_a2id_0 () Bool
	(=>
		(and (= a2val1 a3id1) (= a3val1 a2id1))
		(= a2id2 a0id1)
	)
)

(define-fun C2_a2id_1 () Bool
	(=>
		(or 
			(or
				(or (and (= a2val1 a3id1) (= a3val1 a0id1)) (and (= a2val1 a3id1) (= a3val1 a1id1))) 
				(or (and (= a2val1 a0id1) (= a3val1 a2id1)) (and (= a2val1 a1id1) (= a3val1 a2id1)))
			)
			(or (and (= a2val1 a0id1) (= a3val1 a0id1)) (and (= a2val1 a1id1) (= a3val1 a1id1)))
		)	
		(= a2id2 a1id1)
	)
)

(define-fun C2_a2id_2 () Bool
	(=>
		(or (and (= a2val1 a0id1) (= a3val1 a1id1)) (and (= a2val1 a1id1) (= a3val1 a0id1)))	
		(= a2id2 a2id1)
	)
)

(define-fun C2_a3N () Bool (not (= a3val2 a3id2)))

(define-fun C2_a3id_0 () Bool
	(=>
		(or (and (= a2val1 a3id1) (= a3val1 a0id1)) (and (= a2val1 a3id1) (= a3val1 a1id1)))
		(= a3id2 a0id1)
	)
)

(define-fun C2_a3id_1 () Bool
	(=>
		(or
			(or (and (= a2val1 a0id1) (= a3val1 a2id1)) (and (= a2val1 a1id1) (= a3val1 a2id1)))
			(and (= a2val1 a3id1) (= a3val1 a2id1))
		)
		(= a3id2 a1id1)
	)
)

(define-fun C2_a3id_2 () Bool
	(=>
		(or (and (= a2val1 a0id1) (= a3val1 a0id1)) (and (= a2val1 a1id1) (= a3val1 a1id1)))
		(= a3id2 a2id1)
	)
)

(define-fun C2_a3id_3 () Bool
	(=>
		(or (and (= a2val1 a0id1) (= a3val1 a1id1)) (and (= a2val1 a1id1) (= a3val1 a0id1)))
		(= a3id2 a3id1)
	)
)


;; Assertation (B) -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
(define-fun B () Bool (and (= TU2 2) (= a0val2 a1val2)))

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
(assert (! C0_5 :interpolation-group g11))


(assert (! C1_1 :interpolation-group g12))
(assert (! C1_2 :interpolation-group g13))
(assert (! C1_3 :interpolation-group g14))
(assert (! C1_4 :interpolation-group g15))

(assert (! C1_5 :interpolation-group g16))
(assert (! C1_6 :interpolation-group g17))
(assert (! C1_7 :interpolation-group g18))
(assert (! C1_8 :interpolation-group g19))

(assert (! C1_TU :interpolation-group g20))

(assert (! C2_TU0 :interpolation-group g21))
(assert (! C2_TU1 :interpolation-group g22))
(assert (! C2_TU2 :interpolation-group g23))

(assert (! C2_a02 :interpolation-group g24))
(assert (! C2_a03 :interpolation-group g25))
;;(assert (! C2_a0N :interpolation-group g26))

;;(assert (! C2_a1N :interpolation-group g27))
(assert (! C2_a13 :interpolation-group g28))
(assert (! C2_a1id_0 :interpolation-group g29))
(assert (! C2_a1id_1 :interpolation-group g30))

;;(assert (! C2_a2N :interpolation-group g31))
(assert (! C2_a2id_0 :interpolation-group g32))
(assert (! C2_a2id_1 :interpolation-group g33))
(assert (! C2_a2id_2 :interpolation-group g34))

;;(assert (! C2_a3N :interpolation-group g35))
(assert (! C2_a3id_0 :interpolation-group g36))
(assert (! C2_a3id_1 :interpolation-group g37))
(assert (! C2_a3id_2 :interpolation-group g38))
(assert (! C2_a3id_3 :interpolation-group g39))

(assert (! B :interpolation-group gb))

(check-sat)

;; compute an interpolant for the given partition: the argument to
;; get-interpolant is a list of groups forming the A-part of the interpolation
;; problem

(get-interpolant (g1 g2 g3 g4 g5 g6 g7 g8 g9 g10 g11 g12 g13 g14 g15 g16 g17 g18 g19 g20 g21 g22 g23 g24 g25 g28 g29 g30 g32 g33 g34 g36 g37 g38 g39))

(exit)
