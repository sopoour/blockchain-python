# 1 Create two variables – one with your name and one with your age
name = "Sophia"
age = 24

# 2 Create a function which prints your data as one string
def print_data():
    print("My name is: " + name, "\nMy age is: " + str(age))

print_data()

# 3 Create a function which prints ANY data (two arguments) as one string
def print_any_data(name_arg, age_arg):
    """
    Arguments:
        :name_arg: takes your name in String
        :age_arg: takes your age in Int
    """
    print("My name is: " + name_arg, "\nMy age is: " + str(age_arg))
    
print_any_data("Anna", 18)

# 4 Create a function which calculates and returns the number of decades you already lived (e.g. 23 = 2 decades)
def calc_decade(age_new):
    print("I have lived so far in " + str(age_new // 10) + " decades.")

calc_decade(24)
