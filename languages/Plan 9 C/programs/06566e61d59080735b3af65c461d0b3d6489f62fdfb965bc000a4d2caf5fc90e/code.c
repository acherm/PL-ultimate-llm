#include <u.h>
#include <libc.h>

void
main(void)
{
	int i, a, b, t;
	a = 0;
	b = 1;
	for(i = 0; i < 10; i++){
		print("%d\n", a);
		t = a + b;
		a = b;
		b = t;
	}
	exits(nil);
}
