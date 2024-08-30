"""
Data models related to GCP services

NOTE The classvar `REF_NAME` contains the string
     used to reference the service in various links
     such as 'users', 'target', "selfLink' etc.

@author: jldupont
"""
import re
from typing import List, Dict, Union, ClassVar
from dataclasses import dataclass, field
from pygcloud.models import Spec, spec, GCPService
from ._models import _Ref, _hash


EXCEPT_SLASH = "([^/]+)"

# CloudRun example...
# /apis/serving.knative.dev/v1/namespaces/215695389495/services/SERVICE'

PROJECT = f"/projects/(?P<project>{EXCEPT_SLASH})"
PROJECT2 = f"projects/(?P<project>{EXCEPT_SLASH})"
REGION = f"/regions/(?P<region>{EXCEPT_SLASH})"
GLOBAL = "/(?P<region>global)"
SERVICE_TYPE_NAME = f"/(?:(?P<service_type>{EXCEPT_SLASH}))/(?P<name>{EXCEPT_SLASH})"
SERVICE_ACCOUNT = r"^(?:user\:)?(?:serviceAccount\:)?(?P<name>([\w\-\.]+)\@(?P<project>[\w\-]+)\.iam\.gserviceaccount\.com)$"
SERVICE_ACCOUNT2 = r"^(?:user\:)?(?:serviceAccount\:)?(?P<name>([\w\-\.]+)\@([\w\-\.]+)\.gserviceaccount\.com)$"
SERVICE_ACCOUNT3 = r"^(?P<name>project[\w]+\:(?P<project>.*))$"
SERVICE_ACCOUNT4 = r"\/serviceAccounts\/(?P<name>.*)$"
CLOUD_RUN_SELFLINK = r"^\/apis\/serving\.knative\.dev\/v[0-9]{1,2}\/namespaces\/(?P<project_number>[0-9]+)\/services\/(?P<name>[\w\-\_]+)$"  # NOQA
#
# The order is important: longest first
#
PATTERNS = [
    (re.compile(CLOUD_RUN_SELFLINK), {"service_type": "CloudRun"}),
    (re.compile(SERVICE_ACCOUNT),  {"service_type": "ServiceAccount"}),
    (re.compile(SERVICE_ACCOUNT2), {"service_type": "ServiceAccount"}),
    (re.compile(SERVICE_ACCOUNT3), {"service_type": "ServiceAccount"}),
    (re.compile(PROJECT + REGION + SERVICE_TYPE_NAME), {}),
    (re.compile(PROJECT + GLOBAL + SERVICE_TYPE_NAME), {}),
    (re.compile(PROJECT + GLOBAL), {}),
    (re.compile(PROJECT + REGION), {}),
    (re.compile(PROJECT2 + SERVICE_ACCOUNT4), {"service_type": "ServiceAccount"}),
]


class UnknownRef(Exception):
    """
    Used to signal unknown
    or (yet) unsupported reference
    """


Str = Union[str, None]


@dataclass
@_hash
class Ref(_Ref):
    """
    A reference from the `origin_service` to another service instance

    service_type: directly from the service spec
    name: the actual given to the service by the user without the URI prefix
    origin_service: the GCP service instance where this ref comes from
    """

    project: Str = field(default=None)
    project_number: Str = field(default=None)
    region: Str = field(default=None)
    name: Str = field(default_factory=str)
    service_type: Str = field(default=None)
    origin_service: GCPService = field(default=None)


@dataclass
@_hash
class RefSelfLink(Ref):
    """selfLink"""


@dataclass
@_hash
class RefUses(Ref):
    """uses"""


@dataclass
@_hash
class RefUsedBy(Ref):
    """usedBy"""


@dataclass
class UnknownSpecType(Spec):
    """
    Placeholder for unknown / unsupported spec types
    """


@spec
@dataclass
class ServiceAccountSpec(Spec):
    """
    "name":
        "projects/$project/serviceAccounts/
            $project_number-compute@developer.gserviceaccount.com"
    """

    name: RefSelfLink
    email: str
    projectId: str
    uniqueId: str
    oauth2ClientId: str
    displayName: str = field(default_factory=str)
    description: str = field(default_factory=str)

    def is_default(self):
        """
        Is this service account a default one
        """
        return "iam.gserviceaccount.com" not in self.email

    @classmethod
    def build_name(cls, input: str, project_id: str):
        """
        Builds the name (email)
        """
        if "@" not in input or "iam.gserviceaccount.com" not in input:
            return f"{input}@{project_id}.iam.gserviceaccount.com"
        return input

    @property
    def id(self):
        ref = self.name
        return ref.name.partition("@")[0]


@spec
@dataclass
class ProjectDescription(Spec):
    name: str
    projectId: str
    projectNumber: str
    lifecycleState: str
    parent: dict


@spec
@dataclass
class ServiceDescription(Spec):
    """
    A service description as retrieved through
    `gcloud services list --enabled`

    e.g. name:
        projects/215695389495/services/storage.googleapis.com
    """

    name: str
    state: str
    parent: str
    project_number: int = 0
    api: str = "???"

    def __post_init__(self):
        parts = self.name.split("/")
        self.project_number = parts[1]
        self.api = parts[-1]


@spec
@dataclass
class IAMBinding(Spec):
    """
    By default, if the 'email' does not
    contain a namespace prefix, it will be
    set to "serviceAccount"
    """

    email: str
    role: str
    ns: str = field(default=None)

    def __post_init__(self):
        if self.ns is not None:
            return

        maybe_split = self.email.split(":")
        if len(maybe_split) == 2:
            self.ns = maybe_split[0]
            self.email = maybe_split[1]
        else:
            self.ns = "serviceAccount"

    @property
    def sa_email(self):
        return f"{self.ns}:{self.email}"

    @property
    def member(self):
        return f"{self.ns}:{self.email}"


class _IAMMember:

    @classmethod
    def from_obj(cls, obj):

        if isinstance(obj, list):
            return [cls.from_obj(item) for item in obj]

        assert isinstance(obj, str), print(
            f"{cls.__name__}: Expecting string, got: {obj}"
        )

        parts = obj.split(":")
        ns = parts[0]
        email = parts[-1]

        return cls(ns=ns, email=email)


@spec
@dataclass
class IAMMember(_IAMMember, Spec):
    """
    NOTE in some cases, 'email' is really a name or id
         e.g. ns: projectEditor
              email: $project_id

    TODO attach to Ref system
    """

    ns: str
    email: str

    @property
    def member(self):
        return f"{self.ns}:{self.email}"


@spec
@dataclass
class IAMBindings(Spec):

    members: List[IAMMember]
    role: str


@spec
@dataclass
class IAMPolicy(Spec):

    bindings: List[IAMBindings]

    @classmethod
    def from_json_list(cls, json_str: str, path: Str = None, origin_service=None):
        bindings = IAMBindings.from_json_list(
            json_str, path="bindings", origin_service=origin_service
        )
        return cls(bindings=bindings)

    from_string = from_json_list

    def contains(self, binding: IAMBinding) -> bool:
        """
        Determine if a specific binding is contained in the policy
        """
        binding: IAMBindings

        member = IAMMember(ns=binding.ns, email=binding.email)

        # scan through all bindings looking
        # for all entries pertaining to the target member
        for _binding in self.bindings:
            if member in _binding.members:
                if binding.role == _binding.role:
                    return True

        return False


@spec
@dataclass
class IPAddress(Spec):
    """
    Compute Engine IP address
    """

    REF_NAME: ClassVar[str] = "addresses"

    name: str
    address: str
    addressType: str
    ipVersion: str
    selfLink: RefSelfLink
    users: List[RefUsedBy] = field(default_factory=list)


@dataclass
class CloudRunMetadata(Spec):

    name: str
    annotations: dict
    selfLink: RefSelfLink


@dataclass
class CloudRunTemplateSpec(Spec):
    serviceAccountName: RefUses = field(default=None)


@dataclass
class CloudRunTemplate(Spec):
    spec: CloudRunTemplateSpec


@dataclass
class CloudRunSpec(Spec):
    template: CloudRunTemplate = field(default=None)


@dataclass
class CloudRunStatus(Spec):
    url: str


@spec
@dataclass
class CloudRunRevisionSpec(Spec):
    """
    Cloud Run Revision Specification (flattened)

    NOTE the selfLink format:
         "/apis/serving.knative.dev/v1/namespaces/$project_number/services/$name"
    """

    spec: CloudRunSpec
    status: CloudRunStatus
    metadata: CloudRunMetadata
    name: str = field(default=None)

    def __post_init_ex__(self):
        self.name = self.metadata.name


@spec
@dataclass
class BackendGroup(Spec):
    """
    This model is contained, AFAIK, only within
    the BackendServiceSpec

    NOTE group: can contain a link ref to a NEG
    """

    balancingMode: str
    group: RefUses
    capacityScaler: int


@spec
@dataclass
class BackendServiceSpec(Spec):
    """
    https://cloud.google.com/compute/docs/reference/rest/v1/backendServices

    NOTE selfLink e.g.
    "https://www.googleapis.com/compute/v1/projects/$project
        /global/backendServices/$name",
    """

    REF_NAME: ClassVar[str] = "backendServices"

    name: str
    port: int
    portName: str
    protocol: str
    selfLink: RefSelfLink
    backends: List[BackendGroup] = field(default_factory=list)
    iap: Dict = field(default_factory=dict)
    usedBy: List[RefUsedBy] = field(default_factory=list)


@spec
@dataclass
class FwdRule(Spec):
    """
    NOTE selfLink e.g.
        https://www.googleapis.com/compute/v1/projects/$project
            /global/forwardingRules/$name

        target e.g.:
        https://www.googleapis.com/compute/v1/projects/$project
            /global/targetHttpsProxies/$name
    """

    REF_NAME: ClassVar[str] = "forwardingRules"

    name: str
    IPAddress: str
    IPProtocol: str
    loadBalancingScheme: str
    networkTier: str
    portRange: str
    selfLink: RefSelfLink
    target: RefUses


@spec
@dataclass
class ACL(Spec):
    entity: str
    role: str


@spec
@dataclass
class GCSBucket(Spec):
    """
    NOTE 'name' is without the leading "gs://"
    """

    name: str
    location: str
    default_storage_class: str
    location_type: str
    metageneration: int
    public_access_prevention: str
    uniform_bucket_level_access: str
    acl: List[ACL] = field(default=list)
    default_acl: List[ACL] = field(default=list)


@spec
@dataclass
class SSLCertificate(Spec):
    """
    CAUTION: sensitive information in the 'certificate' field

    NOTE selfLink e.g.
        "https://www.googleapis.com/compute/v1/projects/$project
            /global/sslCertificates/$name"
    """

    REF_NAME: ClassVar[str] = "sslCertificates"

    name: str
    type: str
    selfLink: RefSelfLink
    managed: dict = field(default_factory=dict)


@spec
@dataclass
class HTTPSProxy(Spec):
    """
    sslCertificates: list of link refs
    urlMap: link ref
    """

    REF_NAME: ClassVar[str] = "targetHttpsProxies"

    name: str
    selfLink: RefSelfLink
    sslCertificates: List[RefUses] = field(default_factory=list)
    urlMap: RefUses = field(default_factory=str)


@spec
@dataclass
class SchedulerJob(Spec):
    """
    NOTE topicName e.g.
            "projects/$project/topics/$name"
    """

    name: str
    retryConfig: dict
    schedule: str
    state: str
    timeZone: str
    location: str = "???"
    pubsubTarget: dict = field(default_factory=dict)
    topicName_: str = field(default_factory=str)

    def __post_init_ex__(self):
        self.topicName_ = self.pubsubTarget.get("topicName", None)


@spec
@dataclass
class PubsubTopic(Spec):
    """
    NOTE name e.g.
            "projects/$project/topics/$name"
    """

    name: str

    def __post_init__(self):
        parts = self.name.split("/")
        self.name = parts[-1]


@spec
@dataclass
class FirestoreDb(Spec):
    """
    NOTE name format:
            projects/$PROJECT/databases/$db_name
    """

    name: str
    type: str
    locationId: str
    concurrencyMode: str
    pointInTimeRecoveryEnablement: str

    def __post_init__(self):
        parts = self.name.split("/")
        self.name = parts[-1]


@spec
@dataclass
class CloudRunNegSpec(Spec):
    """
    NOTE region e.g.
            https://www.googleapis.com/compute/beta/projects/$project
                /regions/$region

        selfLink e.g.:
            https://www.googleapis.com/compute/beta/projects/$project
                /regions/$region/networkEndpointGroups/$name
    """

    REF_NAME: ClassVar[str] = "networkEndpointGroups"

    name: str
    networkEndpointType: str
    selfLink: RefSelfLink
    region: str = field(default_factory=str)
    cloudRun: dict = field(default_factory=dict)


@spec
@dataclass
class TaskQueue(Spec):
    """
    NOTE name e.g.
            projects/$project/locations/$location/queues/$name
    """

    name: str
    state: str
    location: str = field(default_factory=str)
    rateLimits: dict = field(default_factory=dict)
    retryConfig: dict = field(default_factory=dict)


@spec
@dataclass
class UrlMap(Spec):
    """
    NOTE defaultService e.g.
            https://www.googleapis.com/compute/v1/projects/$project
                /global/backendServices/$name

    NOTE selfLink e.g.
            https://www.googleapis.com/compute/v1/projects/$project
                /global/urlMaps/$name
    """

    REF_NAME: ClassVar[str] = "urlMaps"

    selfLink: RefSelfLink
    id: str = field(default_factory=str)
    name: str = field(default_factory=str)
    defaultService: str = field(default_factory=str)
