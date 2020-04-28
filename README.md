# Pseudo Bitcoin

## Prerequisites
- Python3
- nothing else

## Implemented Feature
- [x] Block
- [x] Blockchain
- [x] Pow
- [x] Persistance
- [x] UTXO model transactions
- [x] CLI

## Usage
```python
#help
python cli.py --help
#create genesis block
python cli.py createblockchain –-address { YOUR_NAME }
#getbalance
python cli.py getbalance --address { ADDRESS }
#send transaction
python cli.py send -–from { NAME1} -–to { NAME2} –amount { HOW_MUCH }
#print blocks information
python cli.py print [--height --print]
#print one block
python cli.py printblock --pheight {BLOCK_HEIGHT}
```

