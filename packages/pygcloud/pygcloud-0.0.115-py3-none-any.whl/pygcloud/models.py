"""
@author: jldupont
"""

import os
import logging
from functools import cache
from collections import UserList
from typing import List, Tuple, Union, Any, Type, Set, Dict
from collections.abc import Callable
from abc import abstractmethod
from dataclasses import dataclass, field
from .constants import ServiceCategory, Instruction
from .base_types import BaseType

from ._models import _Spec

Str = Union[str, None]
Bool = Union[bool, None]

# We cannot put this object as "class var"
# in Spec because of the treatment in dataclass
Specs: Set = set()


class Spec(_Spec):

    @classmethod
    @property
    def derived_class_types(cls):
        return Specs

    def __post_init__(self):
        """
        Helper for typical URI type name i.e.

        projects/PROJECT/locations/LOCATION/RESOURCE/id
        """
        fnc = getattr(self, "__post_init_ex__", None)
        if fnc is not None:
            fnc()

        if not getattr(self, "name", False):
            return

        # it might be a Ref
        if not isinstance(self.name, str):
            return

        parts = self.name.split("/")
        if len(parts) != 6:
            self.name = parts[-1]
            return

        self.location = parts[3]
        self.name = parts[-1]


def spec(cls):
    """
    Class decorator to collect all definitions of
    Spec derived classes. This is required for the catalog.

    TODO use python's MethodType to retrieve unbound
         class methods from Spec and inject them into
         the target class type. This way, we could avoid
         forcing subsclassing from Spec.

    NOTE Attempting to "lift" the class methods directly
         from Spec and 'setattr' them into the class
         being defined does not work: the '__annotations__'
         and other class level definitions pertinent to
         `dataclass` would not be accessible.
    """
    global Specs
    Specs.add(cls)
    return cls


class OptionalParam(UserList):
    """
    If the value resolves to None, the list resolves to empty.

    If the value resolves to something other than None,
    then the list resolves to [param, value]
    """

    def __init__(self, param, value):
        self._param = param
        self._value = value
        if value is None:
            super().__init__()
        else:
            super().__init__([param, value])

    def __repr__(self):
        return f"OptionalParam({self._param, self._value})"


class OptionalParamFromAttribute(UserList):
    """
    If the value of the attribute on the obj
    resolves to "not None", return the list
    []
    """

    def __init__(self, param: str, obj: Any, attr: str):
        assert isinstance(param, str)
        assert isinstance(attr, str)
        self._param = param

        if obj is None:
            return super().__init__()

        value = getattr(obj, attr, None)
        if value is None:
            return super().__init__()

        super().__init__([param, value])

    def __repr__(self):
        return f"OptionalParamFromAttribute({self._param})"


class EnvValue(str):
    """
    Retrieve a value from an environment variable
    """

    def __new__(cls, name, default=None):
        value = os.environ.get(name, default)
        instance = super().__new__(cls, value)
        setattr(instance, "_name", value)
        return instance

    def __repr__(self):
        return f"EnvValue({self._value})"


class LazyValue:
    """
    Abstract base class for lazy resolvers
    """


class LazyEnvValue(str, LazyValue):
    """
    Retrieve a value from an environment variable

    Other operators aside from __eq__ and __neq__
    might be required in the future
    """

    def __init__(self, name):
        super().__init__()
        self._name = name

    @property
    def value(self):
        v = os.environ.get(self._name, None)
        if v is None:
            raise ValueError(f"Environment var '{self._name}' does not exist")
        return v

    def __str__(self):
        return self.value

    def __eq__(self, other):
        return self.value == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        v = os.environ.get(self._name, None)
        return f"LazyEnvValue({self._name}, {v})"


class LazyAttrValue(LazyValue):
    """
    Retrieve a value from an object

    The attribute name can be nested
    using "dot" notation

    See example in the unit-test
    """

    def __init__(self, obj: Any, path: str):
        self._obj = obj
        self._path = path

    @property
    def value(self):
        try:
            parts = self._path.split(".")
            result = self._obj

            while parts:
                key = parts.pop(0)
                if isinstance(result, dict):
                    result = result[key]
                else:
                    result = getattr(result, key)

            return result
        except Exception as e:
            logging.warning(e)
            raise ValueError("Cannot resolve value")

    def __eq__(self, other):
        return self.value == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        obj_repr = repr(self._obj)
        return f"LazyAttrValue({obj_repr}, {self._path})"


@dataclass
class Param:
    """Description of a gcloud parameter"""

    key: str
    value: str

    def __len__(self):
        return 2

    def __getitem__(self, index):

        if index == 0:
            return self.key

        if index == 1:
            return self.value

        # unpacking tuple requires
        # iteration protocol
        raise StopIteration

    def __repr__(self):
        return f"Param({self.key}, {self.value})"


class EnvParam(Param):
    """
    For parameters coming from environment variables
    """

    def __init__(self, key: str, env_var_name: str, default: Str = None):
        """
        key: parameter name
        env_var_name: environment variable name
        """
        assert isinstance(key, str)
        assert isinstance(env_var_name, str)

        self._key = key
        self._env_var_name = env_var_name

        value = os.environ.get(env_var_name, default)
        if value is None:
            raise ValueError(f"Environment variable {env_var_name} not found")
        super().__init__(key, value)

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"EnvParam({self._key}, {self._env_var_name})"


Params = Union[List[Tuple[str, str]], List[Param]]
Label = Tuple[str, str]
GroupName = Union[str, EnvValue]


class GroupNameUtility:

    @staticmethod
    def is_of_type(what: GroupName):
        return isinstance(what, str) or isinstance(what, EnvValue)

    @staticmethod
    def resolve_group_name(name: GroupName) -> str:

        if isinstance(name, str):
            return name

        if isinstance(name, EnvValue):
            return name.value

        raise Exception(f"Expecting a valid name, got: {name}")


@dataclass(frozen=True)
class Result:
    success: bool
    message: str
    code: int


class ServiceMeta(type):

    @classmethod
    def only_add_real_service_class(cls, classe):
        new_class_name = classe.__name__.lower()

        if "servicenodeunknown" in new_class_name:
            return

        if "mock" in new_class_name:
            return

        if new_class_name == "servicenode":
            return

        if "gcpservice" in new_class_name:
            return

        cls.__all_classes__.append(classe)

    def __new__(cls, name, bases, attrs):

        if not getattr(cls, "__all_classes__", False):
            setattr(cls, "__all_classes__", [])

        new_class = super().__new__(cls, name, bases, attrs)
        cls.only_add_real_service_class(new_class)
        return new_class

    def __getattribute__(cls, name):
        """
        Address the challenge of getting the derived class'
        __class__ attribute to work properly when using a metaclass

        "mro" : Method Resolution Order
        """
        if name == "__class__":
            return cls.__mro__[0]  # Get the first class in the MRO
        return super().__getattribute__(name)


class ServiceNode(metaclass=ServiceMeta):
    """
    Protocol to establish "use" relationships
    between services
    """

    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def ns(self):
        raise NotImplementedError


class GCPService(ServiceNode):
    """
    Base class for GCP services

    The 'name' and 'ns' (namespace) parameters are
    only useful when the relationship "use" feature is used.

    We do not use the class name as namespace because
    it might happen we will extend the classes to support
    more usecases.

    REQUIRES_UPDATE_AFTER_CREATE: provides support for services
    which cannot be fully configured during the creation phase.
    For example, Google GCS cannot set labels during creation.

    REQUIRES_DESCRIBE_BEFORE_CREATE: for "create only" services
    that requires checking for existence before attempting creation.
    For example: Firestore database.
    """

    SERVICE_CATEGORY: ServiceCategory = ServiceCategory.INDETERMINATE
    REQUIRES_UPDATE_AFTER_CREATE: bool = False
    REQUIRES_DESCRIBE_BEFORE_CREATE: bool = False
    LISTING_CAPABLE: bool = False
    LISTING_REQUIRES_LOCATION: bool = False
    DEPENDS_ON_API: Str = None
    SPEC_CLASS: Union[Type["Spec"], None] = None
    GROUP: List[str] = []
    GROUP_SUB_DESCRIBE: List[str] = []
    # NAME_PATTERN: str = re.compile(r"^([0-9a-zA-Z\_\-\.\/\:]+)$")
    EXCLUDE_FROM_GRAPH: bool = False

    @classmethod
    def stem_class_from_class(cls) -> Type:
        assert issubclass(cls, ServiceNode)

        def check_class(classe):

            if classe.__name__ == "GCPService":
                raise ValueError("GCPService is the base class")

            if classe.__name__ == "ServiceNode":
                raise ValueError("ServiceNode is the base class")

            if classe.__name__ == "type":
                raise ValueError("Type is a class constructor")

            try:
                parent = classe.__bases__[0]
                if parent.__name__.startswith("GCPService"):
                    return classe
            except:  # NOQA
                pass
            return None

        classe = cls
        depth = 0
        MAX_DEPTH = 3

        while True:
            klass = check_class(classe)
            if klass is not None:
                return classe

            classe = classe.__bases__[0]
            depth += 1
            if depth > MAX_DEPTH:
                break

        raise ValueError(f"Could not find the stem for: {cls}")

    def stem_class_from_self(self) -> Type:
        """
        Returns the class type of the first level derived class
        """
        assert isinstance(self, ServiceNode)
        return self.stem_class_from_class()

    @property
    def category(self):
        return self.SERVICE_CATEGORY

    @property
    def name(self) -> Str:
        return self._name

    @property
    def ns(self) -> Str:
        return self._ns

    def __init__(self, name: Str = None, ns: Str = None):
        """
        name: string (optional)
        ns: string (optional)
        """
        if name is not None:
            assert isinstance(name, str), print(name)
            # if self.NAME_PATTERN.fullmatch(name) is None:
            #    raise ValueError(f"Invalid name: {name}")
        if ns is not None:
            assert isinstance(ns, str)

        self.already_exists: Bool = None  # indeterminated
        self.last_result: Union[Result, None] = None
        self._name: Str = name
        self._ns: Str = ns
        self._uses: List[ServiceNode] = []
        self._callables_before_deploy: List[Callable] = []
        self._just_describe: bool = False
        self._spec: Union["Spec", None] = None

    @property
    def spec(self) -> Union["Spec", None]:
        return self._spec

    @spec.setter
    def spec(self, spec):
        self._spec = spec

    @property
    def just_describe(self) -> bool:
        return self._just_describe

    def set_just_describe(self, enable: bool = True):
        self._just_describe = enable
        return self

    def __repr__(self):
        return f"{self.__class__.__name__}"
        f"({self._name}, already_exists={self.already_exists or ''},"
        f"last_result={self.last_result or ''})"

    def add_task_before_deploy(self, task: Union[Callable, List[Callable]]):

        if isinstance(task, Callable):
            self._callables_before_deploy.append(task)
            return self

        if isinstance(task, List):
            self._callables_before_deploy.extend(task)
            return self

        raise Exception("Expecting task or task list, " f"got: {type(task)}")

    @classmethod
    @cache
    def generate_label(cls, target: ServiceNode) -> Union[str, None]:
        """
        Needs to be implemented in a derived class
        """
        return None

    def validate_label(self, target: ServiceNode) -> bool:
        try:
            self.generate_label(target)

        except Exception:
            return False

        return True

    def before_use(self, target_service: ServiceNode) -> None:
        """
        Raises exception if a valid label cannot be derived
        """
        if self.validate_label(self) is None:
            logging.warning(
                "Label validation is not available for:" f" {self.__class__.name}"
            )
        else:
            self.validate_label(self)

        if not self.validate_label(target_service):
            logging.warning(
                "Label validation is not available for:"
                f" {target_service.__class__.name}"
            )
        else:
            self.validate_label(target_service)

    def use(self, service: ServiceNode):
        self.before_use(service)
        self._uses.append(service)
        self.after_use(service)
        return self

    def after_use(self, service: ServiceNode):
        pass

    @property
    def uses(self) -> List[ServiceNode]:
        return self._uses

    def before_deploy(self) -> Union[Instruction, None]:
        """
        Called by Deployer

        If Instruction.ABORT_DEPLOY is returned by a task,
        the Deployer will abort the deployment of the
        current service.
        """

        instruction: Union[Instruction, None] = None
        for task in self._callables_before_deploy:

            try:
                tname = task.__name__
            except Exception:
                # partial functions do not have __name__
                tname = str(task)

            logging.debug(f"before_deploy: executing {tname}")
            instruction = task()
            if instruction is not None:
                if instruction.is_abort():
                    return instruction

        # returns last instruction ; plan accordingly
        return instruction

    def before_describe(self):
        """This is service specific"""

    def before_create(self):
        """This is service specific"""

    def before_update(self):
        """This is service specific"""

    def before_delete(self):
        """This is service specific"""

    def params_describe(self) -> Params:
        """This is service specific"""
        raise NotImplementedError

    def params_create(self) -> Params:
        """This is service specific"""
        raise NotImplementedError

    def params_update(self) -> Params:
        """This is service specific"""
        raise NotImplementedError

    def params_delete(self) -> Params:
        """This is service specific"""
        raise NotImplementedError

    def after_describe(self, result: Result) -> Result:
        """This is service specific"""
        self.last_result = result

        if not result.success:
            self.already_exists = False
            return result

        if result.success:
            self.already_exists = True
            if self.SPEC_CLASS is not None:
                self._spec = self.SPEC_CLASS.from_string(
                    result.message, origin_service=self
                )

        return result

    def after_create(self, result: Result) -> Result:
        self.last_result = result

        if not result.success:
            return result

        if result.success:
            self.already_exists = False
            if self.SPEC_CLASS is not None:
                self._spec = self.SPEC_CLASS.from_string(
                    result.message, origin_service=self
                )
                if isinstance(self._spec, list):
                    if len(self._spec) > 1:
                        logging.error(f"Unexpected list > 1 item: {self._spec}")
                    self._spec = self._spec[0]

        return result

    def after_update(self, result: Result) -> Result:
        self.last_result = result
        return result

    def after_delete(self, result: Result) -> Result:
        self.last_result = result
        return result

    def after_deploy(self):
        """Called by Deployer"""


class GCPServiceUnknown(GCPService):
    """
    Placeholder for an unknown / unsupported service
    """


class GCPServiceInstanceNotAvailable(GCPService):
    """
    A placeholder for situations where the GCPService
    instance isn't available
    """


class GCPServiceSingletonImmutable(GCPService):
    """
    Base class for GCP services that can only be created once.
    Example: Firestore indexes

    For this class, we ignore exceptions arising from the
    service already being created: we do this by interpreting
    the result code in the "after_create" method.
    """

    SERVICE_CATEGORY = ServiceCategory.SINGLETON_IMMUTABLE

    def before_create(self):

        # We do not know if the service already exists
        # but we set it to False to simplify the creation
        # of derived classes
        self.already_exists = False
        self.last_result = None

    def after_create(self, result: Result) -> Result:

        self.last_result = result

        # Case 1: the service was just created
        if result.code == 0:
            return super().after_create(result)

        # Case 2: Check if the service already exists
        lmsg = result.message.lower()

        if "already_exists" in lmsg or "already exists" in lmsg:

            # fake idempotence
            self.already_exists = True
            new_result = Result(success=True, message=result.message, code=0)
            self.last_result = new_result
            return new_result

        return result


class GCPServiceRevisionBased(GCPService):
    """
    Base class for GCP services that deploy with unique revisions
    """

    SERVICE_CATEGORY = ServiceCategory.REVISION_BASED

    def before_update(self):
        raise Exception("This method should not be implemented")

    def after_update(self, result: Result) -> Result:
        raise Exception("This method should not be implemented")


class GCPServiceUpdatable(GCPService):
    """
    Base class for GCP services that can be updated
    but must be created first
    """

    SERVICE_CATEGORY = ServiceCategory.UPDATABLE


class ServiceGroup(list):
    """
    Utility class for grouping service instances

    Useful for deploying services in group whilst
    keeping a central view of all services in a workload

    A service instance can only be added once per group.
    """

    @property
    def name(self):
        return self._name

    def __init__(self, name: Union[str, EnvValue]):
        self._name = GroupNameUtility.resolve_group_name(name)
        self._all = set()

    def clear(self):
        self._all.clear()
        super().clear()

    @property
    def all(self):
        return self._all

    def append(self, what: Union[GCPService, Callable]):
        assert isinstance(what, GCPService) or callable(what)
        if what in self._all:
            raise Exception(f"{what} already in group: {self}")
        self._all.add(what)
        return super().append(what)

    add = append
    __add__ = append

    def __repr__(self):
        count = len(self._all)
        return f"ServiceGroup(name={self.name}, count={count})"


class ServiceGroups(list):
    """
    Container utility class for groups

    The use case is for a Deployer to retrieve
    a target group of services to deploy

    Since it's base class is a list, just
    'append' to it but the more typical use
    case would be to use the `create` method
    so that the groups are properly tracked.
    """

    def __init__(self):
        super().__init__()
        self._map = dict()

    def empty(self):
        """
        Empties each service group
        """
        [group.clear() for group in self]

    def clear(self):
        self.empty()
        super().clear()
        self._map.clear()

    @property
    def all(self) -> Dict[str, ServiceGroup]:
        return self._map

    def __getitem__(self, what: Union[str, GroupName]):
        str_name = GroupNameUtility.resolve_group_name(what)
        return self._map[str_name]

    def get(self, what, default):
        str_name = GroupNameUtility.resolve_group_name(what)
        return self._map.get(str_name, default)

    def create(self, name: GroupName) -> ServiceGroup:
        """
        Create or retrieve a group by name

        NOTE Idempotent operation
        """
        str_name = GroupNameUtility.resolve_group_name(name)

        if (group := self._map.get(str_name, None)) is not None:
            return group

        # create a new one and keep track of it
        group: ServiceGroup = ServiceGroup(name)

        self._map[str_name] = group
        self.append(group)

        return group


# We only really need one group of groups
service_groups = ServiceGroups()


class PolicyViolation(Exception):
    """Base class for all policy violations"""


class Policy(metaclass=BaseType):
    """
    The base class for all policies

    We are using class methods to simplify usage i.e.
    instead of having the user track policy instances
    in the build code

    REQUIRES_SERVICE_SPEC: if the policy requires the availability
    of the service specification for it to be effective. This is
    particularily pertinent for the "after deployment use-cases".
    """

    REQUIRES_SERVICE_SPEC: bool = False

    _allowed: List[GCPService] = []

    def __init__(self):
        raise Exception("Cannot be instantiated")

    @classmethod
    @property
    def name(cls):
        return cls.__name__

    @classmethod
    def allows(cls, service: GCPService):
        assert isinstance(service, GCPService)
        return service in cls._allowed

    @classmethod
    def allow(cls, service: GCPService, reason: str):
        assert isinstance(service, GCPService)
        assert isinstance(reason, str)

        logging.warning(
            f"The service '{service}' was "
            f"allowed by default on policy '{cls.name}', reason= {reason}"
        )
        cls._allowed.append(service)
        return cls

    @classmethod
    def evaluate(cls, groups: List[ServiceGroup], service: GCPService):
        """
        NOTE must be implemented in derived classes

        NOTE Must raise an exception when policy is violated
        """
        raise NotImplementedError


@dataclass
class PolicingResult:
    """
    passed: True if the policy evaluation passed
    raised: when an exception was raised in DRY_RUN mode
    allowed: when skipped because policy allowed by default on service
    skipped: if the policy could not be evaluated
    """

    service: GCPService
    policy: Policy
    violation: Union[PolicyViolation, None] = field(default=None)

    raised: bool = field(default=False)
    passed: bool = field(default=False)
    allowed: bool = field(default=False)
    skipped: bool = field(default=False)


@dataclass
class PolicingResults:
    """
    outcome: the takeaway result - if passed => None
    results: the individual results
    """

    outcome: Union[PolicingResult, None]
    results: List[PolicingResult]
