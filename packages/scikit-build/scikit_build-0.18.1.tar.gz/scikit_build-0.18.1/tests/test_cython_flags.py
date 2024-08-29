"""test_cython_flags
----------------------------------

Tries to build the `cython-flags` sample project.
"""

from __future__ import annotations

from . import project_setup_py_test


@project_setup_py_test("cython-flags", ["build"])
def test_hello_cython_builds():
    pass
