try:
    from .torch import jrmpc, initialize_cluster_centers
except (ModuleNotFoundError, ImportError):
    from .numpy import jrmpc, initialize_cluster_centers
