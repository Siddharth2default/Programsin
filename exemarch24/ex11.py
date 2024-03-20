'''
#factorial
num = int(input("Enter a number"))
if num <0:
    print("Factorial is not possible")
else:
    fact = 1
    for i in range(1,num+1):
        fact = fact*i
        print(fact)
    print("factorial of number is:",fact)

#fibonacci
#0 1 1 2 3 5 8 13 21 34 55
num = int(input("Series count:"))
a,b=0,1
c=0
for i in range(1,num+1):
    a=b #a-1
    b=c #b-0
    print(c,end=" ")
    c = a + b
    '''
#num=int(input("Series:"))
a,b=0,1
while a<10:
    print("pre a-b",a,b)
    a,b=b,a+b
    print("post a-b",a,b)
    #a=b
    #b=a+b