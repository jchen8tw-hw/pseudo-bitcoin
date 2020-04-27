from blockchain import Blockchain
from pow import Pow
import pickle

if __name__ == '__main__':
    try:
        f = open("../blocks/blockchain.pkl","rb")
        bc = pickle.load(f)
        f.close()
        print("loaded data")
        bc.add_block("block %s" % str(len(bc.blocks)))
    except:
        bc = Blockchain(12)   
        bc.add_block("block 1")
        bc.add_block("block 2")

    for block in bc.blocks:
        print("Prev hash: %s" %(block.prev_block_hash))
        print("Data: %s" % (block.data))
        print("Hash: %s" %(block.hash))
        pw = Pow(block)
        print("PoW: %s" %(pw.validate()))
    f = open("../blocks/blockchain.pkl","wb+")
    pickle.dump(bc,f)
    f.close()
