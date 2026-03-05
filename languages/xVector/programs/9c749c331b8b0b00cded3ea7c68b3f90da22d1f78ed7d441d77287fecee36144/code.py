import sys
def cross(x,y):
 a,b,c,d,e,f=x+y
 return (b*f-c*e,c*d-a*f,b*d-a*e)
k=sys.stdin.read().strip().split('\n')
acc=(0.0,0.0,0.0)
p=0
while p<len(k):
 kp=k[p]
 if len(kp.split())==9:
  a,b,c,h,i,j,e,f,g=list(map(float,kp.split()))
  if cross(acc,(a,b,c))==(h,i,j):
   acc=(acc[0]+e,acc[1]+f,acc[2]+g)
   p=0
   continue
 else:
  a,b,c,l,m,n,e,f,g,h,i,j=list(map(float,kp.split()))
  if cross(acc,(a,b,c))==(l,m,n):
   print(chr(int(cross(acc,(h,i,j))[0])),end='')
   acc=(acc[0]+e,acc[1]+f,acc[2]+g)
   p=0
   continue
 p+=1
