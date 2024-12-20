# Blockchain Project README

## Overview

This Blockchain project is a simplified implementation of a blockchain system in Python. It includes core features such as block mining, transaction validation, and a reward system for miners. The blockchain is persistent, ensuring data is saved and loaded across sessions.

---

## Features

1. **Genesis Block**:
   - The blockchain starts with a genesis block.

2. **Block Mining**:
   - Proof-of-Work mining with adjustable difficulty.
   - Mining rewards for adding blocks to the chain.

3. **Transactions**:
   - Transactions are validated for sufficient balance before being added.
   - Each transaction can include a digital signature (placeholder implementation).

4. **Balances**:
   - Dynamic balance management for each user in the system.

5. **Persistence**:
   - The blockchain is saved to a file and reloaded when the program starts.

6. **Security**:
   - Chain validation to ensure data integrity.
   - Tamper-proof block hashing with Proof-of-Work.

7. **Console Output**:
   - Display of all blocks and transactions.
   - User-friendly messages for operations.

---

## Requirements

- **Python 3.8+**
- No external dependencies are required, but you can install cryptography libraries to enhance the digital signature functionality.

---

## How to Use

1. **Clone or Download the Repository**:
   ```bash
   git clone git@github.com:asimwe1/py-chain
   cd py-chain
   ```

2. **Run the Program**:
   - Execute the program in your terminal:
     ```bash
     python3 blockchain.py
     ```

3. **Interact with the Blockchain**:
   - The program demonstrates adding transactions, mining blocks, and displaying the blockchain.

---

## Code Structure

- `Transaction`:
  - Represents a transaction between a sender and recipient.

- `Block`:
  - Stores transactions, timestamps, and hash values.
  - Handles mining with a proof-of-work algorithm.

- `Blockchain`:
  - Core functionality of the blockchain system.
  - Manages blocks, transactions, balances, and persistence.

- `main()`:
  - Entry point for the program.
  - Contains examples of how to interact with the blockchain.

---

## Sample Output

- **Initial Balances**:
  ```
  Initial Balances:
  Alice: 1000
  Bob: 500
  Charlie: 300
  Miner: 0
  ```

- **Mining a Block**:
  ```
  Mining block 1...
  Block mined successfully!
  ```

- **Displaying Blockchain**:
  ```
  Block 1:
    Timestamp: Mon Dec 6 12:00:00 2024
    Transactions: 3
    Previous Hash: 0
    Hash: 0000abc123def456
    Nonce: 123456
    Mined by: Miner
  ```

- **Final Balances**:
  ```
  Final Balances:
  Alice: 800
  Bob: 550
  Charlie: 550
  Miner: 100
  ```

---

## Next Steps

1. **Enhance Digital Signatures**:
   - Replace placeholder signatures with a cryptography library like `cryptography` or `PyCryptodome`.

2. **Add Network Support**:
   - Implement peer-to-peer networking to simulate a decentralized blockchain.

3. **Improve User Interface**:
   - Upgrade from a terminal-based UI to a GUI using frameworks like **Tkinter** or **PyQt**.

4. **Smart Contracts**:
   - Introduce a framework for running smart contracts on the blockchain.

---

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your improvements.

---

## License

This project is open-source and available under the [MIT License](https://opensource.org/licenses/MIT).

---

## Author

**Asimwe Landry**  
- GitHub: [@asimwe1](https://github.com/asimwe1)  
- LinkedIn: [linkedin.com/in/asimwe-landry](https://linkedin.com/in/asimwe-landry)  

---
