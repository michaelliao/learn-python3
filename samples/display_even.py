#to display even no. between m and n
m,n=[int(i) for i in input("enter max. and min. range: ").split(',')]
x=m#start  from m  onwards
if x%2!=0:
    x+=1
while x>=m and x<=n:
    print(x)
    x+=2