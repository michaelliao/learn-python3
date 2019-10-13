l=[]
f=0
n=int(input("enter the size of list:"))
s=input("enter the numbers:")
l=s.split()
for i in range (0,n):
    l[i]=int(l[i])
ele=int(input("enter the element to be searched"))
for i in range (0,n):
    if l[i]==ele:
        print("element found at position",i+1)
        f=1
if f==0:
    print("element not found")
    
