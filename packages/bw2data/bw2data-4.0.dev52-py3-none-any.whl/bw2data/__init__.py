__all__ = [
    "dynamic_calculation_setups",
    "calculation_setups",
    "config",
    "convert_backend",
    "Database",
    "databases",
    "DataStore",
    "Edge",
    "extract_brightway_databases",
    "get_activity",
    "get_multilca_data_objs",
    "get_node",
    "get_id",
    "geomapping",
    "IndexManager",
    "JsonWrapper",
    "labels",
    "mapping",
    "Method",
    "methods",
    "Node",
    "Normalization",
    "normalizations",
    "parameters",
    "preferences",
    "prepare_lca_inputs",
    "ProcessedDataStore",
    "projects",
    "Searcher",
    "set_data_dir",
    "Weighting",
    "weightings",
]

__version__ = (4, 0, "dev52")

from .configuration import config, labels
from .project import projects
from .utils import set_data_dir
from .meta import (
    dynamic_calculation_setups,
    calculation_setups,
    databases,
    geomapping,
    methods,
    normalizations,
    preferences,
    weightings,
)

# Add metadata class instances to global list of serialized metadata
config.metadata.extend(
    [
        dynamic_calculation_setups,
        calculation_setups,
        databases,
        geomapping,
        methods,
        normalizations,
        preferences,
        weightings,
    ]
)

# Backwards compatibility - preferable to access ``preferences`` directly
config.p = preferences

from .serialization import JsonWrapper
from .database import DatabaseChooser as Database
from .utils import get_activity, get_node
from .data_store import DataStore, ProcessedDataStore
from .method import Method
from .search import Searcher, IndexManager
from .weighting_normalization import Weighting, Normalization
from .backends import convert_backend, get_id, Node, Edge
from .compat import prepare_lca_inputs, Mapping, get_multilca_data_objs
from .backends.wurst_extraction import extract_brightway_databases

mapping = Mapping()

from .updates import Updates
from .parameters import parameters

Updates.check_status()


try:
    # Will register itself as a database backend provider
    import multifunctional
except ImportError:
    pass
