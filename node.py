from uuid import uuid4
from blockchain_final import Blockchain
from verification import Verification

class Node:
    def __init__(self):
        #For now we comment it out because we need to figure out how to store the UUID
        #self.id = str(uuid4())
        self.id = 'Sophia'
        self.blockchain = Blockchain(self.id)
       

    def get_transaction_value(self):
        """ retruns the input of the user (a new transaction amount) as a float"""
        tx_recipient = input("Enter the recipient of the transaction: ")
        tx_amount = float(input("Your transaction amount please: "))
        # return a tuple of recipient and amount; you could also make it more explicit by writing (tx_recipient, tx_amount) but you don't need to
        return tx_recipient, tx_amount


    def get_user_choice(self):
        """ gets the choice of the user (rn: 1, 2, h, q)"""
        user_input = input("Your choice: ")
        return user_input


    def print_blockchain_output(self):
        """ prints the blockchain """
        for block in self.blockchain.chain:
            print("Outputting Block")
            print(block)
        else:
            print("-" * 20)


    def listen_for_input(self):
        awaiting_input = True
        while awaiting_input:
            print("Please choose:")
            print("1: Add a new transaction value")
            print("2: Mine a new block")
            print("3: Output the blockchain blocks")
            print("4: Check transaction validity")
            print("q: Quit")
            user_choice = self.get_user_choice()
            if user_choice == "1":
                tx_data = self.get_transaction_value()
                # one possibility is to unpack the tuple by following where the first element of the tuple will be assigned to the first variable (recipient):
                recipient, amount = tx_data
                # second possibility is to call the respective elements directly as argument as following:
                # add_transaction(owner, tx_data[0], tx_data[1])

                # skip the optional sender argument my having a named argument of amount
                #I can check it like that with if since add_transaction returns either True or False
                if self.blockchain.add_transaction(recipient, self.id, amount=amount):
                    print("Successfully added a transaction!")
                else:
                    print("Transaction failed!")
                print(self.blockchain.open_transactions)
            elif user_choice == "2":
                #reset the block when successful mined since the transactions are then already processed and shouldn't be processed again
                self.blockchain.mine_block()
            elif user_choice == "3":
                self.print_blockchain_output()
            elif user_choice == "4":
                verifier = Verification()
                if verifier.verify_transactions(self.blockchain.open_transactions, self.blockchain.get_balance):
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
            verifier = Verification()
            if not verifier.verify_chain(self.blockchain.chain):
                self.print_blockchain_output()
                print("Invalid blockchain!")
                break
            print('Balance of {}:{:6.2f}'.format(self.id, self.blockchain.get_balance()))

        print("done!")

node = Node()
node.listen_for_input()