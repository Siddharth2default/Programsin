a = int(input("Enter count:"))
'''
for i in range(1,a+1):
    print(chr(64+i),end="")
print()
for i in range(1,a+1):
    print(chr(64+i),end="")
print()
for i in range(1,a+1):
    print(chr(64+i),end="")
print()
for i in range(1,a+1):
    print(chr(64+i),end="")
*_
**_
***_
****
'''

for i in range(1,a+1):
    for j in range(a-i+1):
        print("#",end="")
    print()