str='vijay=23,ganesh=20,lakshmi=19,nikhil=22'

lst=[]
for x in str.split(','):
    y=x.split('=')
    lst.append(y)
    print(y)

d=dict(lst)
d1={}
for k,v in d.items():
    d1[k]=int(v)
print(d1)