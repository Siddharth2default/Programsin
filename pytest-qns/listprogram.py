
fruits = ['mango', 'apples', 'orange']

juice = ['vannila', 'pista', 'plum']
list3 = []

for i, j in zip(fruits, juice):
    list3.append(i + ':' + j)

print(list3)

