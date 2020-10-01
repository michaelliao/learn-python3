#program to print prime no. upto a given number
max=int(input("upto what no.?"))
for num in range(2,max+1):#generate from 2 onwards till maxx
    for i in range(2,num):#i represent no. from 2 to num-1
        if (num % i) == 0:#if num is divisible by i
            break#then it is not a prime no.and then go back
    else:
        print(num)