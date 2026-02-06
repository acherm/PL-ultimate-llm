# Factorial program in Ratfor
# Demonstrates structured programming in Ratfor

      program factorial
      integer n, result, i

      write(6,*) 'Enter a positive integer:'
      read(5,*) n

      if (n < 0) {
          write(6,*) 'Error: negative number'
          stop
      }

      result = 1
      for (i = 2; i <= n; i = i + 1) {
          result = result * i
      }

      write(6,*) 'Factorial of', n, 'is', result
      end
