# 1) Write a normal function that accepts another function as an argument. Output the result of that other function in your “normal” function.
def square (num):
    return num*num

def changed(func):
    square = func(4)
    print(square)

print("With function that accepts another function as argument:")
changed(square)

# 2) Call your “normal” function by passing a lambda function – which performs any operation of your choice – as an argument.
print("With lambda function:")
changed(lambda num: num*num)

# 3) Tweak your normal function by allowing an infinite amount of arguments on which your lambda function will be executed.
print("With lambda function and infinte arguments:")
def changed2(func, *args):
    for argument in args:
        print(func(argument))

changed2(lambda num: num*num, 6, 8, 10)
# 4) Format the output of your “normal” function such that numbers look nice and are centered in a 20 character column.
def changed2(func, *args):
    for argument in args:
        print('Result: {:^20.2f}'.format(func(argument)))

changed2(lambda num: num*num, 6, 8, 10)
