x={}

print('how many players? ',end=' ')
n=int(input())

for i in range(n):
    print('enter player name: ',end=' ')
    k=input()
    print('enter runs: ',end=' ')
    v=int(input())
    x.update({k:v})

print('\n player in this match: ')
for pname in x.keys():
    print(pname)

print('enter player name: ',end=' ')
name=input()

runs=x.get(name,-1)
if(runs==-1):
    print('player not found')
else:
    print('{} made runs {}'.format(name,runs))
