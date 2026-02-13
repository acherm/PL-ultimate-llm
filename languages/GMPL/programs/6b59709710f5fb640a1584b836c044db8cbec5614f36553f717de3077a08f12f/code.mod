/* Diet problem: minimize cost of food while meeting nutritional requirements */

set FOOD;
set NUTRIENTS;

param cost{FOOD} >= 0;
param nutrient_content{FOOD, NUTRIENTS} >= 0;
param min_nutrient{NUTRIENTS} >= 0;
param max_nutrient{NUTRIENTS} >= 0;

var amount{FOOD} >= 0;

minimize total_cost: sum{f in FOOD} cost[f] * amount[f];

s.t. nutrient_min{n in NUTRIENTS}:
    sum{f in FOOD} nutrient_content[f,n] * amount[f] >= min_nutrient[n];

s.t. nutrient_max{n in NUTRIENTS}:
    sum{f in FOOD} nutrient_content[f,n] * amount[f] <= max_nutrient[n];

data;

set FOOD := Bread Milk Eggs Chicken;
set NUTRIENTS := Protein Calories Fat;

param cost :=
    Bread   0.50
    Milk    1.20
    Eggs    1.50
    Chicken 3.00;

param nutrient_content:
            Protein  Calories  Fat :=
    Bread       3      265      1
    Milk        8      150      8
    Eggs       13      155     11
    Chicken    26      220     12;

param min_nutrient :=
    Protein  50
    Calories 2000
    Fat      20;

param max_nutrient :=
    Protein  200
    Calories 3000
    Fat      100;

end;
