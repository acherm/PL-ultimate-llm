using Gen

# Define a simple Bayesian linear regression model
@gen function linear_regression(xs::Vector{Float64})
    slope = @trace(normal(0.0, 2.0), :slope)
    intercept = @trace(normal(0.0, 2.0), :intercept)
    noise = @trace(gamma(2.0, 0.5), :noise)
    for (i, x) in enumerate(xs)
        @trace(normal(slope * x + intercept, noise), (:y, i))
    end
end

# Sample some observed data
xs = [1.0, 2.0, 3.0, 4.0, 5.0]
ys = [2.1, 3.9, 6.2, 8.1, 10.0]

# Condition on observations
observations = choicemap()
for (i, y) in enumerate(ys)
    observations[(:y, i)] = y
end

# Run importance sampling to infer slope and intercept
traces, log_weights, _ = importance_sampling(linear_regression, (xs,), observations, 1000)

# Estimate posterior means
slopes = [tr[:slope] for tr in traces]
intercepts = [tr[:intercept] for tr in traces]
weights = exp.(log_weights .- logsumexp(log_weights))

println("Posterior mean slope:     ", sum(slopes .* weights))
println("Posterior mean intercept: ", sum(intercepts .* weights))
