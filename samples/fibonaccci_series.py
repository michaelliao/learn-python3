#program to display fibonacci series
n=int(input('how many fibonacci?'))
f1=0
f2=1
c=0
if n==1:
    print(f1)
elif n==2:
    print(f1,'\n',f2,sep='')
else:
    print(f1,'\n',f2,sep='')
    while c<n:
        f=f1+f2
        print(f)
        f1=f2
        f2=f
        c+=1