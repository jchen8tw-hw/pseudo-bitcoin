from utils import *
import pickle
from abc import abstractclassmethod


class TxInput(object):

    def __init__(self, txid, vout, sig):
        self._tx_id = encode(txid)
        self._vout = vout
        self._script_sig = sig

    def __repr__(self):
        return 'TXInput(tx_id={0!r}, vout={1!r}, script_sig={2!r})'.format(
            self._tx_id, self._vout, self._script_sig)

    def valid_sig(self, sig):
        return self._script_sig == sig

    @property
    def tx_id(self):
        return self._tx_id

    @property
    def vout(self):
        return self._vout


class TxOutput(object):

    reward = 10

    def __init__(self, value, pubkey):
        self._value = value
        self.script_pubkey = pubkey

    def __repr__(self):
        return 'TXOutput(value={0!r}, script_pubkey={1!r})'.format(
            self._value, self.script_pubkey)

    def valid_pubkey(self, pubkey):
        return self.script_pubkey == pubkey

    @property
    def value(self):
        return self._value


class Transaction(object):
    def __init__(self):
        self._id = None
        self._vin = None
        self._vout = None

    @property
    def ID(self):
        return self._id

    @property
    def vin(self):
        return self._vin

    @property
    def vout(self):
        return self._vout

    def set_id(self):
        self._id = sum256(pickle.dumps(self))
        return self

    @abstractclassmethod
    def tx_type(self):
        return NotImplemented


class CoinbaseTx(Transaction):
    def __init__(self, to, data=None):
        if not data:
            data = 'Reward to {0}'.format(to)

        self._id = None
        self._vin = [TxInput('', -1, data)]
        self._vout = [TxOutput(TxOutput.reward, to)]

    def __repr__(self):
        return 'CoinbaseTx(id={0!r}, vin={1!r}, vout={2!r})'.format(
            self._id, self._vin, self._vout)
    
    def tx_type(self):
        return u'Coinbase'

class UTXOTx(Transaction):
    def __init__(self,from_addr,to_addr,amount,bc)
