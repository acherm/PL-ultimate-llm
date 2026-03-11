/* OpenRISC Assembly (OR1K) - Fibonacci Sequence */
/* Iteratively computes fib(10) = 55 */

	.section .text
	.global _start

_start:
	l.addi	r1, r0, 0	/* r1 = prev = fib(0) = 0 */
	l.addi	r2, r0, 1	/* r2 = curr = fib(1) = 1 */
	l.addi	r3, r0, 9	/* r3 = iteration count */

loop:
	l.add	r4, r1, r2	/* r4 = prev + curr */
	l.add	r1, r0, r2	/* prev = curr */
	l.add	r2, r0, r4	/* curr = new fib value */
	l.addi	r3, r3, -1	/* decrement counter */
	l.sfnei	r3, 0		/* SR[F] = (counter != 0) */
	l.bf	loop		/* loop if counter != 0 */
	l.nop			/* delay slot */

	/* r2 = fib(10) = 55 */
halt:
	l.j	halt		/* infinite loop */
	l.nop
