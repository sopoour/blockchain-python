from hash_util import hash_string_256, hash_block

class Verification:

    def valid_proof(self, transactions, last_hash, proof):
        """Check: Only a hash with "00" is valid"""
        # concertinate all of it together as string and encode in order to get a proper UTF8 string
        guess = (str([tx.to_ordered_dict() for tx in transactions]) + str(last_hash) + str(proof)).encode()
        # hash that guess
        guess_hash = hash_string_256(guess)
        print(guess_hash)
        # check that the hash starts with two zeros
        return guess_hash[0:2] == "00"
        
    def verify_chain(self, blockchain):
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
            if not self.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                print("Proof of Work is invalid")
                return False
        return True
    
    def verify_transaction(self, transaction, get_balance):
        sender_balance = get_balance()
        # check if we can afford the amount we want to send
        return sender_balance >= transaction.amount
    
    def verify_transactions(self, open_transactions, get_balance):
        """Verifies all open transactions."""
        # check if all transactions in open_transactions are valid (=True)
        return all([self.verify_transaction(tx, get_balance) for tx in open_transactions])


    
