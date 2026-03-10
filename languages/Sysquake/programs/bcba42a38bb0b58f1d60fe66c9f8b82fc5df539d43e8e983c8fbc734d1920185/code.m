% Sysquake LME: State-space system analysis
% Define a second-order system (double integrator with damping)
A = [0, 1; -2, -3];
B = [0; 1];
C = [1, 0];
D = 0;

% Compute eigenvalues of the system matrix
ev = eig(A);
fprintf('System eigenvalues: %.4f %+.4fi, %.4f %+.4fi\n', ...
        real(ev(1)), imag(ev(1)), real(ev(2)), imag(ev(2)));

% Check stability (all eigenvalues must have negative real part)
if all(real(ev) < 0)
    fprintf('System is stable.\n');
else
    fprintf('System is unstable.\n');
end

% Simulate step response using Euler integration
dt = 0.05;
t = 0:dt:2;
x = [0; 0];
y = zeros(1, length(t));
for k = 1:length(t)
    y(k) = C * x + D;
    x = x + dt * (A * x + B * 1);
end

fprintf('Step response at t=1s: %.4f\n', y(round(1/dt)+1));
fprintf('Step response at t=2s: %.4f\n', y(end));
