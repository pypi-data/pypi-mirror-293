import collections
from typing import ClassVar

from pydantic.main import BaseModel

from cumulonimbus_models.operations import OperationTypes, OperationType, SubmitOperationRequest


class SubmitUpdateOperationRequest(SubmitOperationRequest):
    type: ClassVar[OperationType] = OperationTypes.UPDATE
    parameters: dict[str, str] = {}


class ShellCommandOperationParameters(BaseModel):
    command: str
    args: list[str] = []


class SubmitShellCommandOperationRequest(SubmitOperationRequest):
    type: ClassVar[OperationType] = OperationTypes.SHELL_COMMAND
    parameters: ShellCommandOperationParameters

