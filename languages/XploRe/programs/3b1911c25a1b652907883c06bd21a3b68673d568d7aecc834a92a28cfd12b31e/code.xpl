; XploRe: Descriptive Statistics Demo
; Simulates data and computes summary statistics

n  = 100           ; sample size
p  = 2             ; number of variables
x  = normal(n, p)  ; simulate n x p standard normal data

; Compute descriptive statistics
xmean = mean(x)    ; column means
xvar  = var(x)     ; column variances
xcor  = cor(x)     ; correlation matrix

show "Sample means:"
show xmean
show "Sample variances:"
show xvar
show "Correlation matrix:"
show xcor
