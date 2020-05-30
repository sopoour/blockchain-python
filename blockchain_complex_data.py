# NOTE: This program contains more complex data structures including tuples, sets and dictionaries

# Initialize important global variables
#Global constant that should never change --> you get 10 coins for mining a block
MINING_REWARD = 10
# Add a genenis block as the first block in a blockchain that is initialized from the beginning on
genenis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': []
}
blockchain = [genenis_block]
open_transactions = []
owner = 'Sophia'
participants = {'Sophia'}


def hash_block(block):
    # NOTE: Simple non-secure hashing of a block = append all key values into one string:
    # Previously, for loop to create a hashed_block
    # hashed_block = ''
    # for key in last_block:
    #     value = last_block[key]
    #     hashed_block = hashed_block + str(value)

    # use list comprehension for that instead of a separate for loop:
    # hashed_block = str([last_block[key] for key in last_block]) --> Problem: you get the brackets of list also stringified "["['', 0, []]", 1, [{'sender': 'Sophia', 'recipient': 'Anna', 'amount': 5.6}]]"
    # Better: use join method to add a character ("-") together with the list where the last_block[key] must be a string
    return "-".join([str(block[key]) for key in block])

def get_balance(participant):
    """Calculate the balance of each participant as verification check whether he can still send money"""
    #Amount Sent:
    #get the amount for a given transaction for all transactions in a block where the the sender of that transaction is the participant, do so for every block in the blockchain
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    #check not only the past sent amounts but also the open transaction amounts to send; same logic as above but for all the transactions in the open transactions
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant]
    #Now create one list with all the transaction amounts from both the blockchain what we spent there and we spent in the open transactions
    tx_sender.append(open_tx_sender)
    amount_sent = 0
    for tx in tx_sender:
        if len(tx) > 0:
            amount_sent += tx[0]

    #Amount received:
    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    amount_received = 0
    for tx in tx_recipient:
        if len(tx) > 0:
            amount_received += tx[0]
    return amount_received - amount_sent
    
def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    #check if we can afford the amount we want to send
    return sender_balance >= transaction['amount']


def add_transaction(recipient, sender=owner, amount=1.0):
    """ append a new value and last BC value to BC

    Arguments:
        :sender: the sender of the coins.
        :recipient: the recipient of the coins.
        :amount: the amount of coins sent with the transaction (default=1.0)
    """
    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        #Benefit of sets is here that if we add another Sophia which is already in the set it will ignore that
        #Hence sets make sure that we have only unique values in the set 
        participants.add(sender)
        participants.add(recipient)
        return True
    return False
# Create a new block


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    reward_transaction = {
        #the sender is hard-coded is basically the system which sends the reward
        'sender': "MINING",
        'recipient': owner,
        'amount': MINING_REWARD
    }

    #In order to manipulte the list only locally to be more safe you can copy the open_transactions to that copy
    #lists and other iterable data structures are copied by reference so that if I would simply set them both equal only the pointer would be
    #copied and not the values --> if I change the copied list it would also change the original list
    #so in case the mine block ever would deny adding that transaction we could safely do that without risking that the general open_transactions is affected
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    # when we always take the current len of the blockchain we get always an untaken index
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': copied_transactions
    }
    blockchain.append(block)
    return True


def get_transaction_value():
    """ retruns the input of the user (a new transaction amount) as a float"""
    tx_recipient = input("Enter the recipient of the transaction: ")
    tx_amount = float(input("Your transaction amount please: "))
    # return a tuple of recipient and amount; you could also make it more explicit by writing (tx_recipient, tx_amount) but you don't need to
    return tx_recipient, tx_amount


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
    # in order to get access to the index of the block, use enumerate method that returns a tuple of index and value
    # # then upack that tuple by writing the (index, block) in front
    for (index, block) in enumerate(blockchain):
        if index == 0:
           continue
        # check if the stored previous_hash of current block doesn't match the dynamic recalculation of the previous block
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
    return True
    
def verify_transactions():
    #check if all transactions in open_transactions are valid (=True)
    return all([verify_transaction(tx) for tx in open_transactions])
awaiting_input = True

while awaiting_input:
    print("Please choose:")
    print("1: Add a new transaction value")
    print("2: Mine a new block")
    print("3: Output the blockchain blocks")
    print("4: Output participants")
    print("5: Check transaction validity")
    print("h: Manipulate the chain")
    print("q: Quit")
    user_choice = get_user_choice()
    if user_choice == "1":
        tx_data = get_transaction_value()
        # one possibility is to unpack the tuple by following where the first element of the tuple will be assigned to the first variable (recipient):
        recipient, amount = tx_data
        # second possibility is to call the respective elements directly as argument as following:
        # add_transaction(owner, tx_data[0], tx_data[1])

        # skip the optional sender argument my having a named argument of amount
        #I can check it like that with if since add_transaction returns either True or False
        if add_transaction(recipient, amount=amount):
            print("Successfully added a transaction!")
        else:
            print("Transaction failed!")
        print(open_transactions)
    elif user_choice == "2":
        #reset the block when successful mined since the transactions are then already processed and shouldn't be processed again
        if mine_block():
            open_transactions = []
    elif user_choice == "3":
        print_blockchain_output()
    elif user_choice == "4":
        print(participants)
    elif user_choice == "5":

    # this is hack, which eventually needs to be prevented in our blockchain
    elif user_choice == "h":
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_transaction': '',
                'index': 0,
                'transaction': [{'sender': 'Alex', 'recipient': 'Sophia', 'amount': 100.0}]
            }
    elif user_choice == "q":
        awaiting_input = False
    else:
        print("Input was invalid, please pick one of the values 1 or 2.")

    """
    Check if results of verify_chain (from the returned is_valid) is not True 
    --> because "if verify_chain()" would check if True, which we would need if we want to continue, 
    but here we want to have the case that in case it's false we want to exit the loop
    """
    if not verify_chain():
        print_blockchain_output()
        print("Invalid blockchain!")
        break
    print(get_balance('Sophia'))

print("done!")
