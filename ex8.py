#3 ways to reverse a string
#using for loop
#using inbuild reversed() fn
#using extended slice syntax
#1.for loop

def reversej(s):
    result = ""
    for i in s:
        result=i+result
    return result
si = "intelligent"
print("original string:",si)
print("reverse post :",reversej(si))