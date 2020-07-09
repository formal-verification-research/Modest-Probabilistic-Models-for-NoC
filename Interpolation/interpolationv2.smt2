;; activate interpolation
(set-option :produce-interpolants true)

;;Variables
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
(define-fun P4 () Bool (not (= a1id0 a2id0)))
(define-fun P5 () Bool (not (= a1id0 a3id0)))
(define-fun P6 () Bool (not (= a2id0 a3id0)))

;;Clock cycle t=0
(define-fun C0_1 () Bool (= a0val0 a2id0))
(define-fun C0_2 () Bool (= a1val0 a2id0))
(define-fun C0_3 () Bool (= a2val0 a0id0))
(define-fun C0_4 () Bool (= a3val0 a0id0))

;;Clock cycle t=1
(define-fun C1_1 () Bool (= a0val1 a1val0))
(define-fun C1_2 () Bool (= a1val1 a3val0))

(define-fun C1_3 () Bool (or (= a2val1 a0id1) (or (= a2val1 a1id1) (= a2val1 a3id1))))
(define-fun C1_4 () Bool (or (= a3val1 a0id1) (or (= a3val1 a1id1) (= a3val1 a2id1))))

;;(define-fun C1_3 () Bool (or (and (and (= a2val1 a0id1) (not(= a2val1 a1id1))) (and (not(= a2val1 a2id1)) (not(= a2val1 a3id1)))) (or (and (and (not(= a2val1 a0id1)) (= a2val1 a1id1)) (and (not(= a2val1 a2id1)) (not(= a2val1 a3id1)))) (and (and (not(= a2val1 a0id1)) (not(= a2val1 a1id1))) (and (not(= a2val1 a2id1)) (= a2val1 a3id1))))))
;;(define-fun C1_4 () Bool (or(and (and (= a3val1 a0id1) (not(= a3val1 a1id1))) (and (not(= a3val1 a2id1)) (not(= a3val1 a3id1)))) (or (and (and (not(= a3val1 a0id1)) (= a3val1 a1id1)) (and (not(= a3val1 a2id1)) (not(= a3val1 a3id1)))) (and (and (not(= a3val1 a0id1)) (not(= a3val1 a1id1))) (and (= a3val1 a2id1) (not(= a3val1 a3id1)))))))

(define-fun C1_5 () Bool (= a0id1 a1id0))
(define-fun C1_6 () Bool (= a1id1 a3id0))
(define-fun C1_7 () Bool (= a2id1 a0id0))
(define-fun C1_8 () Bool (= a3id1 a2id0))


;; Assertation (B)
(define-fun B () Bool 
	(and 
		(or
			(and (and (= a0val0 a2id0) (= a1val0 a2id0)) (and (= a2val0 a0id0) (= a3val0 a0id0)))
			(or
				(and (and (= a0val0 a2id0) (= a1val0 a2id0)) (and (= a2val0 a1id0) (= a3val0 a1id0)))
				(or
					(and (and (= a0val0 a3id0) (= a1val0 a3id0)) (and (= a2val0 a0id0) (= a3val0 a0id0)))
					(or
						(and (and (= a0val0 a3id0) (= a1val0 a3id0)) (and (= a2val0 a1id0) (= a3val0 a1id0)))
						(or	
							(and (and (= a0val0 a1id0) (= a1val0 a0id0)) (and (= a2val0 a1id0) (= a3val0 a0id0)))
							(or
								(and (and (= a0val0 a1id0) (= a1val0 a2id0)) (and (= a2val0 a1id0) (= a3val0 a2id0)))
								(or
									(and (and (= a0val0 a3id0) (= a1val0 a0id0)) (and (= a2val0 a3id0) (= a3val0 a0id0)))
									(or
										(and (and (= a0val0 a3id0) (= a1val0 a2id0)) (and (= a2val0 a3id0) (= a3val0 a2id0)))
										(or
											(and (and (= a0val0 a1id0) (= a1val0 a0id0)) (and (= a2val0 a0id0) (= a3val0 a1id0)))
											(or
												(and (and (= a0val0 a1id0) (= a1val0 a3id0)) (and (= a2val0 a3id0) (= a3val0 a1id0)))
												(or
													(and (and (= a0val0 a2id0) (= a1val0 a0id0)) (and (= a2val0 a0id0) (= a3val0 a2id0)))
													(and (and (= a0val0 a2id0) (= a1val0 a3id0)) (and (= a2val0 a3id0) (= a3val0 a2id0)))
												)
											)
										)
									)
								)
							)
						)
					)
				)
			)
		)
		(or
			(or
				(and (and (= a1val1 a0id1) (= a2val1 a0id1)) (= a3val1 a0id1))
				(and (and (= a0val1 a1id1) (= a2val1 a1id1)) (= a3val1 a1id1))
			)
			(or
				(and (and (= a0val1 a2id1) (= a1val1 a2id1)) (= a3val1 a2id1))
				(and (and (= a0val1 a3id1) (= a1val1 a3id1)) (= a2val1 a3id1))
			)
		)
	)	
)
;; use annotation :interpolation-group to partition the input problem into
;; several groups
(assert (! P1 :interpolation-group gp1))
(assert (! P2 :interpolation-group gp2))
(assert (! P3 :interpolation-group gp3))
(assert (! P4 :interpolation-group gp4))
(assert (! P5 :interpolation-group gp5))
(assert (! P6 :interpolation-group gp6))

(assert (! C0_1 :interpolation-group g0_1))
(assert (! C0_2 :interpolation-group g0_2))
(assert (! C0_3 :interpolation-group g0_3))
(assert (! C0_4 :interpolation-group g0_4))

(assert (! C1_1 :interpolation-group g1_1))
(assert (! C1_2 :interpolation-group g1_2))
(assert (! C1_3 :interpolation-group g1_3))
(assert (! C1_4 :interpolation-group g1_4))

(assert (! C1_5 :interpolation-group g1_5))
(assert (! C1_6 :interpolation-group g1_6))
(assert (! C1_7 :interpolation-group g1_7))
(assert (! C1_8 :interpolation-group g1_8))

(assert (! B :interpolation-group gb))

(check-sat)

;; compute an interpolant for the given partition: the argument to
;; get-interpolant is a list of groups forming the A-part of the interpolation
;; problem

(get-interpolant (gp1 gp2 gp3 gp4 gp5 gp6 g0_1 g0_2 g0_3 g0_4 g1_1 g1_2 g1_3 g1_4 g1_5 g1_6 g1_7 g1_8))

(exit)
