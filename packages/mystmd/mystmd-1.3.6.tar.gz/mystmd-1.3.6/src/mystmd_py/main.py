import os
import pathlib
import shutil
import subprocess
import sys
import re


def main():
    NODE_LOCATION = (
        shutil.which("node") or shutil.which("node.exe") or shutil.which("node.cmd")
    )
    PATH_TO_BIN_JS = (pathlib.Path(__file__).parent / "myst.cjs").resolve()

    if not NODE_LOCATION:
        raise SystemExit(
            "You must install node >=18 to run MyST\n\n"
            "We recommend installing the latest LTS release, using your preferred package manager\n"
            "or following instructions here: https://nodejs.org/en/download"
        )
    node = pathlib.Path(NODE_LOCATION).absolute()

    _version = subprocess.run(
        [node, "-v"], capture_output=True, check=True, text=True
    ).stdout
    major_version_match = re.match(r"v(\d+).*", _version)

    if major_version_match is None:
        raise SystemExit(f"MyST could not determine the version of Node.js: {_version}")

    major_version = int(major_version_match[1])
    if not (major_version in {18, 20, 22} or major_version > 22):
        raise SystemExit(
            f"MyST requires node 18, 20, or 22+; you are running node {major_version}.\n\n"
            "Please update to the latest LTS release, using your preferred package manager\n"
            "or following instructions here: https://nodejs.org/en/download"
        )
    os.execve(
        node,
        [node.name, PATH_TO_BIN_JS, *sys.argv[1:]],
        {**os.environ, "MYST_LANG": "PYTHON"},
    )


if __name__ == "__main__":
    main()
