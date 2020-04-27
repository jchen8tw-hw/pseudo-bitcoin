from block import Block
from transaction import CoinbaseTx


class Blockchain(object):
    def __init__(self, address=None, difficulty=24):
        self._bits = difficulty
        self._blocks = [
            Block([CoinbaseTx(address, 'genesis block').set_id()], bits=difficulty).pow_of_block()]

    def MineBlock(self, transaction_lst):
        last_hash = self.blocks[-1].hash
        cur_height = self.blocks[-1].height
        new_block = Block(transaction_lst,
                          prev_block_hash=last_hash, bits=self._bits, height=cur_height+1).pow_of_block()
        self._blocks.append(new_block)
    
    def find_utxo(self,address=None):
        utxos = []
        unspent_txs = self.find_unspent_txs(address)
        pass
    
    def find_unspent_txs(self,address):
        spent_txo = {}
        unspent_txs = []

        for block in self._blocks:
            for tx

    @property
    def blocks(self):
        return self._blocks

    @property
    def difficulty(self):
        return self._bits
