str="google"

dict={}

for x in str:
    dict[x]=dict.get(x,0)+1

for k,v in dict.items():
    print('key={}\t Its occurrences={}'.format(k,v))