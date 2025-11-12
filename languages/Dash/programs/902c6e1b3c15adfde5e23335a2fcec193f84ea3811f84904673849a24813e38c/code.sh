# Iterative
f0=0
f1=1
echo $f0
echo $f1
for i in `seq 3 20`
do
  fn=`echo "$f0 + $f1" | bc`
  echo $fn
  f0=$f1
  f1=$fn
done