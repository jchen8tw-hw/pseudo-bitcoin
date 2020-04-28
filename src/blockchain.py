from block import Block
from transaction import CoinbaseTx
from collections import defaultdict


class Blockchain(object):
    def __init__(self, address=None, difficulty=24):
        self._bits = difficulty
        self._blocks = [
            Block([CoinbaseTx(address, 'genesis block').set_id()], bits=difficulty).pow_of_block()]

    def MineBlock(self, transaction_lst):
        last_hash = self.blocks[-1].hash
        cur_height = int(self.blocks[-1].height)
        new_block = Block(transaction_lst,
                          prev_block_hash=last_hash, bits=self._bits, height=cur_height+1).pow_of_block()
        self._blocks.append(new_block)

    def find_unspent_txs(self, address):
        spent_txo = defaultdict(list)
        unspent_txs = []

        #reverse from the latest block
        for block in self._blocks[::-1]:
            for tx in block.transactions:
                if not isinstance(tx, CoinbaseTx):
                    for vin in tx.vin:
                        if vin.valid_sig(address):
                            tx_id = vin.tx_id
                            spent_txo[tx_id].append(vin.vout)
                tx_id = tx.ID
                spent = False
                for idx, out in enumerate(tx.vout):
                    if spent_txo[tx_id]:
                        for spent_out in spent_txo[tx_id]:
                            if spent_out == idx:
                                spent = True
                                break
                    if spent is True:
                        break
                    if out.valid_pubkey(address):
                        unspent_txs.append(tx)
        return unspent_txs

    def find_spendable_outputs(self, address, amount):
        accumulated = 0
        unspent_outputs = defaultdict(list)
        unspent_txs = self.find_unspent_txs(address)
        found = False
        for tx in unspent_txs:
            tx_id = tx.ID
            for out_idx, out in enumerate(tx.vout):
                if out.valid_pubkey(address) and accumulated < amount:
                    accumulated += out.value
                    unspent_outputs[tx_id].append(out_idx)

                    if accumulated >= amount:
                        found = True
                        break
            if found is True:
                break

        return accumulated, unspent_outputs

    def find_utxo(self, address=None):
        utxos = []
        unspent_txs = self.find_unspent_txs(address)

        for tx in unspent_txs:
            for out in tx.vout:
                if out.valid_pubkey(address):
                    utxos.append(out)

        return utxos

    @property
    def blocks(self):
        return self._blocks

    @property
    def difficulty(self):
        return self._bits
