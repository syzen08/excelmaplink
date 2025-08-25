import subprocess


def get_commit() -> str:
    try:
        # exists only when frozen, as the file gets created by the build script 
        from src.version.commit_freeze import commit # pyright: ignore[reportMissingImports]  # noqa: PLC0415
        return commit
    except ImportError:
        try: 
            return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode().strip()  # noqa: S607
        except Exception: # if anything goes wrong, just return unknown
            return "unknown"