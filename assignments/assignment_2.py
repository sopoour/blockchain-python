# 1) Create a list of names and use a for loop to output the length of each name (len()).
list_names = ["Sophia", "Evelina", "Nicolas", "Alexander"]
check_names = False
for name in list_names:
    # 1)
    #print(name +":", len(name))
    # 2) Add an if check inside the loop to only output names longer than 5 characters.
    # 3) Add another if check to see whether a name includes a “n” or “N” character.
    if len(name) > 5 and ("n" in name or "N" in name):
        print(name + ":", len(name))

check_names = True

# 4) Use a while loop to empty the list of names (via pop())
while check_names:
    print(list_names)
    list_names.pop()
    if len(list_names) < 1:
        break
print("List is empty")

"""
better solution or a bit different:
while len(list_names) >= 1:
    print(list_names)
    list_names.pop()
print("List is empty")
"""