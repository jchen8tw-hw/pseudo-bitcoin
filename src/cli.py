import argparse
from blockchain import Blockchain
from pow import Pow
import pickle


def new_parser():
    parser = argparse.ArgumentParser()
    sub_parser = parser.add_subparsers(help="commands")
    print_parser = sub_parser.add_parser('print')
    print_parser.add_argument('--print', dest='print', action='store_true')
    print_parser.add_argument(
        '--height', dest='print_height', action='store_true')
    add_parser = sub_parser.add_parser("addblock")
    add_parser.add_argument("--transaction", type=str, dest='add_data')
    return parser


def add_block(bc, data):
    if (type(data) == str and data != ''):
        bc.add_block(data)
        print("added")
    else:
        print("invalid input")


def print_chain(bc):
    for block in bc.blocks:
        print("Prev hash: %s" % (block.prev_block_hash))
        print("Data: %s" % (block.data))
        print("Hash: %s" % (block.hash))
        pw = Pow(block)
        print("PoW: %s" % (pw.validate()))


def print_height(bc):
    print(bc.blocks[-1].height)


if __name__ == '__main__':
    parser = new_parser()
    args = vars(parser.parse_args())
    try:
        f = open("../blocks/blockchain.pkl", "rb")
        bc = pickle.load(f)
        f.close()
        print("loaded data")
    except:
        bc = Blockchain(12)

    if args.get('print') is True:
        print_chain(bc)
    if args.get('print_height') is True:
        print_height(bc)
    if args.get('add_data') is not None:
        add_block(bc, args.get('add_data'))

    f = open("../blocks/blockchain.pkl", "wb+")
    pickle.dump(bc, f)
    f.close()
