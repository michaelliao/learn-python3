#using continue to execcute next iteration of while loop
x=0
while x<10:
    x+=1
    #print(x)
    if x>5:#if x>5 then continue next iterration
        continue
        #break#or you can use pass statemnt when u don't care about result
    print('x= ',x)
print("out of loop")