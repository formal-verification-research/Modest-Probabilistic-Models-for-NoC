;; activate interpolation
(set-option :produce-interpolants true)

;;Variables
(declare-fun a01 () Bool) ;; a[0].val = a[1].id
(declare-fun a02 () Bool) ;; a[0].val = a[2].id
(declare-fun a03 () Bool) ;; a[0].val = a[3].id

(declare-fun a10 () Bool) ;; a[1].val = a[0].id
(declare-fun a12 () Bool) ;; a[1].val = a[2].id
(declare-fun a13 () Bool) ;; a[1].val = a[3].id

(declare-fun a20 () Bool) ;; a[2].val = a[0].id
(declare-fun a21 () Bool) ;; a[2].val = a[1].id
(declare-fun a23 () Bool) ;; a[2].val = a[3].id

(declare-fun a30 () Bool) ;; a[3].val = a[0].id
(declare-fun a31 () Bool) ;; a[3].val = a[1].id
(declare-fun a32 () Bool) ;; a[3].val = a[2].id


(declare-fun a01_1 () Bool) ;; a[0].val = a[1].id
(declare-fun a02_1 () Bool) ;; a[0].val = a[2].id
(declare-fun a03_1 () Bool) ;; a[0].val = a[3].id

(declare-fun a10_1 () Bool) ;; a[1].val = a[0].id
(declare-fun a12_1 () Bool) ;; a[1].val = a[2].id
(declare-fun a13_1 () Bool) ;; a[1].val = a[3].id

(declare-fun a20_1 () Bool) ;; a[2].val = a[0].id
(declare-fun a21_1 () Bool) ;; a[2].val = a[1].id
(declare-fun a23_1 () Bool) ;; a[2].val = a[3].id

(declare-fun a30_1 () Bool) ;; a[3].val = a[0].id
(declare-fun a31_1 () Bool) ;; a[3].val = a[1].id
(declare-fun a32_1 () Bool) ;; a[3].val = a[2].id

;;Inherit properties of the model
;;The value in a buffer can only equal one id.
(define-fun P0_0 () Bool 

	(or 
		(or 
			(and (and a01 (not a02)) (not a03)) 
			(and (and (not a01) a02) (not a03))
		) 
		(and (and (not a01) (not a02)) a03)
	)
)
(define-fun P1_0 () Bool 
	(or 
		(or 
			(and (and a10 (not a12)) (not a13)) 
			(and (and (not a10) a12) (not a13))
		) 
		(and (and (not a10) (not a12)) a13)
	)
)
(define-fun P2_0 () Bool 
	(or 
		(or 
			(and (and a20 (not a21)) (not a23)) 
			(and (and (not a20) a21) (not a23))
		) 
		(and (and (not a20) (not a21)) a23)
	)
)
(define-fun P3_0 () Bool 
	(or 
		(or 
			(and (and a30 (not a31)) (not a32)) 
			(and (and (not a30) a31) (not a32))
		) 
		(and (and (not a30) (not a31)) a32)
	)
)

(define-fun P0_1 () Bool 
	(or 
		(or 
			(and (and a01_1 (not a02_1)) (not a03_1)) 
			(and (and (not a01_1) a02_1) (not a03_1))
		) 
		(and (and (not a01_1) (not a02_1)) a03_1)
	)
)
(define-fun P1_1 () Bool 
	(or 
		(or 
			(and (and a10_1 (not a12_1)) (not a13_1)) 
			(and (and (not a10_1) a12_1) (not a13_1))
		) 
		(and (and (not a10_1) (not a12_1)) a13_1)
	)
)
(define-fun P2_1 () Bool 
	(or 
		(or 
			(and (and a20_1 (not a21_1)) (not a23_1)) 
			(and (and (not a20_1) a21_1) (not a23_1))
		) 
		(and (and (not a20_1) (not a21_1)) a23_1)
	)
)
(define-fun P3_1 () Bool 
	(or 
		(or 
			(and (and a30_1 (not a31_1)) (not a32_1)) 
			(and (and (not a30_1) a31_1) (not a32_1))
		) 
		(and (and (not a30_1) (not a31_1)) a32_1)
	)
)

;;Clock cycle t=0
(define-fun C0_state2 () Bool 
	(and 
		(and a03 a13)
		(and a20 a30)
	)
)

;;Clock cycle t=1
(define-fun C1_1 () Bool
	(and (and a01_1 a12_1) (and a23_1 a32_1)) ;;Change this line for each iteration
)


;; Assertation (B)
(define-fun B () Bool 
	(and 
	;;state 2b
		(or
		(and (and a02 a12) (and a21 a31))
		(or
		(and (and a03 a13) (and a20 a30))
		(or
		(and (and a03 a13) (and a21 a31))
		(or
		(and (and a01 a12) (and a21 a32))
		(or	
		(and (and a03 a10) (and a23 a30))
		(or
		(and (and a03 a12) (and a23 a32))
		(or
		(and (and a01 a10) (and a20 a31))
		(or
		(and (and a01 a13) (and a23 a31))
		(or
		(and (and a02 a10) (and a20 a32))
		(or
		(and (and a01 a13) (and a23 a31))
		(and (and a02 a13) (and a23 a32))
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
		;;state 3a
		(or
			(or
				(and (and a10_1 a20_1) a30_1)
				(and (and a01_1 a21_1) a31_1)
			)
			(or
				(and (and a02_1 a12_1) a32_1)
				(and (and a03_1 a13_1) a23_1)
			)
		)	
	)
)
;; use annotation :interpolation-group to partition the input problem into
;; several groups
(assert (! P0_0 :interpolation-group g0_0))
(assert (! P1_0 :interpolation-group g1_0))
(assert (! P2_0 :interpolation-group g2_0))
(assert (! P3_0 :interpolation-group g3_0))

(assert (! P0_1 :interpolation-group g0_1))
(assert (! P1_1 :interpolation-group g1_1))
(assert (! P2_1 :interpolation-group g2_1))
(assert (! P3_1 :interpolation-group g3_1))

(assert (! C0_state2 :interpolation-group gc0_2))
(assert (! C1_1 :interpolation-group gc1))


(assert (! B :interpolation-group gb))

(check-sat)

;; compute an interpolant for the given partition: the argument to
;; get-interpolant is a list of groups forming the A-part of the interpolation
;; problem

(get-interpolant (g0_0 g1_0 g2_0 g3_0 g0_1 g1_1 g2_1 g3_1 gc0_2 gc1))

(exit)
