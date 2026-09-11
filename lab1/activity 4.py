username = input('Enter Username: ')
age = int(input('Enter Age: '))
category = input('Enter Content Category: ')

print("Instragram Profile")
print("==================")
print("Username:", username)
print("Age:", age)
print("Category: ", category)

if age>40 and category == "fun":
    print("You are old what is fun for you??")