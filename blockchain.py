import hashlib
import json
import time
import random
from collections import OrderedDict

class Block:
    def __init__(self, index, previous_hash, transactions, validator, timestamp=None):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.validator = validator  # Validator who created this block
        self.timestamp = timestamp or time.time()
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_data = json.dumps(
            OrderedDict({
                "index": self.index,
                "previous_hash": self.previous_hash,
                "transactions": self.transactions,
                "validator": self.validator,
                "timestamp": self.timestamp
            }),
            sort_keys=True
        )
        return hashlib.sha256(block_data.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.stakeholders = {}  # Stores users and their staked tokens
        self.validators = []  # List of chosen validators
        self.create_genesis_block()
    
    def create_genesis_block(self):
        genesis_block = Block(0, "0", [], "Genesis")
        self.chain.append(genesis_block)

    def stake_tokens(self, user, amount):
        """ Users stake tokens to be eligible as validators """
        if user in self.stakeholders:
            self.stakeholders[user] += amount
        else:
            self.stakeholders[user] = amount
        print(f"{user} has staked {amount} tokens.")

    def select_validators(self):
        """ Validators are chosen based on the stake (higher stake = higher chance) """
        weighted_pool = []
        for user, stake in self.stakeholders.items():
            weighted_pool.extend([user] * stake)  # More stake = more chances
        self.validators = random.sample(weighted_pool, min(3, len(weighted_pool)))  # Select 3 validators
        print(f"Selected validators: {self.validators}")

    def add_block(self, transactions):
        """ Block is created by a randomly selected validator """
        last_block = self.chain[-1]
        validator = random.choice(self.validators)  # Randomly select from validators
        new_block = Block(len(self.chain), last_block.hash, transactions, validator)
        self.chain.append(new_block)
        print(f"Block {new_block.index} added by validator {validator}")

    def apply_penalty(self, validator):
        """ Penalty for malicious validators (Slashing mechanism) """
        if validator in self.stakeholders:
            self.stakeholders[validator] //= 2  # Slash half of the stake
            print(f"{validator} was penalized! New stake: {self.stakeholders[validator]}")

    def distribute_rewards(self):
        """ Reward validators for validating transactions """
        reward = 10  # Fixed reward per block
        for validator in self.validators:
            if validator in self.stakeholders:
                self.stakeholders[validator] += reward
            else:
                self.stakeholders[validator] = reward
            print(f"{validator} received {reward} tokens as a reward.")

    def print_chain(self):
        for block in self.chain:
            print(f"Index: {block.index}, Hash: {block.hash}, Prev Hash: {block.previous_hash}, Transactions: {block.transactions}, Validator: {block.validator}")

if __name__ == "__main__":
    blockchain = Blockchain()
    
    # Staking process
    blockchain.stake_tokens("Alice", 50)
    blockchain.stake_tokens("Bob", 30)
    blockchain.stake_tokens("Charlie", 20)
    
    blockchain.select_validators()
    
    # Adding blocks
    blockchain.add_block(["Alice pays Bob 5 BTC"])
    blockchain.add_block(["Bob pays Charlie 2 BTC"])
    
    # Apply penalties and rewards
    blockchain.apply_penalty("Bob")  # Suppose Bob acted maliciously
    blockchain.distribute_rewards()
    
    # Print the blockchain
    blockchain.print_chain()
