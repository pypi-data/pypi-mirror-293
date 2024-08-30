"""
@author: jldupont

# Labels

* The parameter `--labels` is an alias for `--update-labels`.
* When `--clear-labels` is also specified along with `--labels`,
  clearing takes precedence

# References

* [Cloud Run](https://cloud.google.com/run/docs/deploying)
"""

from typing import Union, Optional
from pygcloud.models import (
    GCPServiceRevisionBased,
    Params,
    GCPServiceSingletonImmutable,
    OptionalParamFromAttribute,
)
from pygcloud.gcp.labels import LabelGenerator
from pygcloud.gcp.models import CloudRunRevisionSpec, CloudRunNegSpec
from pygcloud.gcp.services.iam import ServiceAccountCapableMixin, IAMBindingCapableMixin


class CloudRun(
    GCPServiceRevisionBased,
    LabelGenerator,
    ServiceAccountCapableMixin,
    IAMBindingCapableMixin,
):
    """
    https://cloud.google.com/sdk/gcloud/reference/run

    CAUTION: sensitive information can be contained in the spec
             e.g. in the environment variables
    """

    LISTING_CAPABLE = True
    DEPENDS_ON_API = "run.googleapis.com"
    SPEC_CLASS = CloudRunRevisionSpec
    GROUP = ["beta", "run"]
    GROUP_SUB_DESCRIBE = [
        "services",
    ]

    def __init__(
        self, name: str, *params: Params, region: Optional[Union[str, None]] = None
    ):
        super().__init__(name=name, ns="run")
        assert isinstance(region, str)
        self.params = list(params)
        self.region = region

    def params_describe(self):
        return ["describe", self.name, "--region", self.region, "--format", "json"]

    def params_create(self):
        """
        The common parameters such as project_id would normally
        be injected through the Deployer.
        """
        return (
            [
                "deploy",
                self.name,
                "--clear-labels",
                "--region",
                self.region,
                OptionalParamFromAttribute(
                    "--service-account", self.service_account, "email"
                ),
                "--format",
                "json",
            ]
            + self.params
            + self.generate_use_labels()
        )


class CloudRunNeg(GCPServiceSingletonImmutable):
    """
    Cloud Run NEG

    https://cloud.google.com/sdk/gcloud/reference/beta/compute/network-endpoint-groups
    """

    LISTING_CAPABLE = True
    DEPENDS_ON_API = "compute.googleapis.com"
    REQUIRES_DESCRIBE_BEFORE_CREATE = True
    SPEC_CLASS = CloudRunNegSpec
    GROUP = ["beta", "compute", "network-endpoint-groups"]

    def __init__(
        self, name: str, *params: Params, region: Optional[Union[str, None]] = None
    ):
        assert isinstance(region, str)
        super().__init__(name, ns="crneg")
        self._region = region
        self._params = list(params) + ["--region", region]

    def params_describe(self):
        return ["describe", self.name, "--region", self._region, "--format", "json"]

    def params_create(self):
        """
        In the params, typically:
        --cloud-run-url-mask=${URL_MASK}
        --cloud-run-service=${CLOUD_RUN_NAME}
        """
        return [
            "create",
            self.name,
            "network-endpoint-type",
            "serverless",
            "--format",
            "json",
        ] + self._params
