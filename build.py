# ruff: noqa: T201 S607
import subprocess
import sys
from pathlib import Path

import PyInstaller.__main__

commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode().strip()
Path("./src/version/commit_freeze.py").write_text(f'commit = "{commit}"\n')
print(f"wrote commit {commit}")
print("do you want to build to one file (1) or create an installer (2) ?")
answer = input("[1/2]: ")
if answer == "1":
    print("building")
    PyInstaller.__main__.run(["main-onefile.spec"])
elif answer == "2":
    print("building app")
    PyInstaller.__main__.run(["main-onedir.spec"])
else:
    print("invalid answer, quitting")
    sys.exit(-1)
print("deleting commit_freeze.py")
Path("./src/version/commit_freeze.py").unlink()
print("done")