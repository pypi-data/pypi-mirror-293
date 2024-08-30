"""
Cloud Scheduler

NOTE: Job can be created with pubsub publication without the topic
being created first.

@author: jldupont
"""

from pygcloud.models import GCPServiceUpdatable, Params
from pygcloud.gcp.models import SchedulerJob


class CloudScheduler(GCPServiceUpdatable):
    """
    https://cloud.google.com/sdk/gcloud/reference/scheduler

    NOTE: requires --location for listing
    """

    LISTING_CAPABLE = True
    LISTING_REQUIRES_LOCATION = True
    DEPENDS_ON_API = "cloudscheduler.googleapis.com"
    SPEC_CLASS = SchedulerJob
    GROUP = ["scheduler", "jobs"]

    def __init__(self, name: str, params_create: Params, params_update: Params):
        assert isinstance(name, str)
        super().__init__(name, ns="scheduler")
        self._params_create = list(params_create)
        self._params_update = list(params_update)

    def params_describe(self):
        return ["describe", self.name, "--format", "json"]

    def params_create(self):
        """
        https://cloud.google.com/sdk/gcloud/reference/scheduler/jobs/create
        """
        return ["create", self.name, "--format", "json"] + self._params_create

    def params_update(self):
        return ["update", self.name, "--format", "json"] + self._params_update
