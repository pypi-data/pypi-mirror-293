from enum import Enum


class ErrorCode(Enum):
    SYSTEM_ERROR = (-2, "python容器系统错误")
    CAN_NOT_FIND_CRAWLER = (100000, "can't find the crawler")

    def __init__(self, code, message):
        self._code = code
        self._message = message

    @property
    def code(self):
        return self._code

    @property
    def message(self):
        return self._message
