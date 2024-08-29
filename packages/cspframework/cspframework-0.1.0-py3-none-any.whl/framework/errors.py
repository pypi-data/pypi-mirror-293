# -*- encoding: utf-8 -*-
# 错误码框架定义
from dataclasses import dataclass

__ERRCODES_ALL__ = set()


@dataclass
class ErrCode:
    value: int
    desc: str

    def __init__(self, value: int, desc: str):
        self.value = value
        self.desc = desc
        __ERRCODES_ALL__.add(value)

    def format(self, msg):
        return ':'.join((str(self), msg)) if (msg is not None and msg != '') else str(self)


class BasicErrCodes:
    OK = ErrCode(0, "OK")
    COMMON_ERR = ErrCode(-1, "UnknownError")
    STATUS_ERR = ErrCode(-2, "StatusError")
    PARAM_ERR = ErrCode(-3, "ParameterError")
    UNINITED = ErrCode(-4, "Uninitialized")

    @staticmethod
    def has(code: int):
        return code in BasicErrCodes.__ALL__


BasicErrCodes.__ALL__ = __ERRCODES_ALL__


@dataclass
class AlgorithmException(Exception):
    code: ErrCode
    msg: str

    def __str__(self):
        return self.code.format(self.msg)
