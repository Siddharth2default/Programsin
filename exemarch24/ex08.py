'''
def topten(num):
    while num <= 10:
        print(num)
        num += 1


values = topten(5)
'''


def topten(num):
    while num <= 10:
        yield num
        num += 1


values = topten(5)
for i in values:
    print(i)
