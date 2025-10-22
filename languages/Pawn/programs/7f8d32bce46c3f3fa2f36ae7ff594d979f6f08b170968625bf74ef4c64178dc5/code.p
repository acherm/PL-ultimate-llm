/* Simple calculator, using the rational number support library
 * (c) Copyright 1998-2011, ITB CompuPhase
 * This file is provided as is (no warranties).
 */

#include <rational>
#include <string>

main()
{
    new buf{100}
    new Rational: a, Rational: b, Rational: result
    new op{2}

    print "Simple calculator\n"
    print "Supported operators: + - * /\n"
    print "Enter expressions like: 3.5 + 2.25\n"
    print "Type 'quit' to exit\n\n"

    for ( ;; )
    {
        print "> "
        getstring buf, sizeof buf
        if (strcmp(buf, "quit") == 0)
            break

        new pos = 0
        new len = strlen(buf)

        /* skip leading whitespace */
        while (pos < len && buf{pos} <= ' ')
            pos++

        /* get first number */
        new start = pos
        while (pos < len && buf{pos} != ' ' && buf{pos} != '\t')
            pos++
        new num1{20}
        strmid(num1, buf, start, pos, sizeof num1)
        a = rationalstr(num1)

        /* skip whitespace */
        while (pos < len && buf{pos} <= ' ')
            pos++

        /* get operator */
        if (pos < len)
            op{0} = buf{pos++}
        else
            op{0} = 0
        op{1} = 0

        /* skip whitespace */
        while (pos < len && buf{pos} <= ' ')
            pos++

        /* get second number */
        start = pos
        while (pos < len && buf{pos} > ' ')
            pos++
        new num2{20}
        strmid(num2, buf, start, pos, sizeof num2)
        b = rationalstr(num2)

        /* perform operation */
        switch (op{0})
        {
            case '+':
                result = a + b
            case '-':
                result = a - b
            case '*':
                result = a * b
            case '/':
            {
                if (b == Rational: 0)
                {
                    print "Error: Division by zero\n"
                    continue
                }
                result = a / b
            }
            default:
            {
                print "Error: Unknown operator\n"
                continue
            }
        }

        /* display result */
        printf "Result: %r\n", result
    }

    print "Goodbye!\n"
}