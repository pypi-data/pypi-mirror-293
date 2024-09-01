from builtins import BaseException, BaseExceptionGroup


def get_utf8_string(value: str) -> str:
    return value.encode("utf-8").decode("utf-8")


class CliException(BaseException): ...


class CliExceptionGroup(BaseExceptionGroup): ...


class CliError(CliException): ...


class CliWarning(CliException): ...


class CliInfo(CliException): ...
