a = ["Navin","Sidd","Amala"]
b =["Dell","Apple","MS"]
c=[]
'''
zipped = (list(zip(names,comps)))
print(zipped)
c =[]
for a,b in zipped:
    c.append(a+":"+b)

print(c)
'''
for i in range(len(a)):
    c.append(a[i]+":"+b[i])

print(c)
