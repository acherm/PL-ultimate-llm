# steel.mod
#
# A simple steel production model.

set PROD;     # products

param rate {PROD} > 0;              # tons produced per hour
param profit {PROD} > 0;            # profit per ton
param market {PROD} >= 0;           # market limit on tons sold

param avail >= 0;                   # hours available

var Make {p in PROD} >= 0, <= market[p];  # tons of product p to make

maximize Total_Profit: sum {p in PROD} profit[p] * Make[p];

subject to Time: sum {p in PROD} (1/rate[p]) * Make[p] <= avail;