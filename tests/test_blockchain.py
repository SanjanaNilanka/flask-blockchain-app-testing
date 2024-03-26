import unittest
from unittest.mock import patch
from blockchain import get_hash, write_block, get_POW, check_blocks_integrity, get_next_block, check_block, is_valid_proof
import hashlib
import json
import os
from time import time

BLOCKCHAIN_DIR = os.curdir + "/blocks/"

class BlockchainTest(unittest.TestCase):
    def test_check_blocks_integrity(self):
        next_block1 = int(get_next_block())
        write_block("Test data 1")
        next_block2 = int(get_next_block())
        write_block("Test data 2")
        results = check_blocks_integrity()
        for result in results:
            self.assertEqual(result['result'], 'ok')
            
        os.remove(f"{BLOCKCHAIN_DIR}{next_block1}.json")
        os.remove(f"{BLOCKCHAIN_DIR}{next_block2}.json")
        
    def test_check_block(self):
        write_block("Test data")
        result = check_block(2)
        self.assertEqual(result['result'], 'ok')
        os.remove(f"{BLOCKCHAIN_DIR}{int(get_next_block())-1}.json")
        
    def test_get_POW(self):
        next_block = int(get_next_block())
        write_block("Test data")
        get_POW(next_block)
        file_path = f"{BLOCKCHAIN_DIR}{next_block}.json"
        with open(file_path, "r") as file:
            data = json.load(file)
            self.assertTrue(data["proof"] >= 0)
        
        os.remove(f"{BLOCKCHAIN_DIR}{next_block}.json")
        
    def test_is_valid_proof(self):
        last_proof = 1234
        proof = 0
        difficulty = 2
        while is_valid_proof(last_proof, proof, difficulty) is False:
            proof += 1
        self.assertTrue(is_valid_proof(last_proof, proof, difficulty))
    
    def test_get_hash(self):
        # Create a temporary block file for testing
        block_data = {
            "text": "Test data",
            "prev_hash": "previous_hash_value",
            "timestamp": 123456789,
            "proof": 123,
            "index": "1"
        }
        with open(f"{BLOCKCHAIN_DIR}test_block.json", "w") as file:
            file.write(json.dumps(block_data))

        # Calculate the hash using the get_hash function
        calculated_hash = get_hash("test_block.json")

        # Manually calculate the expected hash for the test block
        expected_hash = hashlib.sha256(json.dumps(block_data).encode()).hexdigest()

        # Assert that the calculated hash matches the expected hash
        self.assertEqual(calculated_hash, expected_hash)

        # Clean up: remove the temporary block file
        os.remove(f"{BLOCKCHAIN_DIR}test_block.json")
        
    def test_get_next_block(self):
        next_block = int(get_next_block())
        self.assertEqual(next_block, 2)  # Assuming initial block index is 1
   
    def test_write_block(self):
        text = "Test data"
        next_block = int(get_next_block())
        write_block(text)
        
        file_path = f"{BLOCKCHAIN_DIR}{next_block}.json"
        self.assertTrue(os.path.exists(file_path))
        with open(file_path, "r") as file:
            data = json.load(file)
            self.assertEqual(data["text"], text)
            
        os.remove(f"{BLOCKCHAIN_DIR}{next_block}.json")
    

if __name__ == "__main__":
    unittest.main()
