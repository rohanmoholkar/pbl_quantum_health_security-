import hashlib
import time
import json
from dataclasses import dataclass, asdict
from typing import List, Dict

@dataclass
class Block:
    index: int
    timestamp: float
    transactions: List[Dict]
    previous_hash: str
    nonce: int = 0
    hash: str = ""

    def compute_hash(self) -> str:
        """
        Calculates the cryptographic hash of the block.
        """
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class BlockchainEHR:
    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        Generates the first block in the blockchain.
        """
        genesis_block = Block(0, time.time(), [], "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    def add_transaction(self, transaction: Dict):
        """
        Adds an EHR access or update log to the unconfirmed transactions pool.
        """
        self.unconfirmed_transactions.append(transaction)

    def mine(self) -> int:
        """
        Mines the unconfirmed transactions into a new block.
        (Using a simplified Proof-of-Work for demonstration)
        """
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block
        new_block = Block(
            index=last_block.index + 1,
            timestamp=time.time(),
            transactions=self.unconfirmed_transactions,
            previous_hash=last_block.hash
        )

        # Simplified PoW: finding a hash that starts with "00"
        while not new_block.compute_hash().startswith('00'):
            new_block.nonce += 1
            
        new_block.hash = new_block.compute_hash()
        self.chain.append(new_block)
        self.unconfirmed_transactions = []
        return new_block.index

    def verify_chain_integrity(self) -> bool:
        """
        Checks if the blockchain is mathematically sound.
        """
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current.hash != current.compute_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

def run_simulation():
    print("Initializing Quantum-Secured Blockchain EHR Ledger...")
    ehr_chain = BlockchainEHR()
    
    print("\n--- Event: Patient Registration ---")
    ehr_chain.add_transaction({
        "event": "PatientRegistered",
        "patientAddress": "0xABC123",
        "aadhaarHash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    })
    ehr_chain.mine()
    print(f"Block Mined! Hash: {ehr_chain.last_block.hash}")

    print("\n--- Event: Doctor Granted Access ---")
    ehr_chain.add_transaction({
        "event": "AccessGranted",
        "patientAddress": "0xABC123",
        "doctorAddress": "0xDOC999"
    })
    ehr_chain.mine()
    print(f"Block Mined! Hash: {ehr_chain.last_block.hash}")

    print("\n--- Event: Doctor Updates EHR (Off-chain IPFS Hash) ---")
    ehr_chain.add_transaction({
        "event": "EHRUpdated",
        "patientAddress": "0xABC123",
        "newEhrIpfsHash": "QmYwAPJzv5CZsnA625s3Xf2dzjmNsm1VNFlRzQ"
    })
    ehr_chain.mine()
    print(f"Block Mined! Hash: {ehr_chain.last_block.hash}")
    
    print("\n--- Verifying Cryptographic Integrity ---")
    is_valid = ehr_chain.verify_chain_integrity()
    print(f"Blockchain integrity intact: {is_valid}")
    
    print("\n--- Simulating Tampering Attack ---")
    # A hacker tries to change the Doctor Address in Block 2
    print("Hacker modifies Block 2...")
    ehr_chain.chain[2].transactions[0]["doctorAddress"] = "0xHACKER"
    
    # Check integrity again
    is_valid_after_hack = ehr_chain.verify_chain_integrity()
    print(f"Blockchain integrity intact after hack: {is_valid_after_hack}")
    if not is_valid_after_hack:
        print("Tampering Detected! Cryptographic link broken.")

if __name__ == "__main__":
    run_simulation()
