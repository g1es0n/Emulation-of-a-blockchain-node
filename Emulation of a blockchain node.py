import json
from pathlib import Path
from hashlib import sha256


class Blockchain:
    def __init__(self, path, difficulty):
        self.path = path + "data.json"
        self.difficulty = difficulty
        self.block = {"data": '', "prevhash": '0000', "nonce": 0, "hash": ''}
        self.prevhash = "0000"

    def create_file(self):
        file_path = Path(self.path)
        if not (file_path.exists()):
            with open(self.path, "w") as _:
                pass
        else:
            with open(self.path, "r") as f:
                blocks = f.readlines()
                if len(blocks) != 0:
                    last_block = blocks[-1]
                    last_json = json.loads(last_block)
                    self.block["prevhash"] = last_json["hash"]

    def create_blockchain(self):
        start = self.difficulty * "0"
        while True:
            self.block["data"] = input("Введите данные: ")
            if len(self.block["data"]) == 0:
                break
            while True:
                self.block["hash"] = sha256(
                    (self.block["data"] + self.block["prevhash"] + str(self.block["nonce"])).encode()).hexdigest()
                if self.block["hash"].startswith(start):
                    break
                self.block["nonce"] += 1
            s = json.dumps(self.block)
            with open(self.path, "a") as f:
                f.write(s + "\n")
            self.block["prevhash"] = self.block["hash"]
            self.block["nonce"] = 0

    def check_blockchain(self):
        prevhash = '0000'
        number = 0
        with open(self.path, 'r') as f:
            for line in f:
                block = json.loads(line)
                if prevhash != block['prevhash']:
                    print(f'Invalid previous hash in block {number}')
                    exit()
                hash = sha256((block['data'] + prevhash + str(block["nonce"])).encode()).hexdigest()
                if hash != block['hash']:
                    print(f'Invalid hash in block {number}')
                    exit()
                print(f'Block {number} is OK')
                prevhash = hash
                number += 1


path = input("Введите путь к папке: ")
difficult = int(input("Введите сложность: "))
block = Blockchain(path=path, difficulty=difficult)
block.create_file()
block.check_blockchain()
block.create_blockchain()