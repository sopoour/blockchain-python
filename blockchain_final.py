# NOTE: This program contains more complex data structures including tuples, sets and dictionaries

import functools
import hashlib as hl
import json
#convert python data to binary data which is stored in a file, you are able to serialize and unserialize your data
import pickle

#import another file and classes
from hash_util import hash_block
from block import Block
from transaction import Transaction
from verification import Verification

#Global constant that should never change --> you get 10 coins for mining a block
MINING_REWARD = 10

class Blockchain:
    def __init__(self, hosting_node_id):
        # When I don't have a file yet, it means I don't have a blockchain yet so that we initialize the blockchain with our genesis block in this exception
        # Add a genenis block as the first block in a blockchain that is initialized from the beginning on
        # we can have the initiatization of genesis_block just in here and chain will be overwritten anyways
        genenis_block = Block(0, '', [], 100, 0)
        # Initializing our empty blokckchain list
        self.chain = [genenis_block]
        self.open_transactions = []
        # I want the load_data method to run every time a blockchain is newly initiated
        self.load_data()
        self.hosting_node = hosting_node_id

    def load_data(self):
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
                    #Calling Transaction class
                    converted_tx = [Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in block['transactions']]
                    updated_block = Block(block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])
                
                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain
                #same as before for open transactions
                open_transactions = json.loads(file_content[1])
                updated_transactions = []
                for tx in open_transactions:
                    updated_transaction = Transaction(tx['sender'], tx['recipient'], tx['amount'])
                    updated_transactions.append(updated_transaction)
                self.open_transactions = updated_transactions
        #Except when a special error occurs; 
        #You have to specify the error and you can also specify multiple errors "except (IOError, ValueError)""
        #You should always specify the error and not just use "except:" because then you might catch too many errors
        #You can also use "Finally:" in order to have some tasks that should always run no matter the error --> good for cleanup work
        #IO error: groups all file related errors (this is the case here)
        #In this way the program doesn't stop and still continues
        except (IOError, IndexError):
            print("Handled exception...")

    def save_data(self):
        try:
            with open('blockchain.txt', mode="w") as f:
                #Here again converting from object to dict and here we don't need copy() cuz we don't manipulate anything
                #The block should be already a Block object, therefore every dict element should be an attribute of the block to access it properly
                savable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) for block_el in self.chain]]
                #needs to be converted to dict in order to be able to be dumped into json
                savable_tx = [tx.__dict__ for tx in self.open_transactions]
                #With JSON:
                f.write(json.dumps(savable_chain) + "\n" + json.dumps(savable_tx))

        except (IOError, IndexError):
            print("Saving failed!")


    def proof_of_work(self):
        """Increment the proof number"""
        last_block = self.chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        verifier = Verification()
        while not verifier.valid_proof(self.open_transactions, last_hash, proof):
            proof += 1
        return proof

    def get_balance(self):
        """Calculate the balance of each participant as verification check whether he can still send money"""
        participant = self.hosting_node
        #Amount Sent:
        #get the amount for a given transaction for all transactions in a block where the sender of that transaction is the participant, do so for every block in the blockchain
        tx_sender = [[tx.amount for tx in block.transactions if tx.sender== participant] for block in self.chain]
        #check not only the past sent amounts but also the open transaction amounts to send; same logic as above but for all the transactions in the open transactions
        open_tx_sender = [tx.amount for tx in self.open_transactions if tx.sender == participant]
        #Now create one list with all the transaction amounts from both the blockchain what we spent there and we spent in the open transactions
        tx_sender.append(open_tx_sender)
        #instead of a for loop, you can use a reduce method:
        #function to be used on list: lambda...; list to be reduced: tx_sender; initial value: 0
        #pass on the current sum and amount of transactions; go through all the values of tx_sender, get access to the current value which is the first element of the nested list tx_sender (tx_amt[0]) and add it to the current sum (tx_sum)
        #check additionally whether the tx_amt is greater than 0, otherwise add 0
        #UPDATE: we need sum(tx_amt) instead of tx_amt[0] in order to sum all the added open transactions + we neext to change else 0 to else tx_sum + 0 otherwise it always returns back to 20 when mining 
        amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
        
        #Amount received:
        tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in self.chain]
        #Same logic as for amount_sent above:
        amount_received = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
            
        return amount_received - amount_sent
    
    def get_last_blockchain_value(self):
        """ Return the last value of the current blockchain. """
        if len(self.chain) < 1:
            return None
        return self.chain[-1]

    def add_transaction(self, recipient, sender, amount=1.0):
        """ append a new value and last BC value to BC

        Arguments:
            :sender: the sender of the coins.
            :recipient: the recipient of the coins.
            :amount: the amount of coins sent with the transaction (default=1.0)
        """
        transaction = Transaction(sender, recipient, amount)
        verifier = Verification()
        if verifier.verify_transaction(transaction, self.get_balance):
            self.open_transactions.append(transaction)
            #Benefit of sets is here that if we add another Sophia which is already in the set it will ignore that
            #Hence sets make sure that we have only unique values in the set 
            self.save_data()
            return True
        return False
    
    # Create a new block
    def mine_block(self):
        last_block = self.chain[-1]
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        ##Add the proof of work within our block

        reward_transaction = Transaction('MINING', self.hosting_node, MINING_REWARD)
        #In order to manipulte the list only locally to be more safe you can copy the open_transactions to that copy
        #lists and other iterable data structures are copied by reference so that if I would simply set them both equal only the pointer would be
        #copied and not the values --> if I change the copied list it would also change the original list
        #so in case the mine block ever would deny adding that transaction we could safely do that without risking that the general open_transactions is affected
        copied_transactions = self.open_transactions[:]
        copied_transactions.append(reward_transaction)
        # when we always take the current len of the blockchain we get always an untaken index
        block = Block(len(self.chain), hashed_block, copied_transactions, proof)
        self.chain.append(block)
        self.open_transactions = []
        self.save_data()
        return True



