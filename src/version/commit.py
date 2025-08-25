import subprocess


def get_commit() -> str:
    try:
        # exists only when frozen, as the file gets created by the build script 
        from src.version.commit_freeze import commit # pyright: ignore[reportMissingImports]
        return commit
    except ImportError:
        try: 
            commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode().strip()
            return commit
        except Exception: # if anything goes wrong, just return unknown
            return "unknown"