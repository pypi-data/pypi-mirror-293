import importlib.metadata


def _get_package_version() -> str:
    try:
        return importlib.metadata.version("opik")
    except importlib.metadata.PackageNotFoundError:
        return "Please install comet with `pip install opik`"


VERSION = _get_package_version()
