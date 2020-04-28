import argparse
from blockchain import Blockchain
from pow import Pow
import pickle
import sys
from transaction import UTXOTx


def new_parser():
    parser = argparse.ArgumentParser()
    sub_parser = parser.add_subparsers(help="commands")
    print_parser = sub_parser.add_parser('print')
    print_parser.add_argument('--print', dest='print', action='store_true')
    print_parser.add_argument(
        '--height', dest='print_height', action='store_true')
    print_block_parser = sub_parser.add_parser('printblock')
    print_block_parser.add_argument(
        '--pheight', dest='print_height', type=int)
    balance_parser = sub_parser.add_parser('getbalance')
    balance_parser.add_argument(
        '--address', type=str, dest='balance_address', help='ADDRESS of balance')

    bc_parser = sub_parser.add_parser(
        'createblockchain', help='Create a blockchain and send genesis block reward to ADDRESS')
    bc_parser.add_argument(
        '--address', type=str, dest='blockchain_address', help='ADDRESS')

    send_parser = sub_parser.add_parser(
        'send', help='Send AMOUNT of coins from FROM address to TO')
    send_parser.add_argument(
        '--from', type=str, dest='send_from', help='FROM')
    send_parser.add_argument(
        '--to', type=str, dest='send_to', help='TO')
    send_parser.add_argument(
        '--amount', type=int, dest='send_amount', help='AMOUNT')
    return parser


def get_balance(address, bc):

    balance = 0
    UTXOs = bc.find_utxo(address)

    for out in UTXOs:
        balance += out.value

    print('Balance of {0}: {1}'.format(address, balance))


def create_blockchain(address):
    bc = Blockchain(address, difficulty=12)
    f = open("../blocks/blockchain.pkl", "wb")
    pickle.dump(bc, f)
    f.close()
    print('Done!')


def print_chain(bc):
    for block in bc.blocks:
        print("Prev hash: %s" % (block.prev_block_hash))
        #print("Data: %s" % (block.data))
        print("Hash: %s" % (block.hash))
        pw = Pow(block)
        print("Transactions: %s" % block.transactions[0])
        print("PoW: %s" % (pw.validate()))


def print_block(bc, height):
    block = bc.blocks[height - 1]
    print("Prev hash: %s" % (block.prev_block_hash))
    #print("Data: %s" % (block.data))
    print("Hash: %s" % (block.hash))
    pw = Pow(block)
    print("Transactions: %s" % block.transactions[0])
    print("PoW: %s" % (pw.validate()))


def send(from_addr, to_addr, amount, bc):

    tx = UTXOTx(from_addr, to_addr, amount, bc).set_id()
    bc.MineBlock([tx])
    print('Success!')


def print_height(bc):
    print(bc.blocks[-1].height)


if __name__ == '__main__':
    parser = new_parser()
    args = vars(parser.parse_args())
    bc = None
    if args.get('blockchain_address') is not None:
        create_blockchain(args.get('blockchain_address'))

    try:
        f = open("../blocks/blockchain.pkl", "rb")
        bc = pickle.load(f)
        f.close()
        #print("loaded data")
    except:
        print("create blockchain first!")
        sys.exit()
    if args.get('print_height') is not None:
        try:
            print_block(bc, args.get('print_height'))
        except IndexError:
            print('height out of range max(%s)' % (bc.blocks[-1].height))
    if args.get('print') is True:
        print_chain(bc)
    if args.get('print_height') is True:
        print_height(bc)
    if args.get('balance_address') is not None:
        get_balance(args.get('balance_address'), bc)

    if args.get('send_from') is not None and \
            args.get('send_to') is not None and \
            args.get('send_amount') is not None:
        send(args.get('send_from'), args.get(
            'send_to'), args.get('send_amount'), bc)

    f = open("../blocks/blockchain.pkl", "wb")
    pickle.dump(bc, f)
    f.close()
