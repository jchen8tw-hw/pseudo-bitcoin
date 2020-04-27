from block import Block

class Blockchain(object):
    def __init__(self,difficulty=24):
        block = Block(bits=difficulty)
        self._blocks = [block.pow_of_block()]
        self._bits = difficulty
    
    def add_block(self, data):
        prev_block_hash = self._blocks[-1].hash
        block = Block(data,prev_block_hash,len(self._blocks)+1,self._bits)
        self._blocks.append(block.pow_of_block())
    
    @property
    def blocks(self):
        return self._blocks

    @property
    def difficulty(self):
        return self._bits