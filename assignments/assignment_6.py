# 1) Write a short Python script which queries the user for input (infinite loop with exit possibility) and writes the input to a file.

wait_user = True

while wait_user:
    print("Please choose from below options:")
    print("Option 1: Write Something to a File")
    print("Option 2: Exit")
    print("Option 3: Output written text in terminal")
    user_input = input("Your Option: ")
    
    if user_input == "1":
        text = input("Your text: ")
        with open("input.txt", mode="a") as f:
            f.write(text)
    elif user_input == "2":
        wait_user = False
    # 2) Add another option to your user interface: The user should be able to output the data stored in the file in the terminal.
    elif user_input == "3":
        with open("input.txt", mode="r") as f:
            loaded_text = f.readlines()
            for line in loaded_text:
                print("Your stored text: " + line)
# 3) Store user input in a list (instead of directly adding it to the file) and write that list to the file – both with pickle and json.
import json
import pickle

wait_user1 = True
text_list = []
while wait_user1:
    print("Please choose from below options:")
    print("Option 1: Write Something to a File")
    print("Option 2: Exit")
    print("Option 3: Output written text in terminal")
    user_input = input("Your Option: ")
    if user_input == "1":
        text = input("Your text: ")
        text_list.append(text)
        #with JSON:
        with open("input.txt", mode="w") as f:
            f.write(json.dumps(text_list))
        #with pickle:
        with open("input.p", mode="wb") as f:
            f.write(pickle.dumps(text_list))
    elif user_input == "2":
        wait_user1 = False
    elif user_input == "3":
        with open("input.txt", mode="r") as f:
            # 4) Adjust the logic to load the file content to work with pickled/ json data.
            loaded_text = json.loads(f.read())
            print("Written from JSON file: ")
            for text in loaded_text:
                print(text)
        with open("input.p", mode="rb") as f:
            loaded_text = pickle.loads(f.read())
            print("Written from pickle file: ")
            for text in loaded_text:
                print(text)
