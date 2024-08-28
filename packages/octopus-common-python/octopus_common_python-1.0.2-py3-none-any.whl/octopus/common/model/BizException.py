from octopus.common.enums.ErrorCode import ErrorCode


class BizException(Exception):
    def __init__(self, error_code: ErrorCode = ErrorCode.SYSTEM_ERROR):
        self.code = error_code.code
        self.message = error_code.message
