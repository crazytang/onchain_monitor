from hexbytes import HexBytes


def bn_to_number(num: int, precision=18) -> float:
    """
    BigNumber转成普通数字
    :param num: 大整形数字
    :param precision: 精度
    :return:
    """
    return num / 10 ** precision

def batch_hex_bytes_to_string(arr:[HexBytes])->[str] :
    _strs: [str] = []
    for i in range(0, len(arr)):
        _strs.append(arr[i].hex())

    return _strs

def hex_to_dec(_hex)->int:
    return int(_hex, 16)