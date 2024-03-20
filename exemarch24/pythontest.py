#input- no of alphabets
'''
___A
__A B__
_A B C_
'''
rows = int(input("Enter alphabets :"))

for i in range(1,rows+1):
    for j in range(1,rows-i+1):
        print(end=" ")
    for num in range(1,(2*i)):
        print(chr(64+num),end="")
    print()
for i in range(rows-1,0,-1):
    for j in range(1,rows-i+1):
        print(end=" ")
    for num in range(1,2*i):
        print(chr(64+num),end="")
    print()
