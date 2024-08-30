from datetime import datetime

from typing import NamedTuple


def test_operations():
    class TestType(NamedTuple):
        test: str
    test_data = TestType(test='test')
    from cumulonimbus_models import operations, operation_submissions
    assert operations.Operation(id='test-operation-id', type='UPDATE', parameters=test_data)
    assert operations.OperationResultStatuses.PENDING
    assert operations.OperationTypes.UPDATE
    assert operations.SubmitOperationRequest(type='UPDATE', parameters=())
    assert operations.SubmitOperationResponse(operation_id='test', submitted=datetime.now())
    assert operations.OperationResult(operation_output='test', operation_status='PENDING')
    assert operations.UpdateOperationResultRequest(started=datetime.now(), completed=datetime.now(), operation_result=operations.OperationResult(operation_output='test', operation_status='PENDING'))
    assert operations.OperationBase(agent_id='test', operation_id='test')
    assert operation_submissions.SubmitShellCommandOperationRequest(parameters=operation_submissions.ShellCommandOperationParameters(command='test'))
    assert operation_submissions.SubmitUpdateOperationRequest(parameters={})

