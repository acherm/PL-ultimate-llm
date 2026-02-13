FUNCTION_BLOCK FB_PID
VAR_INPUT
    fSetpoint : REAL;
    fActualValue : REAL;
    fKp : REAL := 1.0;
    fKi : REAL := 0.1;
    fKd : REAL := 0.01;
    fCycleTime : REAL;
END_VAR

VAR_OUTPUT
    fOut : REAL;
END_VAR

VAR
    fError : REAL;
    fErrorLast : REAL;
    fIntegral : REAL;
    fDerivative : REAL;
END_VAR

// Calculate error
fError := fSetpoint - fActualValue;

// Proportional term
fOut := fKp * fError;

// Integral term
fIntegral := fIntegral + (fKi * fError * fCycleTime);
fOut := fOut + fIntegral;

// Derivative term
fDerivative := fKd * (fError - fErrorLast) / fCycleTime;
fOut := fOut + fDerivative;

// Save error for next cycle
fErrorLast := fError;
