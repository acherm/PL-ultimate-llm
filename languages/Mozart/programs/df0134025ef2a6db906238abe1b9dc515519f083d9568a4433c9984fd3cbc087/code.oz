functor
import
   System
   Application
define
   fun {Fib N}
      if N < 2 then N
      else {Fib N-1} + {Fib N-2}
      end
   end
in
   {System.showInfo "Fibonacci of 10 is: "#{Fib 10}}
   {Application.exit 0}
end
