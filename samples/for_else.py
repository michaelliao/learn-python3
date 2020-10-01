#searching for an element in a list
group1=[1,2,3,4,5]#take a list of element
search=int(input('enter element t0 search: '))
for element in group1:
    if search==element:
        print('element found')
        break#come out of for  loop
else:
    print('element not found')#this is else suite