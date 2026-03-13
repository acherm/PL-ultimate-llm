	ORG	$C000
	
* initialize stack to something so subroutines can be used (addresses are stored on stack automatically)
	LDS 	$D000 
	
* your main program here
	LDAA	#1 * Value of A register is now 1.
	JSR	ADD5TOA * Call the subroutine using JSR, jump to subroutine
	* Value of A register is now 6.  
	
DONE	BRA	DONE * end of program

* Subroutine definition:
* This subroutine adds 5 to the A register
ADD5TOA	* give it a label
	* do all your stuff in here
	ADDA	#5
	RTS	* return from subroutine, goes back to where you used JSR
	