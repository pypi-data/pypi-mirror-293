from .decorator.tracker import track, flush_tracker
from .api_objects.comet import Comet
from .api_objects.trace import Trace
from .api_objects.span import Span
from .api_objects.dataset.dataset_item import DatasetItem
from .api_objects.dataset import Dataset
from . import _logging
from . import package_version

_logging.setup()

__version__ = package_version.VERSION
__all__ = [
    "__version__",
    "track",
    "flush_tracker",
    "Comet",
    "Trace",
    "Span",
    "DatasetItem",
    "Dataset",
]
