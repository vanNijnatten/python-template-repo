import pkgutil
import subprocess
import sys

import pytest

import python_template_repo

MODULES = sorted(
    name
    for _, name, _ in pkgutil.walk_packages(
        python_template_repo.__path__, prefix=f"{python_template_repo.__name__}."
    )
    if name != "python_template_repo.__main__"
)


@pytest.mark.parametrize("module", ["archive_services", *MODULES])
def test_module_imports_in_isolation(module: str) -> None:
    """Import each module in a fresh interpreter so import cycles surface regardless of order."""
    result = subprocess.run(
        [sys.executable, "-c", f"import {module}"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
