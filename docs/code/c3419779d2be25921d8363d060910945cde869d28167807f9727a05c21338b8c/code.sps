* Pearsons correlation.

* One-tailed test.
CORRELATIONS
	/VARIABLES=Exam Anxiety Exam Performance
	/PRINT=ONETAIL NOSIG
	/MISSING=PAIRWISE.

* Two-tailed test.
CORRELATIONS
	/VARIABLES=Exam Anxiety Exam Performance
	/PRINT=TWOTAIL SIG
	/MISSING=PAIRWISE.

* Bivariate Correlation with a control variable (Partial Correlation).

PARTIAL CORR
	/VARIABLES=Exam Performance Exam Anxiety BY Time Spent Revising
	/SIGNIFICANCE=TWOTAIL
	/MISSING=LISTWISE.

* Spearman's correlation.

NONPAR CORR
	/VARIABLES=liar creativity
	/PRINT=SPEARMAN TWOTAIL NOSIG
	/MISSING=PAIRWISE.


* Kendall's tau.

NONPAR CORR
	/VARIABLES=liar creativity
	/PRINT=KENDALL TWOTAIL NOSIG
	/MISSING=PAIRWISE.