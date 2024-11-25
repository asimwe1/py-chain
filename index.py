import hashlib
import time
import json

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = time.time()

    def to_dict(self):
        return {"sender": self.sender, "recipient": self.recipient, "amount": self.amount, "timestamp": self.timestamp}

class Block:
    def __init__(self, index, timestamp, transactions, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        transactions_str = json.dumps([t.to_dict() for t in self.transactions], sort_keys=True)
        data_to_hash = (str(self.index) + str(self.timestamp) + transactions_str + self.previous_hash + str(self.nonce))
        return hashlib.sha256(data_to_hash.encode()).hexdigest()

    def mine_block(self, difficulty):
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4
        self.pending_transactions = []
        self.transaction_pool_limit = 10
        self.balances = {}  # Dictionary to store account balances

    def create_genesis_block(self):
        return Block(0, time.time(), [], "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                print(f"Block {current_block.index} has been tampered.")
                return False

            if current_block.previous_hash != previous_block.hash:
                print(f"Block {current_block.index} has an invalid link.")
                return False

        return True

    def add_transaction(self, transaction):
        # Check if the sender has enough balance before adding the transaction
        sender_balance = self.get_balance(transaction.sender)
        if sender_balance >= transaction.amount:
            self.pending_transactions.append(transaction)
        else:
            print(f"Transaction from {transaction.sender} failed: Insufficient balance.")
            return

        if len(self.pending_transactions) >= self.transaction_pool_limit:
            self.mine_pending_transactions()

    def mine_pending_transactions(self):
        if not self.pending_transactions:
            print("No transactions to mine.")
            return

        new_block = Block(
            len(self.chain), 
            time.time(),
            self.pending_transactions,
            self.get_latest_block().hash
        )

        print(f"Mining block {new_block.index}...")
        self.add_block(new_block)

        # Update balances after mining the block
        self.update_balances(new_block)

        self.pending_transactions = []

    def update_balances(self, block):
        # Update balances for each transaction in the block
        for transaction in block.transactions:
            if transaction.sender in self.balances:
                self.balances[transaction.sender] -= transaction.amount
            else:
                self.balances[transaction.sender] = -transaction.amount

            if transaction.recipient in self.balances:
                self.balances[transaction.recipient] += transaction.amount
            else:
                self.balances[transaction.recipient] = transaction.amount

    def get_balance(self, address):
        # Return the balance for a given address (default to 0 if no balance exists)
        return self.balances.get(address, 0)

    def display_blockchain(self):
        for block in self.chain:
            print(f"Block {block.index}:")
            print(f"  Timestamp: {time.ctime(block.timestamp)}")
            print(f"  Transactions: {len(block.transactions)}")
            print(f"  Previous Hash: {block.previous_hash}")
            print(f"  Hash: {block.hash}")
            print(f"  Nonce: {block.nonce}\n")

def main():
    blockchain = Blockchain()

    # Add initial balances
    blockchain.balances["Alice"] = 1000
    blockchain.balances["Bob"] = 500
    blockchain.balances["Charlie"] = 300
    blockchain.balances["David"] = 200

    print("Initial Balances:")
    print(f"Alice: {blockchain.get_balance('Alice')}")
    print(f"Bob: {blockchain.get_balance('Bob')}")
    print(f"Charlie: {blockchain.get_balance('Charlie')}")
    print(f"David: {blockchain.get_balance('David')}\n")

    # Create and add some transactions
    blockchain.add_transaction(Transaction("Alice", "Bob", 50))
    blockchain.add_transaction(Transaction("Bob", "Charlie", 30))
    blockchain.add_transaction(Transaction("Charlie", "David", 20))
    blockchain.mine_pending_transactions()

    # Add more transactions
    blockchain.add_transaction(Transaction("Alice", "Charlie", 100))
    blockchain.add_transaction(Transaction("Bob", "David", 10))
    blockchain.mine_pending_transactions()

    blockchain.display_blockchain()

    # Check if the blockchain is valid
    print("Blockchain is valid:", blockchain.is_chain_valid())

    # Check balances after transactions
    print(f"Alice's balance: {blockchain.get_balance('Alice')}")
    print(f"Bob's balance: {blockchain.get_balance('Bob')}")
    print(f"Charlie’s balance: {blockchain.get_balance('Charlie')}")
    print(f"David’s balance: {blockchain.get_balance('David')}\n")

if __name__ == "__main__":
    main()
