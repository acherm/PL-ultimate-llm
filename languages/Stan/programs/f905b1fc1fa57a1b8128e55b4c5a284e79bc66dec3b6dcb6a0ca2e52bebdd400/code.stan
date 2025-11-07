data {
  int<lower=0> J;  // number of schools
  real y[J];              // estimated treatment effects
  real<lower=0> sigma[J]; // standard errors of effect estimates
}
parameters {
  real mu;  // population mean
  real<lower=0> tau;  // population sd
  vector[J] eta;  // school effects
}
transformed parameters {
  vector[J] theta = mu + tau * eta;
}
model {
  eta ~ normal(0, 1);
  y ~ normal(theta, sigma);
}
generated quantities {
  real log_lik[J];
  for (j in 1:J)
    log_lik[j] = normal_lpdf(y[j] | theta[j], sigma[j]);
}