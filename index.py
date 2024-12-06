import hashlib
import time
import json
import os
import pickle
from collections import defaultdict

class Transaction:
    def __init__(self, sender, recipient, amount, signature=None):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = time.time()
        self.signature = signature  # digital signature for authentication

    def to_dict(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "signature": self.signature,
        }

    def sign_transaction(self, private_key):
        # simulating signing with private key (stub for cryptography library)
        self.signature = hashlib.sha256((self.sender + self.recipient + str(self.amount)).encode()).hexdigest()

class Block:
    def __init__(self, index, timestamp, transactions, previous_hash, miner_address):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
        self.miner_address = miner_address  # miner on the block

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
        self.chain = self.load_chain()
        if not self.chain:
            self.chain = [self.create_genesis_block()]
        self.difficulty = 4
        self.pending_transactions = []
        self.transaction_pool_limit = 10
        self.balances = defaultdict(int) 
        self.mining_reward = 50  # reward for mining a block is (50 of the current)

    def create_genesis_block(self):
        return Block(0, time.time(), [], "0", "GenesisMiner")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.save_chain()

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
        sender_balance = self.get_balance(transaction.sender)
        if sender_balance < transaction.amount:
            print(f"Transaction from {transaction.sender} failed: Insufficient balance.")
            return False

        # insurin for no duplicates
        for t in self.pending_transactions:
            if t.to_dict() == transaction.to_dict():
                print(f"Transaction {transaction} is already in the pool.")
                return False

        self.pending_transactions.append(transaction)
        print(f"Transaction from {transaction.sender} to {transaction.recipient} added to pool.")
        return True

    def mine_pending_transactions(self, miner_address):
        if not self.pending_transactions:
            print("No transactions to mine.")
            return

        # mining reward implimatation added here
        reward_transaction = Transaction("Network", miner_address, self.mining_reward)
        self.pending_transactions.append(reward_transaction)

        new_block = Block(
            len(self.chain),
            time.time(),
            self.pending_transactions,
            self.get_latest_block().hash,
            miner_address,
        )

        print(f"Mining block {new_block.index}...")
        self.add_block(new_block)

        # assigningnew reward in balance after mining the block
        self.update_balances(new_block)
        self.pending_transactions = []

    def update_balances(self, block):
        for transaction in block.transactions:
            if transaction.sender != "Network":
                self.balances[transaction.sender] -= transaction.amount
            self.balances[transaction.recipient] += transaction.amount

    def get_balance(self, address):
        return self.balances[address]

    def save_chain(self):
        with open("blockchain_data.pkl", "wb") as file:
            pickle.dump(self.chain, file)

    def load_chain(self):
        if os.path.exists("blockchain_data.pkl"):
            with open("blockchain_data.pkl", "rb") as file:
                return pickle.load(file)
        return None

    def display_blockchain(self):
        for block in self.chain:
            print(f"Block {block.index}:")
            print(f"  Timestamp: {time.ctime(block.timestamp)}")
            print(f"  Transactions: {len(block.transactions)}")
            print(f"  Previous Hash: {block.previous_hash}")
            print(f"  Hash: {block.hash}")
            print(f"  Nonce: {block.nonce}")
            print(f"  Mined by: {block.miner_address}\n")

def main():
    blockchain = Blockchain()

    blockchain.balances["Alice"] = 1000
    blockchain.balances["Bob"] = 500
    blockchain.balances["Charlie"] = 300
    blockchain.balances["Miner"] = 0

    print("Initial Balances:")
    for user in blockchain.balances:
        print(f"{user}: {blockchain.get_balance(user)}")
    print()

    blockchain.add_transaction(Transaction("Alice", "Bob", 100))
    blockchain.add_transaction(Transaction("Bob", "Charlie", 50))
    blockchain.mine_pending_transactions("Miner")

    blockchain.add_transaction(Transaction("Alice", "Charlie", 200))
    blockchain.mine_pending_transactions("Miner")

    blockchain.display_blockchain()

    print("Final Balances:")
    for user in blockchain.balances:
        print(f"{user}: {blockchain.get_balance(user)}")

if __name__ == "__main__":
    main()
