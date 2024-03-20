#python
ac = input("Enter a word")
vowels = "aeiouAEIOU"

for j in ac:
    if j not in vowels:
        print(j,"is consonant")

for i in ac:
    if i in vowels:
        print(i,"is vowel")
