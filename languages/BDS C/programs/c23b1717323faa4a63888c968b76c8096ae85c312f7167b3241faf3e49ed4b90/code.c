/*
 * BDS C: word and character count (wc)
 * Classic CP/M utility in BDS C style (K&R, pre-ANSI)
 */
#include "bdscio.h"

main(argc, argv)
int argc;
char *argv[];
{
    int c, words, chars, lines;
    int inword;

    words = 0;
    chars = 0;
    lines = 0;
    inword = 0;

    while ((c = getchar()) != EOF) {
        chars++;
        if (c == '\n')
            lines++;
        if (c == ' ' || c == '\t' || c == '\n') {
            inword = 0;
        } else if (!inword) {
            inword = 1;
            words++;
        }
    }
    printf("lines: %d  words: %d  chars: %d\n", lines, words, chars);
}
