// Simple ADMB example: estimate mean and variance of a normal distribution
DATA_SECTION
  init_int n
  init_vector y(1,n)

PARAMETER_SECTION
  init_number mu
  init_number log_sigma
  objective_function_value f

PROCEDURE_SECTION
  dvariable sigma = exp(log_sigma);
  f = 0;
  for (int i = 1; i <= n; i++)
  {
    f += 0.5 * log(2.0 * M_PI) + log_sigma + 0.5 * square((y(i) - mu) / sigma);
  }
