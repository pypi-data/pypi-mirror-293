from cleo.io.io import IO
from poetry.plugins.plugin import Plugin
from poetry.poetry import Poetry
from .. import build_version

_GITV = __name__.split(".")[0]


class GitVersionPlugin(Plugin):
    def activate(self, poetry: Poetry, io: IO):
        if _GITV in poetry.pyproject.build_system.requires:
            if v := poetry.package.version:
                parts = (v.major, v.minor, v.patch)
                v = ".".join(str(p) for p in parts if p is not None)
            poetry.package.version = build_version(v)
