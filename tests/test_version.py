from __future__ import annotations

from importlib.metadata import version

from new_project import __version__


def test_version_matches_installed_distribution() -> None:
    assert __version__ == version("new-project")
