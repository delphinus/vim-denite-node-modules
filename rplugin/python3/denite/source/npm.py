from .base import Base
from denite.util import error
from json import loads
from operator import itemgetter
from os import R_OK, access
from pathlib import Path


class Source(Base):
    def __init__(self, vim):
        super().__init__(vim)

        self.name = "packages"
        self.kind = "directory"

    def gather_candidates(self, context):
        cwd = Path(self.vim.call("getcwd"))
        package_json = self._find_package_json(cwd)
        if not package_json:
            error(self.vim, "package.json not found")
            return []

        try:
            items = self._load_items(package_json)
        except:
            error(self.vim, f"Error occurred in reading {package_json}")
            return []

        node_modules = package_json.parent / "node_modules"
        candidates = []

        for package_dir in node_modules.iterdir():
            try:
                if package_dir.name.startswith("@"):
                    for sub_dir in package_dir.iterdir():
                        self._add_candidate(candidates, items, sub_dir)
                else:
                    self._add_candidate(candidates, items, package_dir)
            except:
                error(self.vim, f"Error occurred in reading {package_dir}")
                return []

        return sorted(
            candidates, key=itemgetter("source__is_prod", "source__is_dev", "word")
        )

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
            r"syntax match deniteNpmDev /\[[DO]\]/ contained containedin=deniteNpm"
        )

    def _add_candidate(self, candidates, items, package_dir):
        package_json = package_dir / "package.json"
        if access(package_json, R_OK):
            with package_json.open() as fp:
                obj = loads(fp.read())
                name = obj.get("name")
                flag = items.get(name, "[O]")
                version = obj.get("version", "unknown")
                candidates.append(
                    {
                        "word": name,
                        "abbr": f"{name} ({version}) {flag}",
                        "action__path": str(package_dir),
                        "source__is_prod": flag == "",
                        "source__is_dev": flag == "D",
                    }
                )

    def _load_items(self, path):
        with open(path) as fp:
            obj = loads(fp.read())
            deps = {x: "" for x in obj.get("dependencies", {})}
            dev_deps = {x: "[D]" for x in obj.get("devDependencies", {})}
            return {**deps, **dev_deps}

    def _find_package_json(self, path):
        if path == Path("/") or path.is_mount():
            return None
        p = path / "package.json"
        return p if access(p, R_OK) else self._find_package_json(path.parent)
