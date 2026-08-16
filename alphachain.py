import hashlib, time, json, os

REWARD = 10
DIFFICULTY = 3

class Transaction:
    def __init__(self, sender, receiver, amount, data=""):
        self.sender, self.receiver, self.amount, self.data = sender, receiver, amount, data
    def to_dict(self): return self.__dict__

class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index, self.timestamp, self.transactions = index, time.time(), transactions
        self.previous_hash, self.nonce, self.miner = previous_hash, 0, "Unknown"
        self.hash = self.calc_hash()
    def calc_hash(self):
        block_string = json.dumps({"index":self.index,"timestamp":self.timestamp,
            "transactions":[t.to_dict() for t in self.transactions],
            "previous_hash":self.previous_hash,"nonce":self.nonce,"miner":self.miner}, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    def mine(self, difficulty, miner_name):
        self.miner = miner_name
        target = '0' * difficulty
        while self.hash[:difficulty]!= target: self.nonce += 1; self.hash = self.calc_hash()
    def to_dict(self):
        d = self.__dict__.copy(); d['transactions'] = [t.to_dict() for t in self.transactions]; return d

class Alphachain:
    def __init__(self, node_name="Rodrigo", filename="alphachain.json"):
        self.filename, self.node_name = filename, node_name
        self.chain, self.mempool = self.load_chain(), []

    def get_balance(self, address):
        balance = 0
        for block in self.chain:
            for tx in block.transactions:
                if tx.receiver == address: balance += tx.amount
                if tx.sender == address: balance -= tx.amount
        return balance

    def add_transaction(self, sender, receiver, amount, data=""):
        self.mempool.append(Transaction(sender, receiver, amount, data))

    def mine_block(self):
        self.mempool.append(Transaction("ALPHACHAIN", self.node_name, REWARD, "Block Reward"))
        new_block = Block(len(self.chain), self.mempool, self.chain[-1].hash)
        new_block.mine(DIFFICULTY, self.node_name)
        self.chain.append(new_block); self.mempool = []; self.save_chain()
        print(f"Bloque {new_block.index} minado por {self.node_name}")
        return new_block.to_dict()

    def load_chain(self):
        if os.path.exists(self.filename):
            with open(self.filename) as f: data = json.load(f)
            chain = []
            for b in data:
                txs = [Transaction(**t) for t in b['transactions']]
                block = Block(b['index'], txs, b['previous_hash'])
                block.__dict__.update({k:v for k,v in b.items() if k!='transactions'})
                chain.append(block)
            return chain
        genesis = Block(0, [Transaction("Genesis", "Rodrigo", 100, "Airdrop")], "0")
        genesis.hash = "0"*64; return [genesis]

    def save_chain(self):
        with open(self.filename, 'w') as f: json.dump([b.to_dict() for b in self.chain], f, indent=2)

    def validate_chain(self):
        for i in range(1, len(self.chain)):
            if self.chain[i].hash!= self.chain[i].calc_hash(): return False
            if self.chain[i].previous_hash!= self.chain[i-1].hash: return False
        return True

if __name__ == "__main__":
    bc = Alphachain()
    bc.add_transaction("Rodrigo", "Ciencia", 0, "Prediccion: GLIMPSE-17775 dim 3x-5x antes Ago 2027 | Paper SHA256: TBD")
    bc.mine_block()
    print(f"Balance: {bc.get_balance('Rodrigo')} ALPHA | Valida: {bc.validate_chain()}")
