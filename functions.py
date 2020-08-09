#*args lets the function take any amount of arguments, seperated by comma, and turn it into a tuple of arguments which you can use in a for loop
#for unnamed arguments one star is enough, for named arguments (dictionary type of) we need two stars
def unlimited_arguments(*args, **keyword_args):
    print(args)
    print(keyword_args)
    for k, argument in keyword_args.items():
        print(k, argument)

unlimited_arguments(1,2,3,4, name='Max', age=29)

#you can use this *args feature now for the format method in Python to unpack dynamically an entire list for arguments
a = [1,2,3]
print('Some text: {} {} {}'.format(*a))