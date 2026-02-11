on mouseUp
   put field "firstNumber" into num1
   put field "secondNumber" into num2
   put field "operator" into op
   
   switch op
      case "+"
         put num1 + num2 into result
         break
      case "-"
         put num1 - num2 into result
         break
      case "*"
         put num1 * num2 into result
         break
      case "/"
         if num2 = 0 then
            put "Error: Division by zero" into result
         else
            put num1 / num2 into result
         end if
         break
      default
         put "Invalid operator" into result
   end switch
   
   put result into field "result"
end mouseUp