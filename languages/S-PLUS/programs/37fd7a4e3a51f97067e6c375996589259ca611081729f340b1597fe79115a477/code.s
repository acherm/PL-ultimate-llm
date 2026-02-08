# Linear regression example in S-PLUS
# Create sample data
x <- c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
y <- c(2.1, 4.3, 6.2, 8.1, 10.3, 12.1, 14.2, 16.1, 18.3, 20.2)

# Fit linear model
model <- lm(y ~ x)

# Display summary
summary(model)

# Plot data and fitted line
plot(x, y, main="Linear Regression", xlab="X", ylab="Y")
abline(model, col="red")
