unit Calculator;

interface

type
  TCalculator = class
  public
    function Add(A, B: Double): Double;
    function Subtract(A, B: Double): Double;
    function Multiply(A, B: Double): Double;
    function Divide(A, B: Double): Double;
  end;

implementation

function TCalculator.Add(A, B: Double): Double;
begin
  Result := A + B;
end;

function TCalculator.Subtract(A, B: Double): Double;
begin
  Result := A - B;
end;

function TCalculator.Multiply(A, B: Double): Double;
begin
  Result := A * B;
end;

function TCalculator.Divide(A, B: Double): Double;
begin
  if B = 0 then
    raise Exception.Create('Division by zero')
  else
    Result := A / B;
end;

end.
