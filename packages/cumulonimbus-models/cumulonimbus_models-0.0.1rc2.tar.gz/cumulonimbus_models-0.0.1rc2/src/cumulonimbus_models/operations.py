from datetime import datetime
from typing import Any, ClassVar, Literal, Optional

from pydantic import ConfigDict
from pydantic.main import BaseModel

from cumulonimbus_models.api import APIRequest


class OperationBase(BaseModel):
    agent_id: str
    operation_id: str


OperationResultStatus = Literal['PENDING', 'SUCCESS', 'FAILURE']


class OperationResultStatuses:
    PENDING: ClassVar[OperationResultStatus] = 'PENDING'
    SUCCESS: ClassVar[OperationResultStatus] = 'SUCCESS'
    FAILURE: ClassVar[OperationResultStatus] = 'FAILURE'


OperationType = Literal['UPDATE', 'SHELL_COMMAND']


class OperationTypes:
    UPDATE: ClassVar[OperationType] = 'UPDATE'
    SHELL_COMMAND: ClassVar[OperationType] = 'SHELL_COMMAND'


class Operation(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: str
    type: OperationType
    parameters: Any



class ShellCommandOperationParameters:
    command: str


class ShellCommandOperation(Operation):
    parameters: ShellCommandOperationParameters


class UpdateOperationParameters:
    pass


class UpdateOperation(Operation):
    type: OperationType = 'UPDATE'
    parameters: UpdateOperationParameters = UpdateOperationParameters()



class SubmitOperationRequest(APIRequest):
    route_format: ClassVar[str] = '/agent/{agent_id}/operation/submit'
    type: ClassVar[OperationType]


class SubmitOperationResponse(BaseModel):
    operation_id: str
    submitted: datetime


class OperationResult(BaseModel):
    operation_output: str
    display_output: Optional[str] = None
    operation_status: OperationResultStatus
    result_data: Optional[dict[str, str]] = None

    '''
    @model_validator(mode='after')
    def validate_outputs(self) -> 'OperationResult':
        if self.display_output is None:
            self.display_output = self.operation_output
        return self
    '''


class UpdateOperationResultRequest(APIRequest):
    route_format: ClassVar[str] = '/agent/{agent_id}/operation/{operation_id}/result'
    started: datetime
    completed: datetime
    operation_result: OperationResult
