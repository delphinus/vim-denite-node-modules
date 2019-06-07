from .base import Base
from denite.util import error
from os import R_OK, access
from os.path import dirname, ismount, join
from json import JSONDecodeError, loads
from functools import reduce


class Source(Base):
    def __init__(self, vim):
        super().__init__(vim)

        self.name = "packages"
        self.kind = "directory"

    def gather_candidates(self, context):
        cwd = self.vim.call("getcwd")
        package_json = self._find_package_json(cwd)
        if not package_json:
            error(self.vim, "package.json not found")
            return []

        items = self._load_items(package_json)
        if not items:
            return []

        root = dirname(package_json)
        candidates = []
        for item in items:
            path = join(root, "node_modules", item["name"], "package.json")
            if not access(path, R_OK):
                continue
            with open(path) as fp:
                try:
                    name = item["name"]
                    obj = loads(fp.read())
                    version = obj.get("version", "unknown")
                    dev_flag = " [D]" if item["dev"] else ""
                    candidates.append(
                        {
                            "word": name,
                            "abbr": f"{name} ({version}){dev_flag}",
                            "action__path": dirname(path),
                        }
                    )
                except JSONDecodeError:
                    error(self.vim, f"Decode error for {path}")
                    return []

        return candidates

    def highlight(self):
        self.vim.command("highlight default link deniteNpmName Title")
        self.vim.command("highlight default link deniteNpmVersion Statement")
        self.vim.command("highlight default link deniteNpmDev Comment")

    def define_syntax(self):
        self.vim.command(
            r"syntax match deniteNpm /^.*$/ containedin=" + self.syntax_name
        )
        self.vim.command(
            r"syntax match deniteNpmName /^\s\?\S\+/ contained containedin=deniteNpm"
        )
        self.vim.command(
            r"syntax match deniteNpmVersion /(.\{-})/ contained containedin=deniteNpm"
        )
        self.vim.command(
            r"syntax match deniteNpmDev /\[D\]/ contained containedin=deniteNpm"
        )

    def _load_items(self, path):
        with open(path) as fp:
            try:
                obj = loads(fp.read())
                deps = obj.get("dependencies")
                dev_deps = obj.get("devDependencies")
                items = []
                if deps:
                    items += [{"name": x, "dev": False} for x in deps]
                if dev_deps:
                    items += [{"name": x, "dev": True} for x in dev_deps]
                return items
            except JSONDecodeError:
                error(self.vim, f"Decode error for {path}")
                return []

    def _find_package_json(self, path):
        if path == "/" or ismount(path):
            return None
        p = join(path, "package.json")
        return p if access(p, R_OK) else self._find_package_json(dirname(path))
