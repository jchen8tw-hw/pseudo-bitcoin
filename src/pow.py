from utils import sum256, encode
import sys


class Pow(object):
    def __init__(self, block):
        self._block = block
        self._target = 1 << (256 - block.bits)

    def _init_data(self, nonce):
        block = self._block
        self.data_ls = [block.prev_block_hash,
                        block.data,
                        block.timestamp,
                        str(self._target),
                        str(nonce)]
        return ''.join(self.data_ls)

    def validate(self):
        data = self._init_data(self._block.nonce)
        hash_int = int(sum256(data), 16)
        return True if hash_int < self._target else False

    def mine(self):
        nonce = 0
        print("Mining the block containing \'%s\'" % (self._block.data))
        while True:
            data = self._init_data(nonce)
            hash_str = sum256(data)
            #sys.stdout.write("%s \r" % (hash_str))           
            hash_int = int(hash_str, 16)
            #sys.stdout.write("%d \r" %(hash_int))            
            if hash_int < self._target:
                break
            else:
                nonce += 1
        print("Mined!\nhash: %s" % hash_str)
        return nonce, hash_str
