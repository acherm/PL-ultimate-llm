functor
import
   System
define
   fun {Fib N}
      if N =< 1 then N
      else {Fib N-1} + {Fib N-2}
      end
   end
   for I in 0..10 do
      {System.showInfo {Fib I}}
   end
end
