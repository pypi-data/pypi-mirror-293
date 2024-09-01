import re
from setuptools import Distribution
from .. import build_version

_GITV = __name__.split(".")[0]
_VSEP = re.compile(r"([-.]?[a-z]+)", re.I)


def configure(dist: Distribution):
    if _GITV in dist.setup_requires:
        if v := dist.metadata.version:
            v = _VSEP.split(v, 1)[0]
        dist.metadata.version = build_version(v)
