# Simple Knapsack Problem in Zimpl
set Items := { "item1", "item2", "item3" };
param weight[Items] := <"item1"> 10, <"item2"> 20, <"item3"> 30;
param value[Items] := <"item1"> 60, <"item2"> 100, <"item3"> 120;
param capacity := 50;

var x[Items] binary;

maximize profit: sum <i> in Items: value[i] * x[i];
subto weight_limit: sum <i> in Items: weight[i] * x[i] <= capacity;