"""@author: jldupont"""

import pytest
from pygcloud.constants import Instruction
from pygcloud.models import (
    Result,
    Param,
    EnvValue,
    GCPServiceSingletonImmutable,
    GCPServiceRevisionBased,
    GCPServiceUpdatable,
    service_groups,
)

#  pytest.skip("NEED TO REENABLE", allow_module_level=True)


@pytest.fixture
def mock_sg_service(mock_sg, mock_service):

    service_groups.clear()
    sg = service_groups.create("sg")
    sg.append(mock_service)
    return sg


@pytest.fixture
def common_params():
    return [Param("--common", "value")]


class MockServiceUpdatable(GCPServiceUpdatable):

    COMMON = [
        ("--param", "value"),
    ]

    def params_describe(self):
        return ["describe", "param_describe", self.COMMON]

    def params_create(self):
        return ["create", "param_create", self.COMMON]

    def params_update(self):
        return ["update", "param_update", self.COMMON]

    def after_create(self, result: Result):
        result = super().after_create(result)
        self.created = True
        return result

    def after_update(self, result: Result):
        result = super().after_update(result)
        self.updated = True
        return result


class MockServiceAlreadyExists(MockServiceUpdatable):

    def before_describe(self):
        self.already_exists = True


class MockServiceDoesNotExists(MockServiceUpdatable):

    def after_describe(self, result: Result):
        self.already_exists = False
        return result


def test_deployer_already_exists(deployer, mock_sg):

    s = MockServiceAlreadyExists("already_exists", ns="service")

    mock_sg + s
    deployer.deploy(mock_sg)

    assert s.last_result.success
    assert s.updated

    with pytest.raises(AttributeError):
        assert s.created is None

    assert deployer.cmd.last_command_args == [
        "echo",
        "update",
        "param_update",
        "--param",
        "value",
    ]


def test_deployer_needs_creation(deployer, mock_sg):

    s = MockServiceDoesNotExists("MockServiceDoesNotExists")

    mock_sg + s
    deployer.deploy(mock_sg)

    assert s.last_result.success
    assert s.created

    with pytest.raises(AttributeError):
        assert s.updated is not None

    assert deployer.cmd.last_command_args == [
        "echo",
        "create",
        "param_create",
        "--param",
        "value",
    ]


def test_deployer_with_common_params(deployer, mock_sg, common_params):

    deployer.set_common_params(common_params)

    s = MockServiceAlreadyExists("MockServiceAlreadyExists")
    mock_sg + s
    deployer.deploy(mock_sg)

    assert deployer.cmd.last_command_args == [
        "echo",
        "update",
        "param_update",
        "--param",
        "value",
        "--common",
        "value",
    ]


# ==============================================================


class MockServiceSingletonImmutable(GCPServiceSingletonImmutable):

    def __init__(self, state_exists: bool = False):
        super().__init__(name="Singleton", ns="service")
        self.state_exists = state_exists

    def params_describe(self):
        """Only called when REQUIRES_DESCRIBE_BEFORE_CREATE is True"""

        if not self.REQUIRES_DESCRIBE_BEFORE_CREATE:
            raise Exception("Should not be called")

        return ["describe", "param_describe"]

    def params_create(self):
        return ["create", "param_create"]

    def params_update(self):
        raise Exception("should not be called")

    def after_create(self, result: Result) -> Result:
        if self.state_exists:
            result = Result(
                success=False, message="bla bla ALREADY_EXISTS bla bla", code=1
            )
        else:
            result = Result(success=True, message="Whatever", code=0)
        return super().after_create(result)


def test_singleton_first_creation(deployer, mock_sg, common_params):

    deployer.set_common_params(common_params)

    s = MockServiceSingletonImmutable(state_exists=False)
    mock_sg + s
    deployer.deploy(mock_sg)

    assert s.last_result.success
    assert not s.already_exists


def test_singleton_already_exists(deployer, mock_sg, common_params):

    deployer.set_common_params(common_params)

    s = MockServiceSingletonImmutable(state_exists=True)
    mock_sg + s
    deployer.deploy(mock_sg)

    assert s.last_result.success
    assert s.already_exists


# ==============================================================


class MockServiceRevisionBased(GCPServiceRevisionBased):
    def params_create(self):
        return ["create", "param_create"]


def test_revision_based_normal(deployer, mock_sg):

    s = MockServiceRevisionBased(name="MockServiceRevisionBased")
    mock_sg + s
    deployer.deploy(mock_sg)

    assert s.last_result.success


# ==============================================================


class MockServiceNotDeployable(GCPServiceRevisionBased):

    def params_create(self):
        return ["create", "param_create"]

    def after_create(self, result: Result) -> Result:
        return Result(success=False, message="Some Error", code=1)


def test_revision_based_not_deployable(deployer, mock_sg):

    s = MockServiceNotDeployable()
    mock_sg + s

    with pytest.raises(SystemExit):
        deployer.deploy(mock_sg)


def test_deploy_service_group(deployer, mock_service):

    service_groups.clear()

    sg = service_groups.create("sg")

    sg.append(mock_service)

    deployer.deploy(sg)

    assert mock_service.last_result.success


def test_service_group_idempotence(mock_service):

    service_groups.clear()
    sg = service_groups.create("mock")

    sg.add(mock_service)

    with pytest.raises(Exception):
        sg.add(mock_service)


def test_deploy_service_groups_retrieve_by_name(
    deployer, env_first_key, mock_service_class
):

    service_groups.clear()
    ms1 = mock_service_class()
    ms2 = mock_service_class()
    ms3 = mock_service_class()

    ms3.last_result = None

    # Pretend the deployment group name comes from an environment variable
    group_name = EnvValue(env_first_key)

    # Pretend we have a group of services we want to deploy together
    sg = service_groups.create(group_name)
    sg.append(ms1)
    sg.append(ms2)
    sg.append(ms3)

    # Reference the deployment by some environment name
    deployer.deploy(group_name)

    assert ms3.last_result.success
    assert ms3.last_result is not None


def test_deploy_with_callable(deployer):

    def task():
        return Result(success=True, message="task_done", code=0)

    service_groups.clear()
    sg = service_groups.create("sg")
    sg.append(task)

    result = deployer.deploy("sg")

    assert result.message == "task_done"


def test_deploy_with_before_deploy_in_service(deployer, mock_service):

    called = False

    def task():
        nonlocal called
        called = True

    mock_service.add_task_before_deploy(task)

    service_groups.clear()
    sg = service_groups.create("sg")
    sg.append(mock_service)

    deployer.deploy("sg")

    assert called


def test_deploy_abort(deployer, mock_service):

    def task():
        return Instruction.ABORT_DEPLOY

    mock_service.add_task_before_deploy(task)

    service_groups.clear()
    sg = service_groups.create("sg")
    sg.append(mock_service)

    result = deployer.deploy("sg")

    assert isinstance(result, Instruction)
    assert result == Instruction.ABORT_DEPLOY


def test_deploy_abort_all(deployer, mock_service):

    def task():
        return Instruction.ABORT_DEPLOY_ALL

    called = False

    def task_should_not_be_executed():
        nonlocal called
        called = True

    mock_service.add_task_before_deploy(task)
    mock_service.add_task_before_deploy(task_should_not_be_executed)

    service_groups.clear()
    sg = service_groups.create("sg")
    sg.append(mock_service)

    result = deployer.deploy("sg")

    assert isinstance(result, Instruction)
    assert result == Instruction.ABORT_DEPLOY_ALL
    assert not called


def test_hooks(deployer, mock_sg_service):
    """
    Empty service group should anyway
    have the "start" and "end" hooks called
    """

    sg = mock_sg_service
    deployer.deploy(sg)

    assert deployer.history_hooks == [
        "start_deploy",
        "before_deploy",
        "after_deploy",
        "end_deploy",
    ], print(deployer.history_hooks)
