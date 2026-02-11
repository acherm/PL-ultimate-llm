prog: main.o utils.o
	cc -o prog main.o utils.o

main.o: main.c defs.h
	cc -c main.c

utils.o: utils.c defs.h
	cc -c utils.c

clean:
	rm -f prog *.o