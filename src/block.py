import time
from utils import sum256, encode, decode
from pow import Pow


class Block(object):
    def __init__(self,transaction_list, prev_block_hash='', height=1, bits=24):
        self._timestamp = encode(str(int(time.time())))
        self._height = height
        self._prev_block_hash = encode(prev_block_hash)
        self._bits = bits
        self._nonce = None
        self._hash = None
        self._tx_list = transaction_list

    def pow_of_block(self):
        pw = Pow(self)
        self._nonce, self._hash = pw.mine()
        self._hash = encode(self._hash)
        return self
    def hash_transactions(self):
        tx_hashes = []

        for tx in self._tx_list:
            tx_hashes.append(tx.ID)
        return sum256(encode(''.join(tx_hashes)))

    @property
    def hash(self):
        return decode(self._hash)

    @property
    def prev_block_hash(self):
        return decode(self._prev_block_hash)

    @property
    def timestamp(self):
        return str(self._timestamp)

    @property
    def nonce(self):
        return str(self._nonce)

    @property
    def bits(self):
        return self._bits


    @property
    def height(self):
        return str(self._height)

    @property
    def transactions(self):
        return self._tx_list
    
