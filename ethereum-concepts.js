const crypto = require("crypto");

// --- 1. Hashing (Ethereum uses Keccak-256, we simulate with SHA-256) ---
function hash(data) {
  return crypto.createHash("sha256").update(JSON.stringify(data)).digest("hex");
}

// --- 2. Transaction ---
class Transaction {
  constructor(from, to, amount) {
    this.from = from;
    this.to = to;
    this.amount = amount;
    this.timestamp = Date.now();
    this.id = hash(this);
  }
}

// --- 3. Block (like an Ethereum block) ---
class Block {
  constructor(index, transactions, previousHash = "0") {
    this.index = index;
    this.timestamp = Date.now();
    this.transactions = transactions;
    this.previousHash = previousHash;
    this.nonce = 0;
    this.hash = this.calculateHash();
  }

  calculateHash() {
    return hash({
      index: this.index,
      timestamp: this.timestamp,
      transactions: this.transactions,
      previousHash: this.previousHash,
      nonce: this.nonce,
    });
  }

  // Proof of Work: find a hash starting with `difficulty` zeros
  mine(difficulty) {
    const target = "0".repeat(difficulty);
    while (!this.hash.startsWith(target)) {
      this.nonce++;
      this.hash = this.calculateHash();
    }
    console.log(`Block ${this.index} mined! Hash: ${this.hash}`);
  }
}

// --- 4. Blockchain ---
class Blockchain {
  constructor() {
    this.chain = [this.createGenesisBlock()];
    this.pendingTransactions = [];
    this.difficulty = 2; // low for demo speed
    this.miningReward = 2; // ETH reward for mining
    this.balances = {};
  }

  createGenesisBlock() {
    return new Block(0, [], "0000000000000000");
  }

  getLatestBlock() {
    return this.chain[this.chain.length - 1];
  }

  addTransaction(tx) {
    if (!tx.from || !tx.to) throw new Error("Transaction must have from/to");
    const senderBalance = this.balances[tx.from] || 0;
    if (tx.from !== "NETWORK" && senderBalance < tx.amount) {
      throw new Error(`Insufficient balance: ${tx.from} has ${senderBalance} ETH`);
    }
    this.pendingTransactions.push(tx);
    console.log(`  TX queued: ${tx.from} -> ${tx.to} | ${tx.amount} ETH`);
  }

  minePendingTransactions(minerAddress) {
    // Reward transaction for the miner
    const rewardTx = new Transaction("NETWORK", minerAddress, this.miningReward);
    this.pendingTransactions.push(rewardTx);

    const block = new Block(
      this.chain.length,
      this.pendingTransactions,
      this.getLatestBlock().hash
    );
    block.mine(this.difficulty);

    // Apply balances
    for (const tx of block.transactions) {
      if (tx.from !== "NETWORK") {
        this.balances[tx.from] = (this.balances[tx.from] || 0) - tx.amount;
      }
      this.balances[tx.to] = (this.balances[tx.to] || 0) + tx.amount;
    }

    this.chain.push(block);
    this.pendingTransactions = [];
  }

  isChainValid() {
    for (let i = 1; i < this.chain.length; i++) {
      const current = this.chain[i];
      const previous = this.chain[i - 1];

      if (current.hash !== current.calculateHash()) return false;
      if (current.previousHash !== previous.hash) return false;
    }
    return true;
  }

  getBalance(address) {
    return this.balances[address] || 0;
  }
}

// --- 5. Simple Smart Contract simulation ---
class SimpleToken {
  constructor(name, symbol, initialSupply, owner) {
    this.name = name;
    this.symbol = symbol;
    this.balances = { [owner]: initialSupply };
    this.totalSupply = initialSupply;
    console.log(`\n[Contract] ${name} (${symbol}) deployed. Supply: ${initialSupply}`);
  }

  transfer(from, to, amount) {
    if ((this.balances[from] || 0) < amount) throw new Error("Insufficient token balance");
    this.balances[from] -= amount;
    this.balances[to] = (this.balances[to] || 0) + amount;
    console.log(`[Contract] ${from} -> ${to}: ${amount} ${this.symbol}`);
  }

  balanceOf(address) {
    return this.balances[address] || 0;
  }
}

// ============================================================
// DEMO
// ============================================================
console.log("=== Ethereum Concepts Demo ===\n");

const chain = new Blockchain();

// Seed some initial balances (like a faucet)
chain.balances["Alice"] = 10;
chain.balances["Bob"] = 5;

console.log("-- Block 1: Alice sends ETH to Bob --");
chain.addTransaction(new Transaction("Alice", "Bob", 3));
chain.addTransaction(new Transaction("Bob", "Alice", 1));
chain.minePendingTransactions("Miner1");

console.log("\n-- Block 2: Bob sends ETH to Charlie --");
chain.addTransaction(new Transaction("Bob", "Charlie", 2));
chain.minePendingTransactions("Miner1");

console.log("\n-- Balances --");
["Alice", "Bob", "Charlie", "Miner1"].forEach((addr) => {
  console.log(`  ${addr}: ${chain.getBalance(addr)} ETH`);
});

console.log("\n-- Chain Valid?", chain.isChainValid());

console.log("\n-- Tamper with chain --");
chain.chain[1].transactions[0].amount = 999; // hack attempt
console.log("-- Chain Valid after tampering?", chain.isChainValid());

// Smart contract demo
const token = new SimpleToken("DemoToken", "DMT", 1000, "Alice");
token.transfer("Alice", "Bob", 200);
token.transfer("Bob", "Charlie", 50);
console.log(`\n[Contract] Balances:`);
["Alice", "Bob", "Charlie"].forEach((addr) => {
  console.log(`  ${addr}: ${token.balanceOf(addr)} DMT`);
});
