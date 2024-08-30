"""
Google Cloud Storage

# Labels

* Cannot be added when creating a bucket
* `--clear-labels` cannot be used on the same command as `--update-labels`
* Updates should be put in one `--update-labels` or
  else inconsistent behavior is to be expected
* Thus, the current state of labels needs to be collected before updating
* `--remove-labels` must be used

**Note** there is no support for labels currently for buckets in pygcloud.

# References

* [Bucket Labels](https://cloud.google.com/storage/docs/using-bucket-labels)

@author: jldupont
"""

from pygcloud.models import Params, GCPServiceUpdatable
from pygcloud.gcp.models import GCSBucket
from pygcloud.gcp.services.iam import IAMBindingCapableMixin


class StorageBucket(GCPServiceUpdatable, IAMBindingCapableMixin):
    """
    https://cloud.google.com/sdk/gcloud/reference/storage
    """

    LISTING_CAPABLE = True
    DEPENDS_ON_API = "storage.googleapis.com"
    REQUIRES_UPDATE_AFTER_CREATE = False
    SPEC_CLASS = GCSBucket
    GROUP = ["storage", "buckets"]

    def __init__(
        self, name: str, params_create: Params = [], params_update: Params = []
    ):
        assert isinstance(name, str)

        if not name.startswith("gs://"):
            name = f"gs://{name}"

        super().__init__(name=name, ns="gcs")
        self._params_create = params_create
        self._params_update = params_update

    def params_describe(self):
        return ["describe", f"{self.name}", "--format", "json"]

    def params_create(self):
        return ["create", f"{self.name}", "--format", "json"] + self._params_create

    def params_update(self):
        return ["update", f"{self.name}", "--format", "json"] + self._params_update
