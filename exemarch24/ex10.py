#extended slice - reversing
s=input("enter a string to know if palindrome or not:")
print(s,s[::-1],sep=" ")
if s==s[::-1]:
    print("it is palindrome")
else:
    print("not a palindrome")