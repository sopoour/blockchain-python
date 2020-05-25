blockchain = []


def get_last_value():
    """ returns the last value of the current blockchain """
    if len(blockchain) < 1:
        # this is used to tell the program there is nothing yet
        return None
    # implicit else statement
    return blockchain[-1]

# Use default value [1] for last_transaction by having the second argument written like "last_transaction=[1]"


def add_transaction(transaction_amount, last_transaction=[1]):
    """ append a new value and last BC value to BC

    Arguments:
        :transaction_amount: the amount that should be added.
        :last_transaction: the last BC transaction (default [1])
    """
    if last_transaction == None:
        last_transaction = [1]
    blockchain.append([last_transaction, transaction_amount])


def get_transaction_value():
    """ retruns the input of the user (a new transaction amount) as a float"""
    return float(input("Your transaction amount please: "))


def get_user_choice():
    """ gets the choice of the user (rn: 1, 2, h, q)"""
    user_input = input("Your choice: ")
    return user_input


def print_blockchain_output():
    """ prints the blockchain """
    for block in blockchain:
        print("Outputting Block")
        print(block)
    else:
        print("-" * 20)


def verify_chain():
    """Verifies whether the previous block equals the first element of the current block => Ensure Immutability"""
    block_index = 0
    is_valid = True
    for block_index in range(len(blockchain)):
        # in case it's the first block in the blockchain, hence no previous block, we want to iterate and start the for loop again
        if block_index == 0:
            continue
        # check if the first part ([0]) of the current block (=blockchain[block_index]; e.g. [[[1], 3.4], 5.6]) equals the previous block (e.g. [[1], 3.4])
        elif blockchain[block_index][0] == blockchain[block_index - 1]:
            is_valid = True
        # otherwise exit loop since there must have been a hack due to mutation
        else:
            is_valid = False
            break
    return is_valid


awaiting_input = True

while awaiting_input:
    print("Please choose:")
    print("1: Add a new transaction value")
    print("2: Output the blockchain blocks")
    print("h: Manipulate the chain")
    print("q: Quit")
    user_choice = get_user_choice()
    if user_choice == "1":
        tx_amount = get_transaction_value()
        add_transaction(tx_amount, get_last_value())
    elif user_choice == "2":
        print_blockchain_output()
    # this is hack, which eventually needs to be prevented in our blockchain
    elif user_choice == "h":
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    elif user_choice == "q":
        waiting = False
    else:
        print("Input was invalid, please pick one of the values 1 or 2.")

    """Check if results of verify_chain (from the returned is_valid) is not True 
    --> because "if verify_chain()" would check if True, which we would need if we want to continue, 
    but here we want to have the case that in case it's false we want to exit the loop"""
    if not verify_chain():
        print_blockchain_output()
        print("Invalid blockchain!")
        break

print("done!")

"""
OLD CODE:

tx_amount = get_transaction_value()
# due to the default of 1 I don't have to add it for the first time I call the add_value function
add_value(tx_amount)

tx_amount = get_user_input()
add_value(tx_amount, get_last_value())

tx_amount = get_user_input()
add_value(tx_amount, get_last_value())"""

"""
you can also have keyboard arguments in case you don't remember the argument's order or just want to switch it:

add_value(2)
add_value(last_transaction=get_last_value(), last_transaction=0.9)
"""