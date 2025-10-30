model RCCircuit "A simple RC circuit"
  // The model parameters
  parameter Modelica.SIunits.Capacitance C = 1e-3 "Capacitance";
  parameter Modelica.SIunits.Resistance R = 1 "Resistance";
  parameter Modelica.SIunits.Voltage V = 10 "Voltage of step";

  // The model components
  Modelica.Electrical.Analog.Basic.Ground ground;
  Modelica.Electrical.Analog.Basic.Resistor resistor(R=R);
  Modelica.Electrical.Analog.Basic.Capacitor capacitor(C=C);
  Modelica.Electrical.Analog.Sources.StepVoltage stepVoltage(V=V);

equation
  connect(stepVoltage.p, resistor.p);
  connect(resistor.n, capacitor.p);
  connect(capacitor.n, ground.p);
  connect(ground.p, stepVoltage.n);
end RCCircuit;