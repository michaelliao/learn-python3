#Binary search in python
#Author-Nikita Jain
l=[]
f=0
s=input("Enter the list in ascending order")
l=s.split()
for x in range(0,len(l)):
    l[x]=int(l[x])
lb=0
ub=len(l)
ele=int(input("enter the element to be searched"))
while(lb<=ub):
    m=int((lb+ub)/2)
    if(l[m]==ele):
        print("element found at position",m+1)
        f=1
        break
    if(l[m]<ele):
        lb=m+1
    else:
        ub=m-1
if(f==0):
    print("element not found")

    

