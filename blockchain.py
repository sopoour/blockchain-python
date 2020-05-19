blockchain = []


def get_last_value():
    return blockchain[-1]

# Use default value [1] for last_transaction by having the second argument written like "last_transaction=[1]"


def add_value(transaction_amount, last_transaction=[1]):
    blockchain.append([last_transaction, transaction_amount])


def get_user_input():
    return float(input("Your transaction amount please: "))


tx_amount = get_user_input()
# due to the default of 1 I don't have to add it for the first time I call the add_value function
add_value(tx_amount)

tx_amount = get_user_input()
add_value(tx_amount, get_last_value())

tx_amount = get_user_input()
add_value(tx_amount, get_last_value())

"""
#you can also have keyboard arguments in case you don't remember the argument's order or just want to switch it:

add_value(2)
add_value(last_transaction=get_last_value(), last_transaction=0.9)
"""

print(blockchain)
