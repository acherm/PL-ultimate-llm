Module: vehicles

define class <vehicle> (<object>)
  slot serial-number :: <integer>,
    required-init-keyword: sn:;
  slot owner :: <string>,
    init-keyword: owner:,
    init-value: "Northern Motors";
end class <vehicle>;

define class <car> (<vehicle>)
end class <car>;

define class <truck> (<vehicle>)
  slot capacity :: <integer>,
    required-init-keyword: capacity:;
end class <truck>;

define method tax(v :: <vehicle>)
  => tax-in-dollars :: <float>;
  100.00;
end;

define method tax(c :: <car>)
  => tax-in-dollars :: <float>;
  50.00;
end method;

define method tax(t :: <truck>)
  => tax-in-dollars :: <float>;
  next-method() + t.capacity * 10.00;
end method;
