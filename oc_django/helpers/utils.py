import datetime
import re

import eth_abi
from django.utils import timezone
from eth_typing import HexStr
from hexbytes import HexBytes
from web3 import Web3


def bn_to_number(num: int, precision=18) -> float:
    """
    BigNumber to number
    """
    return num / 10 ** precision


def batch_hex_bytes_to_string(arr: [HexBytes]) -> [str]:
    """
    batch convert hex to string
    """
    _strs: [str] = []
    for i in range(0, len(arr)):
        _strs.append(arr[i].hex())

    return _strs


def hex_to_dec(_hex) -> int:
    """
    hex convert to dec
    """
    if _hex == '':
        return 0
    return int(_hex, 16)


def check_network_name(network: str) -> (bool, str):
    """
    checking if network is right
    """
    networks = ['kovan', 'goerli', 'mainnet']
    return network in networks, 'network is only %s' % ', '.join(networks)


def get_datetime_now() -> datetime:
    """
    get now time
    """
    return timezone.now()


def to_hex(_str: str) -> HexStr:

    _hex = HexStr(_str)
    # _hex = eth_utils.to_hex(_str)
    return _hex


def to_bytes(_str: str) -> bytes:
    _bytes = Web3.toBytes(hexstr=_str)
    return _bytes


def get_prix_hash(_str: str, left=10) -> str:
    return _str[0:left]


def get_param_types_from_method_sign(method_sign: str) -> [str]:
    param_types = []
    pattern = r'^.*\((.*)\)'
    rs = re.match(pattern, method_sign, re.M | re.I)
    if rs:
        param_types = rs.group(1).split(',')

    return param_types


def get_param_data(method_sign: str, data: str) -> []:
    """
    get param data from tx data
    """
    param_types = get_param_types_from_method_sign(method_sign)
    if data[0:2].lower() == '0x':
        data = data[10:]

    rs = eth_abi.decode_abi(param_types, to_bytes(data))
    i = 0
    param_data = []
    for t in param_types:
        if '[]' in t:  # there is array
            d = list(rs[i])
        elif 'bytes' in t:  # there is bytes data
            d = Web3.toHex(rs[i])
        else:
            d = rs[i]
        param_data.append({'type': t, 'value': d})
        i += 1
    # print('param_data', param_data)
    return param_data
