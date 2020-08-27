# NOTE: This program contains more complex data structures including tuples, sets and dictionaries

import functools
import hashlib as hl
from collections import OrderedDict
import json
#convert python data to binary data which is stored in a file, you are able to serialize and unserialize your data
import pickle

#import another file and classes
from hash_util import hash_string_256, hash_block
from block import Block

# Initialize important global variables
#Global constant that should never change --> you get 10 coins for mining a block
MINING_REWARD = 10
blockchain = []
open_transactions = []
owner = 'Sophia'
participants = {'Sophia'}

def load_data():
    #make variables global to use it in this function
    global blockchain
    global open_transactions
    try:
        with open('blockchain.txt', mode="r") as f:
            file_content = f.readlines()           
            #For JSON: You need to do all of that since it converts it to string and back --> loosing the ordereddict structure
            # file_content = f.readlines()
            #define the first line of the content as blockchain and second line as open_transactions
            #add [:-1] in order to not load the \n
            blockchain = json.loads(file_content[0][:-1])
            updated_blockchain = []
            #need to convert every block again into a ordered dict otherwise it cannot read the transaction later
            for block in blockchain:
                converted_tx = [OrderedDict([('sender', tx['sender']), ('recipient', tx['recipient']), ('amount', tx['amount'])]) for tx in block['transactions']]
                updated_block = Block(block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])
            
                updated_blockchain.append(updated_block)
                blockchain = updated_blockchain
                #same as before for open transactions
                open_transactions = json.loads(file_content[1])
                updated_transactions = []
                for tx in open_transactions:
                    updated_transaction = OrderedDict([('sender', tx['sender']), ('recipient', tx['recipient']), ('amount', tx['amount'])])
                    updated_transactions.append(updated_transaction)
                open_transactions = updated_transactions
    #Except when a special error occurs; 
    #You have to specify the error and you can also specify multiple errors "except (IOError, ValueError)""
    #You should always specify the error and not just use "except:" because then you might catch too many errors
    #You can also use "Finally:" in order to have some tasks that should always run no matter the error --> good for cleanup work
    #IO error: groups all file related errors (this is the case here)
    #In this way the program doesn't stop and still continues
    except (IOError, IndexError):
        # When I don't have a file yet, it means I don't have a blockchain yet so that we initialize the blockchain with our genesis block in this exception
        # Add a genenis block as the first block in a blockchain that is initialized from the beginning on
        genenis_block = Block(0, '', [], 100, 0)
        blockchain = [genenis_block]
        open_transactions = []

load_data()

def save_data():
    try:
        with open('blockchain.txt', mode="w") as f:
            #Here again converting from object to dict and here we don't need copy() cuz we don't manipulate anything
            #ERROR!!
            savable_chain = [block.__dict__ for block in blockchain]
            #With JSON:
            f.write(json.dumps(savable_chain) + "\n" + json.dumps(open_transactions))

    except (IOError, IndexError):
        print("Saving failed!")

def valid_proof(transactions, last_hash, proof):
    """Check: Only a hash with "00" is valid"""
    #concertinate all of it together as string and encode in order to get a proper UTF8 string
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    #hash that guess
    guess_hash = hash_string_256(guess)
    print(guess_hash)
    #check that the hash starts with two zeros
    return guess_hash[0:2] == "00"

def proof_of_work():
    """Increment the proof number"""
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof

def get_balance(participant):
    """Calculate the balance of each participant as verification check whether he can still send money"""
    #Amount Sent:
    #get the amount for a given transaction for all transactions in a block where the sender of that transaction is the participant, do so for every block in the blockchain
    tx_sender = [[tx['amount'] for tx in block.transactions if tx['sender'] == participant] for block in blockchain]
    #check not only the past sent amounts but also the open transaction amounts to send; same logic as above but for all the transactions in the open transactions
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant]
    #Now create one list with all the transaction amounts from both the blockchain what we spent there and we spent in the open transactions
    tx_sender.append(open_tx_sender)
    #instead of a for loop, you can use a reduce method:
    #function to be used on list: lambda...; list to be reduced: tx_sender; initial value: 0
    #pass on the current sum and amount of transactions; go through all the values of tx_sender, get access to the current value which is the first element of the nested list tx_sender (tx_amt[0]) and add it to the current sum (tx_sum)
    #check additionally whether the tx_amt is greater than 0, otherwise add 0
    #UPDATE: we need sum(tx_amt) instead of tx_amt[0] in order to sum all the added open transactions + we neext to change else 0 to else tx_sum + 0 otherwise it always returns back to 20 when mining 
    amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
    
    #Amount received:
    tx_recipient = [[tx['amount'] for tx in block.transactions if tx['recipient'] == participant] for block in blockchain]
    #Same logic as for amount_sent above:
    amount_received = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
    mount_received += tx[0]
        
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

    #NEW: Ordered Dictionary - important for hashing
    transaction = OrderedDict(
        [('sender', sender), ('recipient', recipient), ('amount', amount)])

    if verify_transaction(transaction):
        open_transactions.append(transaction)
        #Benefit of sets is here that if we add another Sophia which is already in the set it will ignore that
        #Hence sets make sure that we have only unique values in the set 
        participants.add(sender)
        participants.add(recipient)
        save_data()
        return True
    return False
# Create a new block


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work()
    ##Add the proof of work within our block

    #NEW: ordered dictionary
    reward_transaction = OrderedDict(
        [('sender', "MINING"), ('recipient', owner), ('amount', MINING_REWARD)])
    #In order to manipulte the list only locally to be more safe you can copy the open_transactions to that copy
    #lists and other iterable data structures are copied by reference so that if I would simply set them both equal only the pointer would be
    #copied and not the values --> if I change the copied list it would also change the original list
    #so in case the mine block ever would deny adding that transaction we could safely do that without risking that the general open_transactions is affected
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    # when we always take the current len of the blockchain we get always an untaken index
    block = Block(len(blockchain), hashed_block, copied_transactions, proof)
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
        if block.previous_hash != hash_block(blockchain[index - 1]):
            return False
        # ADD: additional check that we have two zeros in the hash
        # if the proof is not true then we want it to be invalid
        # transactions: in order to exlude the reward transaction add [:-1], meaning the last transaction is excluded
        if not valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
            print("Proof of Work is invalid")
            return False
    return True
    
def verify_transactions():
    """Verifies all open transactions."""
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
            save_data()
    elif user_choice == "3":
        print_blockchain_output()
    elif user_choice == "4":
        print(participants)
    elif user_choice == "5":
        if verify_transactions():
            print('All transactions are valid')
        else:
            print('There are invalid transactions')
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
    print('Balance of {}:{:6.2f}'.format('Sophia', get_balance('Sophia')))

print("done!")
